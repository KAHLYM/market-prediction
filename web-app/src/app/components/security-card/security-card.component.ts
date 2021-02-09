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
  @Input() ticker: string = '';

  constructor() { }

  ngOnInit(): void {
  }

}
