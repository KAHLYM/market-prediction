#!/usr/bin/env python

import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Tuple

import nltk
import numpy as np
import praw
from classifiers import sentiment_mod as sm
from google.cloud import secretmanager
from helpers.firestore import (
    get_file_from_storage,
    upload_document_to_firestore_database,
)
from helpers.platform import is_gcp_instance

SUBREDDIT: str = "stocks"


def is_submission_valid(submission) -> bool:
    valid: bool = True

    # Omit non-text-based submissions i.e. image-based/link-based submissions
    if not submission.is_self:
        valid = False

    return valid


def setup_praw() -> praw.Reddit:
    # Get PRAW client_secret from Google Cloud Secret Manager
    smsc = secretmanager.SecretManagerServiceClient()
    response = smsc.access_secret_version(
        request={"name": "projects/724762929986/secrets/PRAW/versions/latest"}
    )
    client_secret = response.payload.data.decode("UTF-8")

    # Setup PRAW
    return praw.Reddit(
        client_id="yTDXCkdIpgE05A",
        client_secret=client_secret,
        user_agent=f"{sys.platform}:marketprediction:v0.2 (by u/KAHLYM)",
    )


def get_submissions(subreddit: str) -> list:
    reddit: praw.Reddit = setup_praw()

    submissions = []

    utc_expirary = datetime.utcnow() - timedelta(hours=24)

    # Fetch all subsmissions for given subreddit within 24
    # Reddit API listing limited to 1000 items
    # PRAW will break request into multiple API calls of 100 items seperated by 2 second delay
    for submission in reddit.subreddit(subreddit).new(limit=None):

        if not is_submission_valid(submission):
            continue

        # Submissions are sorted by new so break when first post exceeds expirary
        if submission.created_utc < utc_expirary.timestamp():
            break

        submissions.append(submission.selftext)

    return submissions


def extract_sentiment(
    submissions: list, tickers: json
) -> Tuple[defaultdict(list), list]:
    sentiments = defaultdict(list)
    sentiments_all: list = []

    for submission in submissions:
        # TODO #74 Upload sentiment_mod to Google Cloud Platform
        classification, confidence = sm.sentiment(submission)

        # TODO #189 Implement function to get ticker in submission
        # i.e something more appropriate than split()
        for ticker in [
            ticker for ticker in tickers if f"${ticker}" in submission.split()
        ]:
            sentiments[ticker].append(
                (1 if classification == "pos" else -1) * confidence
            )

        sentiments_all.append((1 if classification == "pos" else -1) * confidence)

    return sentiments, sentiments_all


def calculate_data(sentiment: list) -> Tuple[int, int]:
    sentiment32 = np.array(sentiment, dtype=np.float64)
    sentiment_mean = np.mean(sentiment32, axis=0)

    return round(sentiment_mean.item(), 2), len(sentiment)


def calculate_data_and_upload(
    sentiment: list, collection_path: str, document_id: str
) -> None:
    score, count = calculate_data(sentiment)

    upload_document_to_firestore_database(
        collection_path,
        document_id,
        {
            datetime.today().strftime("%Y-%m-%d"): {
                "score": score,
                "count": count,
            }
        },
        merge=True,
    )


# Google Cloud Platform entry point
def get_reddit_submissions(event, context):

    # The classifiers require corpora that were used to build said classifiers
    # nltk does not lazy load corpora so we need to install these on the instance
    if is_gcp_instance():
        root = os.path.dirname(os.path.abspath(__file__))
        download_dir = os.path.join(root, "nltk_data")
        os.chdir(download_dir)
        nltk.data.path.append(download_dir)

    sentiments, sentiments_all = extract_sentiment(
        get_submissions(SUBREDDIT), get_file_from_storage("sp500.json")
    )

    for ticker, sentiment in sentiments.items():
        calculate_data_and_upload(sentiment, "tickers", ticker)

    calculate_data_and_upload(sentiments_all, "subreddits", SUBREDDIT)
