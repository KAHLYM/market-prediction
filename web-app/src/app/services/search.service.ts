import { Injectable } from '@angular/core';

declare var require: any
@Injectable({
  providedIn: 'root'
})
export class SearchService {

  data: any = require('./data.json');

  constructor() { }

  search(searchValue: string) : [string, string][] {
    var matches: [string, string][] = [];
    
    var searchValueLower: string = searchValue.toLowerCase();

    for (var key in this.data) {
      var keyLower: string = key.toLowerCase();
      var valueLower: string = this.data[key].toLowerCase();

      if (keyLower.includes(searchValueLower) || valueLower.includes(searchValueLower)) {
        matches.push([key, this.data[key]]);
      }
    }

    return matches;
  }
}
