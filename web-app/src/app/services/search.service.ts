import {Injectable} from '@angular/core';
import {doc, Firestore, getDoc} from '@angular/fire/firestore';
import {FirestoreSearch} from '../models/firestore-search';

@Injectable({
  providedIn: 'root',
})
export class SearchService {
  q: string = '';
  search: { [key: string]: FirestoreSearch } = {};
  threshold: number = 1;

  constructor(public firestore: Firestore) {
    this.firestore = firestore;

    getDoc(doc(this.firestore, 'search', 'search'))
        .then((snapshot) => {
          const data = snapshot.data();
          for (const item in data) {
            if (Object.prototype.hasOwnProperty.call(data, item)) {
              this.search[item] = data[item];
            }
          }
        })
        .catch((err) => {
          console.log(err);
        });
  }

  query(query: string): string[] {
    const queryLowerCase: string = query.toLocaleLowerCase();
    const rankings: { [key: string]: number } = {};
    for (const key in this.search) {
      if (Object.prototype.hasOwnProperty.call(this.search, key)) {
        const keyLowerCase: string = key.toLocaleLowerCase();
        let rank: number = 0;

        for (let index = 0; index < queryLowerCase.length; index++) {
          if (keyLowerCase.includes(queryLowerCase.substring(0, index))) {
            rank = index;
          }
        }

        if (keyLowerCase.startsWith(queryLowerCase)) {
          rank++;
        }

        if (keyLowerCase == queryLowerCase) {
          rank++;
        }

        if (rank > this.threshold) {
          rankings[key] = rank;
        }
      }
    }

    return this.sortByValue(rankings);
  }

  getQuery(): string {
    return this.q;
  }

  setQuery(query: string) {
    this.q = query;
  }

  // Credit @Nosredna: https://stackoverflow.com/a/1069840
  sortByValue(items: { [key: string]: number }): string[] {
    return Object.keys(Object.fromEntries(
        Object.entries(items).sort(([, a], [, b]) => a - b).reverse(),
    ));
  }

  getFirestoreSearch(query: string): FirestoreSearch {
    return this.search[query];
  }
}
