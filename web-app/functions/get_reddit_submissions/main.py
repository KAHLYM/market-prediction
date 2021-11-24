#!/usr/bin/env python

from collections import defaultdict
import json
import logging
from pathlib import Path
import sys
from datetime import datetime, timedelta

import numpy as np
import praw
from .classifiers import sentiment_mod as sm
from google.cloud import firestore, secretmanager, storage
from google.cloud.storage.bucket import Bucket


def is_submission_valid(submission) -> bool:
    valid: bool = True

    # Omit non-text-based submissions i.e. image-based/link-based submissions
    if not submission.is_self:
        valid = False

    return valid


def upload_document_to_database(collection_path: str, document_id: str, data: dict, merge: bool = True) -> None:
    try:
        # Write document
        firestore.Client().collection(collection_path).document(document_id).set(data, merge=merge)
    except Exception as e:
        # Swallow all exceptions and log
        logging.warning(f"An exception occured: { e }")


def upload_document_to_storage(blob_name: str, data: str, content_type: str = "text/plain") -> None:
    try:
        # Write document
        bucket: Bucket = storage.Client.get_bucket("gs://market-prediction-5209e.appspot.com")
        bucket.blob(blob_name).upload_from_string(data, content_type)
    except Exception as e:
        # Swallow all exceptions and log
        logging.warning(f"An exception occured: { e }")

def get_submissions() -> list:

    # Get PRAW client_secret from Google Cloud Secret Manager
    smsc = secretmanager.SecretManagerServiceClient()
    response = smsc.access_secret_version(request={"name": "projects/724762929986/secrets/PRAW/versions/latest"})
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
    for subreddit in ["stocks"]:
        # Reddit API listing limited to 1000 items
        # PRAW will break request into multiple API calls of 100 items seperated by 2 second delay
        for submission in reddit.subreddit(subreddit).new(limit=None):

            if not is_submission_valid(submission):
                continue

            # Submissions are sorted by new so break when first post exceeds expirary
            if submission.created_utc < utc_expirary.timestamp():
                break
            
            submissions.append(submission.selftext)
            
            # upload_document_to_storage(f"{submission.id}.json", json.dumps({
            #     "created_utc": int(submission.created_utc),
            #     "subreddit": submission.subreddit.display_name,
            #     "title": submission.title,
            #     "selftext": submission.selftext,
            # }))
    
    return submissions


def analyse(submissions: list) -> list:
    # TODO Automate upload of s&p500.json to Google Cloud Platform
    with open(Path(__file__).parent / "s&p500.json", 'r') as j:
        sp500 = json.loads(j.read())

    sentiments = defaultdict(list)
    for submission in submissions:
        # TODO Upload sentiment_mod to Google Cloud Platform
        classification, confidence = sm.sentiment(submission)
        # TODO Implement function to get ticker in submission
        # i.e something more appropriate than split()
        for ticker in [ticker for ticker in sp500 if ticker in submission.split()]:
            sentiments[ticker].append([classification, confidence])

    return sentiments


def get_reddit_submissions(event, context):

    submissions = get_submissions()

    sentiments = analyse(submissions)
    
    # Calculate averages
    for ticker, sentiment in sentiments:
        sentiment_mean = np.mean(sentiment, axis=0)

        upload_document_to_database(ticker, datetime.today().strftime('%Y-%m-%d'), {
            "classification": sentiment_mean[0],
            "confidence": sentiment_mean[1],
            "entires": len(sentiment),
        }, merge=False)
