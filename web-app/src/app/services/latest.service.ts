import {EventEmitter, Injectable} from '@angular/core';
import {doc, Firestore, getDoc} from '@angular/fire/firestore';
import {FirestoreSentiment} from '../models/firestore-sentiment';

@Injectable({
  providedIn: 'root',
})
export class LatestService {
  constructor(public firestore: Firestore) {
    this.firestore = firestore;
  }

  latestUpdated: EventEmitter<boolean> = new EventEmitter();
  latest: {[key: string] : FirestoreSentiment} = {};

  getLatest(): {[key: string] : FirestoreSentiment} {
    return this.latest;
  }

  async query(q: string): Promise<boolean> {
    await getDoc(doc(this.firestore, "latest", q))
        .then((snapshot) => {
          const data = snapshot.data();
          // eslint-disable-next-line guard-for-in
          for (const item in data) {
            if (Object.prototype.hasOwnProperty.call(data, item)) {
              this.latest[item] = {
                count: data[item]['count'],
                score: data[item]['score'],
              };
            }
          }
          this.latestUpdated.emit(true);
          return true;
        })
        .catch((err) => {
          console.log(err);
        });
    return false;
  }
}
