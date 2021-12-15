#!/usr/bin/env python

import json
import logging
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import nltk
import numpy as np
import praw
from classifiers import sentiment_mod as sm
from google.cloud import firestore, secretmanager, storage

SUBREDDIT: str = "stocks"


def is_gcp_instance() -> bool:
    for env in os.environ:
        if "X_GOOGLE" in env:
            return True

    return False


def is_submission_valid(submission) -> bool:
    valid: bool = True

    # Omit non-text-based submissions i.e. image-based/link-based submissions
    if not submission.is_self:
        valid = False

    return valid


def upload_document_to_database(
    collection_path: str, document_id: str, data: dict, merge: bool = True
) -> None:
    try:
        # Write document
        firestore.Client().collection(collection_path).document(document_id).set(
            data, merge=merge
        )
    except Exception as e:
        # Swallow all exceptions and log
        logging.warning(f"An exception occured: { e }")


def get_submissions(subreddit: str) -> list:

    # Get PRAW client_secret from Google Cloud Secret Manager
    smsc = secretmanager.SecretManagerServiceClient()
    response = smsc.access_secret_version(
        request={"name": "projects/724762929986/secrets/PRAW/versions/latest"}
    )
    client_secret = response.payload.data.decode("UTF-8")

    # Setup PRAW
    reddit = praw.Reddit(
        client_id="yTDXCkdIpgE05A",
        client_secret=client_secret,
        user_agent=f"{sys.platform}:marketprediction:v0.2 (by u/KAHLYM)",
    )

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


def analyse(submissions: list) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket('market-prediction-5209e.appspot.com')
    blob = bucket.blob("sp500.json")
    data = blob.download_as_string().decode("utf-8")
    sp500 = json.loads(data)

    sentiments = defaultdict(list)
    sentiments_all: list = []

    for submission in submissions:
        # TODO Upload sentiment_mod to Google Cloud Platform
        classification, confidence = sm.sentiment(submission)

        # TODO Implement function to get ticker in submission
        # i.e something more appropriate than split()
        for ticker in [
            ticker for ticker in sp500 if f"${ticker}" in submission.split()
        ]:
            sentiments[ticker].append(
                (1 if classification == "pos" else -1) * confidence
            )

        sentiments_all.append((1 if classification == "pos" else -1) * confidence)

    # Calculate averages
    for ticker, sentiment in sentiments.items():
        sentiment32 = np.array(sentiment, dtype=np.float64)
        sentiment_mean = np.mean(sentiment32, axis=0)

        upload_document_to_database(
            "tickers",
            ticker,
            {
                datetime.today().strftime("%Y-%m-%d"): {
                    "score": round(sentiment_mean.item(), 2),
                    "count": len(sentiment),
                }
            },
            merge=True,
        )

    # subreddit
    sentiment32 = np.array(sentiments_all, dtype=np.float64)
    sentiment_mean = np.mean(sentiments_all, axis=0)

    upload_document_to_database(
        "subreddits",
        SUBREDDIT,
        {
            datetime.today().strftime("%Y-%m-%d"): {
                "score": round(sentiment_mean.item(), 2),
                "count": len(sentiments_all),
            }
        },
        merge=True,
    )


def get_reddit_submissions(event, context):

    if is_gcp_instance():
        root = os.path.dirname(os.path.abspath(__file__))
        download_dir = os.path.join(root, "nltk_data")
        os.chdir(download_dir)
        nltk.data.path.append(download_dir)

    analyse(get_submissions(SUBREDDIT))
