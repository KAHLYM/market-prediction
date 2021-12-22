import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { Observable } from 'rxjs';
import { FirestoreSentiment } from '../models/firestore-sentiment';

@Injectable({
  providedIn: 'root'
})
export class SentimentService {
  sentiments: Observable<FirestoreSentiment[]>;

  constructor(public afs: AngularFirestore) {
    this.sentiments = this.afs.collection<FirestoreSentiment>("subreddits").valueChanges();
  }

  getSentiments() {
    return this.sentiments;
  }
}
