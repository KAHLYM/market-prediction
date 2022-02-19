import { Component, OnInit } from '@angular/core';
import { FirestoreSentiment } from 'src/app/models/firestore-sentiment';
import { LatestService } from 'src/app/services/latest.service';

@Component({
  selector: 'app-latest',
  templateUrl: './latest.component.html',
  styleUrls: ['./latest.component.scss']
})
export class LatestComponent implements OnInit {

  latest: {key :string, value: FirestoreSentiment}[] = [];

  constructor(private latestService: LatestService) {
    this.latestService.latestUpdated.subscribe(() => {
      Object.entries(this.latestService.getLatest()).forEach(([key, value]) => {
        this.latest.push(
          {
            key,
            value
          })
      });
    });
  }

  ngOnInit(): void {
    this.latestService.query("tickers");

    let animationDuration: number = 2000;
    setInterval(() => {
      const container = document.getElementsByClassName('LatestOverflow')[0];
      let animation = container.animate([
        { transform: 'translateX(-14rem)' } // Tile width
      ], {
        duration: animationDuration,
        iterations: 1
      });
      animation.onfinish = () => {
        let front = this.latest.shift()
        if (front)
        {
          this.latest.push(front);
        }
      }
    }, animationDuration);
  }

}
