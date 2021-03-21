# functions

## get_reddit_submissions

### Description

This function will gather reddit submissions for given subreddits and store the information in Firebase. As of March 2021, the given subreddit is r/stocks. The function is triggered by cloud pub/sub and is scheduled to run with cron schedule expression  ```0 0 * * *``` i.e. at 00:00. The function will upload data in the format specified below. Although, the schema is not enforced.

### Firebase Reddit Submission Schema
```
{
    "title": "Firebase Reddit Submission Schema",
    "type": "object",
    "properties": {
        "created_utc": {
            "type": "int",
            "description": "The epoch time of the submission"
        },
        "subreddit": {
            "type": "string",
            "description": "The subreddit of the submission"
        },
        "title": {
            "type": "string",
            "description": "The title of the submission"
        },
        "selftext": {
            "type": "string",
            "description": "The body of the submission"
        }
    }
}
```