import {Injectable} from '@angular/core';
import {doc, Firestore, getDoc} from '@angular/fire/firestore';
import {FirestoreSentiment} from '../models/firestore-sentiment';

@Injectable({
  providedIn: 'root',
})
export class SentimentService {
  constructor(public firestore: Firestore) {
    this.firestore = firestore;
  }

  async getSubredditSentiments(subreddit: string): Promise<FirestoreSentiment[]> {
    const sentiments: FirestoreSentiment[] = [];
    getDoc(doc(this.firestore, 'subreddits', subreddit))
        .then((snapshot) => {
          const data = snapshot.data();
          for (const item in data) {
            if (Object.prototype.hasOwnProperty.call(data, item)) {
              sentiments.push({
                count: data[item]['count'],
                date: Date.parse(item),
                score: data[item]['score'],
              });
            }
          }
        })
        .catch((err) => {
          console.log(err);
        });
    return await Promise.resolve(sentiments);
  }
}
