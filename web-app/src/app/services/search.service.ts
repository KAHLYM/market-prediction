import { Injectable } from '@angular/core';
import { doc, Firestore, getDoc } from '@angular/fire/firestore';

@Injectable({
    providedIn: 'root'
})
export class SearchService {
    search: { [key: string]: string } = {};

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

        console.log(this.search)
    }

    query(query: string): boolean {
        if (query in this.search) {
            return true;
        }
        else {
            return false;
        }
    }
}