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

  sentiments: FirestoreSentiment[] = [];

  getSentiments(): FirestoreSentiment[] {
    return this.sentiments;
  }

  async queryTicker(subreddit: string): Promise<boolean> {
    await getDoc(doc(this.firestore, 'tickers', subreddit))
        .then((snapshot) => {
          const data = snapshot.data();
          const sentimentsFormatted: FirestoreSentiment[] = [];
          for (const item in data) {
            if (Object.prototype.hasOwnProperty.call(data, item)) {
              sentimentsFormatted.push({
                count: data[item]['count'],
                date: Date.parse(item),
                score: data[item]['score'],
              });
            }
            this.sentiments = sentimentsFormatted;
          }
          return true;
        })
        .catch((err) => {
          console.log(err);
        });
    return false;
  }
}
