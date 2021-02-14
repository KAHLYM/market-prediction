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
    
    for (var key in data) {
      if (key.includes(searchValue) || data[key].includes(searchValue)) {
        matches.push([key, data[key]]);
      }
    }

    return matches;
  }
}
