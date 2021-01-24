import praw
import secret

reddit = praw.Reddit(
    client_id=secret.client_id,
    client_secret=secret.client_secret,
    user_agent=secret.user_agent
)

print('PRAW is ' + ('' if reddit.read_only else 'not ') + 'running in read-only mode')

submissions = []
submissions_skipped = 0
submissions_limit = 10

# Reddit limited to 100 items per request
# PRAW will break request into multiple API calls of 100 items seperated by 2 second delay
for index, submission in enumerate(reddit.subreddit('all').hot(limit=submissions_limit)):
    submissions.append(submission.selftext)

# Write to .txt file where each line represents a submission
with open('outfile.txt', 'wb') as f:
    for submission in submissions:
        submission = submission.replace('\n', '') + '\n'

        # Skip submissions that contains no text i.e. image-based/link-based submissions
        if submission is '\n':
            submissions_skipped += 1
            continue
        
        # Encode with utf-8 to ensure unicode support i.e. emojis
        f.write(submission.encode('utf-8'))

print(f'{"Submissions skipped":<20}{submissions_skipped:>4}')
print(f'{"Submissions limit":<20}{submissions_limit:>4}')
