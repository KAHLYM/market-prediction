import {Component, OnInit} from '@angular/core';
import {FirestoreSentiment} from 'src/app/models/firestore-sentiment';
import {SentimentService} from 'src/app/services/sentiment.service';

@Component({
  selector: 'app-dummy',
  templateUrl: './dummy.component.html',
  styleUrls: ['./dummy.component.scss'],
})
export class DummyComponent implements OnInit {
  sentiments: FirestoreSentiment[] = [];

  constructor(private sentimentService: SentimentService) {
    this.sentimentService.getSubredditSentiments('stocks')
        .then((sentiments) => {
          this.sentiments = sentiments;
        });
  }

  ngOnInit(): void { }
}
