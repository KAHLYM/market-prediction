#!/usr/bin/env python

import logging
import sys
from datetime import datetime, timedelta

import praw
from google.cloud import firestore, secretmanager


def get_reddit_submissions(event, context):

    # Get PRAW client_secret from Google Cloud Secret Manager
    sm = secretmanager.SecretManagerServiceClient()
    response = sm.access_secret_version(request={"name": "projects/63698589299/secrets/PRAW/versions/latest"})
    client_secret = response.payload.data.decode("UTF-8")

    # Setup PRAW
    reddit = praw.Reddit(
        client_id="yTDXCkdIpgE05A",
        client_secret=client_secret,
        user_agent=f"{sys.platform}:marketprediction:v0.2 (by u/KAHLYM)",
    )

    utc_expirary = datetime.utcnow() - timedelta(hours=24)

    # Fetch all subsmissions for given subreddit within 24
    for subreddit in ["stocks"]:
        # Reddit API listing limited to 1000 items
        # PRAW will break request into multiple API calls of 100 items seperated by 2 second delay
        for submission in reddit.subreddit(subreddit).new(limit=None):

            # Omit non-text-based submissions i.e. image-based/link-based submissions
            if not submission.is_self:
                continue

            # Submissions are sorted by new so break when first post exceeds expirary
            if submission.created_utc < utc_expirary.timestamp():
                break

            try:
                # Write document
                firestore.Client().collection("source:reddit").document(
                    submission.id
                ).set(
                    {
                        "created_utc": int(submission.created_utc),
                        "subreddit": submission.subreddit.display_name,
                        "title": submission.title,
                        "selftext": submission.selftext,
                    },
                    merge=True,
                )

            except Exception as e:
                # Swallow all exceptions and log
                logging.warning(f"An acveption occured: { e }")
