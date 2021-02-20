import { ListKeyManager } from '@angular/cdk/a11y';
import { Injectable } from '@angular/core';

// TODO: Remove with backend implementation
declare var require: any
let data: any = require('./data.json');

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  constructor() { }

  search(searchValue: string) : [string, string][] {
    var matches: [string, string][] = [];
    
    var searchValueLower: string = searchValue.toLowerCase();

    for (var key in data) {
      var keyLower: string = key.toLowerCase();
      var valueLower: string = data[key].toLowerCase();

      if (keyLower.includes(searchValueLower) || valueLower.includes(searchValueLower)) {
        matches.push([key, data[key]]);
      }
    }

    return matches;
  }
}
