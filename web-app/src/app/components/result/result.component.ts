import {Component, OnInit} from '@angular/core';
import { FirestoreSearch } from 'src/app/models/firestore-search';
import {SearchService} from 'src/app/services/search.service';
import {SentimentService} from 'src/app/services/sentiment.service';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss'],
})
export class ResultComponent implements OnInit {
  query: string = '';
  queryData: FirestoreSearch = { type: ""};

  constructor(
    private sentimentService: SentimentService,
    private searchService: SearchService) {
    this.sentimentService.sentimentsUpdated.subscribe((next) => {
      this.query = this.searchService.getQuery();
      this.queryData = this.searchService.getFirestoreSearch(this.query);
    });
  }

  ngOnInit(): void {
  }
}
