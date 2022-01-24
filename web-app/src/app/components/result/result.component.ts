import { Component, OnInit } from '@angular/core';
import { SearchService } from 'src/app/services/search.service';
import { SentimentService } from 'src/app/services/sentiment.service';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss']
})
export class ResultComponent implements OnInit {

  query: string = "";
  queryType: string = "";

  constructor(
    private sentimentService: SentimentService,
    private searchService: SearchService) {

    this.sentimentService.sentimentsUpdated.subscribe(next => {
      this.query = this.searchService.getQuery();
      this.queryType = this.searchService.getType(this.query);
    });
  }

  ngOnInit(): void {
  }

}
