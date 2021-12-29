import { Injectable } from '@angular/core';
import { doc, Firestore, getDoc } from '@angular/fire/firestore';

@Injectable({
    providedIn: 'root'
})
export class SearchService {
    search: { [key: string]: string } = {};
    threshold: number = 1;

    constructor(public firestore: Firestore) {
        this.firestore = firestore;

        getDoc(doc(this.firestore, "search", "search"))
            .then((snapshot) => {
                const data = snapshot.data();
                for (const item in data) {
                    this.search[item] = data[item];
                }
            })
            .catch(err => {
                console.log(err);
            });
    }

    query(query: string): string[] {
        let rankings: { [key: string]: number } = {};
        for (const key in this.search) {
            let rank: number = 0;

            for (let index = 0; index < query.length; index++) {
                if (key.includes(query.substring(0, index))) {
                    rank = index;
                }
            }
            
            if (key.startsWith(key)) {
                rank++;
            }

            if (key == query) {
                rank++;
            }

            if (rank > this.threshold) {
                rankings[key] = rank;
            }
        }

        return this.sortByValue(rankings);
    }

    // Credit @Nosredna: https://stackoverflow.com/a/1069840
    sortByValue(items: { [key: string]: number }): string[] {
        return Object.keys(Object.fromEntries(
            Object.entries(items).sort(([, a], [, b]) => a - b).reverse()
        ));
    }
}