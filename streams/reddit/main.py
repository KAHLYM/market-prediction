import praw

class RedditWrapper:

    _submissions = []

    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

        print('PRAW is ' + ('' if self.reddit.read_only else 'not ') + 'running in read-only mode')

    def submissions(self, subreddit: str, limit: int, text_based: bool = True) -> int:
        complete: int = 0

        # Reddit limited to 100 items per request
        # PRAW will break request into multiple API calls of 100 items seperated by 2 second delay
        for submission in self.reddit.subreddit(subreddit).new(limit=limit):

            # Omit non-text-based submissions i.e. image-based/link-based submissions
            if text_based and not submission.selftext:
                continue
            
            self._submissions.append(submission.selftext)
            complete += 1
        
        return complete

    def write(self, outfile: str):
        with open(outfile, 'wb') as f:
            for submission in self._submissions:
                # Each line represents a submission
                submission = submission.replace('\n', ' ') + '\n'

                # Encode with utf-8 to ensure unicode support i.e. emojis
                f.write(submission.encode('utf-8'))
