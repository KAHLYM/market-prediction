from typing import Any
import unittest
from dataclasses import dataclass, field

from .main import analyse, is_submission_valid
from praw import Reddit
from praw.models.reddit.submission import Submission


class TestGetRedditSubmissions(unittest.TestCase):
    @dataclass(init=True, repr=True, eq=True)
    class parameterizedTest:
        returnValue: Any = None
        parameters: list = field(default_factory=list)

    tests: dict = {
        "is_submission_valid": [
            parameterizedTest(True, [True]),
            parameterizedTest(False, [False]),
        ],
    }

    def test_is_submission_valid(self):
        with self.subTest(params=[True, False]):
            for test in self.tests["is_submission_valid"]:
                submission: Submission = Submission(
                    Reddit, _data={"id": "test_id", "is_self": test.parameters[0]}
                )

                assert is_submission_valid(submission) is test.returnValue

    def test_analyse(self):
        submissions: list = ["AAPL amazing", "AAPL okay", "FB bad"]

        sentiments = analyse(submissions)

        self.assertEqual(len(sentiments), 2)
        self.assertIn("AAPL", sentiments)
        self.assertEqual(len(sentiments["AAPL"]), 2)
        self.assertIn("FB", sentiments)
        self.assertEqual(len(sentiments["FB"]), 1)


if __name__ == "__main__":
    unittest.main()
