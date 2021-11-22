from typing import Any
import unittest
from dataclasses import dataclass, field

from main import is_submission_valid
from praw import Reddit
from praw.models.reddit.submission import Submission


class TestGetRedditSubmissions(unittest.TestCase):
    
    @dataclass(init=True, repr=True, eq=True)
    class test:
        returnValue: Any = None
        parameters: list = field(default_factory=list)

    tests: dict = {
        "is_submission_valid": [
            test(True, [True]),
            test(False, [False])],
    }

    def test_is_submission_valid(self):
        with self.subTest(params=[True, False]):
            for test in self.tests["is_submission_valid"]:
                submission: Submission = Submission(Reddit, _data={'id': 'test_id', "is_self": test.parameters[0]})
                
                assert is_submission_valid(submission) is test.returnValue

if __name__ == '__main__':
    unittest.main()
