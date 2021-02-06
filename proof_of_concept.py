import pickle
import sys

from classifiers.sentdex import sentiment_mod as sm
from secret import secret
from streams.reddit import reddit as r

TICKER = 'AAPL'

nasdaq_f = open('data/nasdaq/nasdaq.pickle', 'rb')
nasdaq = pickle.load(nasdaq_f)
nasdaq_f.close()

user_agent = f'{sys.platform}:marketprediction:v0.1 (by u/KAHLYM)'
rw = r.RedditWrapper(secret['reddit']['client_id'], secret['reddit']['client_secret'], user_agent=user_agent)

open_file = open('data/nasdaq/nasdaq.pickle', 'rb')
nasdaq = pickle.load(open_file)
open_file.close()

for submission in rw.submissions('stocks', limit=1000, text_based=False):
    if (TICKER in submission) or (nasdaq[TICKER] in submission):
        classification, confidence = sm.sentiment(submission)
        print(f'{"positive" if confidence > 0 else "negative"} @ {confidence:.2f}')
