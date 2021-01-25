import praw
import warnings

from typing import List

class RedditWrapper:

    _submissions = []

    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

        print('PRAW is ' + ('' if self.reddit.read_only else 'not ') + 'running in read-only mode')

        self.limit = 100
        
    @property
    def limit(self) -> int:
        return self._limit

    @limit.setter
    def limit(self, value: int):
        if value < 0:
            raise AttributeError('invalid value, limit should not be negative')
        elif value > 1000:
            warnings.warn('Reddit API listing limited to 1000 items')

        self._limit = value

    @limit.deleter
    def limit(self):
        raise AttributeError('do not delete, limit can be set to 0')

    def submissions(self, subreddit: str, limit: int = None, text_based: bool = True) -> List[str]:
        self.limit = limit if limit else self.limit
        
        # Reddit limited to 100 items per request
        # PRAW will break request into multiple API calls of 100 items seperated by 2 second delay
        for submission in self.reddit.subreddit(subreddit).new(limit=self.limit):

            # Omit non-text-based submissions i.e. image-based/link-based submissions
            if text_based and not submission.selftext:
                continue
            
            self._submissions.append(submission.selftext)
        
        return self._submissions

    def write(self, outfile: str):
        with open(outfile, 'wb') as f:
            for submission in self._submissions:
                # Each line represents a submission
                submission = submission.replace('\n', ' ') + '\n'

                # Encode with utf-8 to ensure unicode support i.e. emojis
                f.write(submission.encode('utf-8'))
