import {EventEmitter, Injectable} from '@angular/core';
import {doc, Firestore, getDoc} from '@angular/fire/firestore';
import {FirestoreSentiment} from '../models/firestore-sentiment';

@Injectable({
  providedIn: 'root',
})
export class SentimentService {
  constructor(public firestore: Firestore) {
    this.firestore = firestore;
  }

  sentimentsUpdated: EventEmitter<boolean> = new EventEmitter();
  sentiments: FirestoreSentiment[] = [];

  getSentiments(): FirestoreSentiment[] {
    return this.sentiments;
  }

  async query(q: string, t: string): Promise<boolean> {
    // FIXME
    // Update firebase search dictionary value to be collection name
    const collection: string = t == 'ticker' ? 'tickers' : 'subreddits';
    await getDoc(doc(this.firestore, collection, q))
        .then((snapshot) => {
          const data = snapshot.data();
          const sentimentsFormatted: FirestoreSentiment[] = [];
          // eslint-disable-next-line guard-for-in
          for (const item in data) {
            if (Object.prototype.hasOwnProperty.call(data, item)) {
              sentimentsFormatted.push({
                count: data[item]['count'],
                date: Date.parse(item),
                score: data[item]['score'],
              });
            }
            this.sentiments = sentimentsFormatted.sort(function(x, y) {
              if (y.date && x.date) {
                return y.date - x.date;
              } else {
                // we should not hit this case
                return 0;
              }
            });
          }
          this.sentimentsUpdated.emit(true);
          return true;
        })
        .catch((err) => {
          console.log(err);
        });
    return false;
  }
}
