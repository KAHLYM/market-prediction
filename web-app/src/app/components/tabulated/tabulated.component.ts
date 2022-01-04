import { Component, OnInit } from '@angular/core';
import { FirestoreSentiment } from 'src/app/models/firestore-sentiment';
import { SentimentService } from 'src/app/services/sentiment.service';

@Component({
  selector: 'app-tabulated',
  templateUrl: './tabulated.component.html',
  styleUrls: ['./tabulated.component.scss']
})
export class TabulatedComponent implements OnInit {

  sentiments: FirestoreSentiment[] = [];

  constructor(private sentimentService: SentimentService) { }

  ngOnInit(): void {
    this.sentiments = this.sentimentService.getSentiments();
  }

}
