import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-security-card',
  templateUrl: './security-card.component.html',
  styleUrls: ['./security-card.component.scss'],
})
export class SecurityCardComponent implements OnInit {

  @Input() description: string = '';
  @Input() imgSrc: string = ''
  @Input() name: string = '';
  @Input() sentiment: string = '';
  @Input() ticker: string = '';
  @Input() movement: string = '';

  constructor() { }

  ngOnInit(): void {
  }

  parseFloat(sentiment: string): number {
    return parseFloat(sentiment);
  }

}
