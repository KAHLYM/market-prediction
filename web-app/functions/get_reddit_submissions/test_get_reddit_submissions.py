import json
import os
import unittest

from main import calculate_data, extract_sentiment, extract_tickers, is_submission_valid
from helpers.platform import is_gcp_instance
from praw import Reddit
from praw.models.reddit.submission import Submission


class TestGetRedditSubmissions(unittest.TestCase):
    """is_gcp_instance"""

    def test_is_gcp_instance_true(self):
        os.environ["X_GOOGLE"] = "TestValue"

        assert is_gcp_instance() == True

    def test_is_gcp_instance_false(self):
        if "X_GOOGLE" in os.environ:
            del os.environ["X_GOOGLE"]

        assert is_gcp_instance() == False

    """ is_submission_valid """

    def test_is_submission_valid_is_self(self):
        submission: Submission = Submission(
            Reddit, _data={"id": "test_id", "is_self": True}
        )

        assert is_submission_valid(submission) == True

    def test_is_submission_valid_is_not_self(self):
        submission: Submission = Submission(
            Reddit, _data={"id": "test_id", "is_self": False}
        )

        assert is_submission_valid(submission) == False

    """ extract_sentiment """

    def test_extract_sentiment_identifies_ticker(self):
        submissions: list = ["$TestKeyOne appears in this submission"]
        tickers: json = {
            "TestKeyOne": "TestValueOne",
        }

        sentiments, sentiments_all = extract_sentiment(submissions, tickers)

        assert len(sentiments) == 1
        assert len(sentiments_all) == 1

    def test_extract_sentiment_identifies_multiple_tickers_in_single_submission(self):
        submissions: list = [
            "$TestKeyOne appears in this submission and does $TestKeyTwo"
        ]
        tickers: json = {
            "TestKeyOne": "TestValueOne",
            "TestKeyTwo": "TestValueTwo",
        }

        sentiments, sentiments_all = extract_sentiment(submissions, tickers)

        assert len(sentiments) == 2
        assert len(sentiments_all) == 1

    def test_extract_sentiment_multiple_submissions(self):
        submissions: list = [
            "$TestKeyOne appears in this submission",
            "$TestKeyTwo appears in this submission",
        ]
        tickers: json = {
            "TestKeyOne": "TestValueOne",
            "TestKeyTwo": "TestValueTwo",
        }

        sentiments, sentiments_all = extract_sentiment(submissions, tickers)

        assert len(sentiments) == 2
        assert len(sentiments_all) == 2

    def test_extract_sentiment_identifies_single_ticker_in_multiple_submissions(self):
        submissions: list = [
            "$TestKeyOne appears in this submission",
            "$TestKeyOne appears in this submission",
        ]
        tickers: json = {
            "TestKeyOne": "TestValueOne",
        }

        sentiments, sentiments_all = extract_sentiment(submissions, tickers)

        assert len(sentiments) == 1
        assert len(sentiments_all) == 2

    def test_extract_sentiment_identifies_no_ticker(self):
        submissions: list = ["No ticker appears in this submission"]
        tickers: json = {}

        sentiments, sentiments_all = extract_sentiment(submissions, tickers)

        assert len(sentiments) == 0
        assert len(sentiments_all) == 1

    def test_extract_sentiment_identifies_unknown_ticker(self):
        submissions: list = ["$NoTicker appears in this submission"]
        tickers: json = {}

        sentiments, sentiments_all = extract_sentiment(submissions, tickers)

        assert len(sentiments) == 0
        assert len(sentiments_all) == 1

    """ extract_tickers """

    def test_extract_tickers_no_tickers(self):
        submission: str = "TestKeyOne appears in this submission"
        tickers: json = {
            "TestKeyOne": "TestValueOne",
        }

        extracted_tickers: list = extract_tickers(submission, tickers)

        assert len(extracted_tickers) == 1


    def test_extract_tickers_single_ticker(self):
        submission: str = "$TestKeyOne appears in this submission"
        tickers: json = {
            "TestKeyOne": "TestValueOne",
        }

        extracted_tickers: list = extract_tickers(submission, tickers)

        assert len(extracted_tickers) == 1
        assert "TestKeyOne" in extracted_tickers


    def test_extract_tickers_deuplicate_ticker(self):
        submission: str = "$TestKeyOne appears in this submission and does $TestKeyOne"
        tickers: json = {
            "TestKeyOne": "TestValueOne",
        }

        extracted_tickers: list = extract_tickers(submission, tickers)

        assert len(extracted_tickers) == 1
        assert "TestKeyOne" in extracted_tickers


    def test_extract_tickers_multiple_tickers(self):
        submission: str = "$TestKeyOne appears in this submission and does $TestKeyTwo"
        tickers: json = {
            "TestKeyOne": "TestValueOne",
            "TestKeyTwo": "TestValueTwo",
        }

        extracted_tickers: list = extract_tickers(submission, tickers)

        assert len(extracted_tickers) == 2
        assert "TestKeyOne" in extracted_tickers
        assert "TestKeyTwo" in extracted_tickers
    

    def test_extract_tickers_punctuation(self):
        submission: str = "$TestKeyOne, appears in this submission"
        tickers: json = {
            "TestKeyOne": "TestValueOne",
        }

        extracted_tickers: list = extract_tickers(submission, tickers)

        assert len(extracted_tickers) == 1
        assert "TestKeyOne" in extracted_tickers

    
    def test_extract_tickers_lowercase(self):
        submission: str = "$testkeyone appears in this submission"
        tickers: json = {
            "TestKeyOne": "TestValueOne",
        }

        extracted_tickers: list = extract_tickers(submission, tickers)

        assert len(extracted_tickers) == 1
        assert "TestKeyOne" in extracted_tickers

    
    def test_extract_tickers_uppercase(self):
        submission: str = "$TESTKEYONE appears in this submission"
        tickers: json = {
            "TestKeyOne": "TestValueOne",
        }

        extracted_tickers: list = extract_tickers(submission, tickers)

        assert len(extracted_tickers) == 1
        assert "TestKeyOne" in extracted_tickers


    """ calculate_data """

    def test_calculate_data_one_sentiment(self):
        sentiment: list = [0.25]
        score, count = calculate_data(sentiment)

        assert score == 0.25
        assert count == 1

    def test_calculate_data_two_sentiments(self):
        sentiment: list = [0.25, 0.75]
        score, count = calculate_data(sentiment)

        assert score == 0.50
        assert count == 2

    def test_calculate_data_three_sentiments(self):
        sentiment: list = [0.25, 0.50, 0.75]
        score, count = calculate_data(sentiment)

        assert score == 0.50
        assert count == 3

    def test_calculate_data_round_two_decimal_place_down(self):
        sentiment: list = [0.253, 0.504, 0.755]
        score, count = calculate_data(sentiment)

        assert score == 0.50
        assert count == 3

    def test_calculate_data_round_two_decimal_place_up(self):
        sentiment: list = [0.255, 0.506, 0.757]
        score, count = calculate_data(sentiment)

        assert score == 0.51
        assert count == 3


if __name__ == "__main__":
    unittest.main()
