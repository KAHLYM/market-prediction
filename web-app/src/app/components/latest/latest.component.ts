import { Component, OnInit } from '@angular/core';
import { FirestoreSentiment } from 'src/app/models/firestore-sentiment';
import { LatestService } from 'src/app/services/latest.service';

@Component({
  selector: 'app-latest',
  templateUrl: './latest.component.html',
  styleUrls: ['./latest.component.scss']
})
export class LatestComponent implements OnInit {

  latest: {[key: string] : FirestoreSentiment} = {};

  constructor(private latestService: LatestService) {
    this.latestService.latestUpdated.subscribe((next) => {
      this.latest = this.latestService.getLatest();
      console.log("latest:", this.latest);
    });
  }

  ngOnInit(): void {
    this.latestService.query("tickers");
  }

}
