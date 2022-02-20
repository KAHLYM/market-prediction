import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-display-value',
  templateUrl: './display-value.component.html',
  styleUrls: ['./display-value.component.scss']
})
export class DisplayValueComponent implements OnInit {

  @Input() key: string = "n/a";
  @Input() value: string = "n/a";
  @Input() sign: string = "neu";
  @Input() left?: boolean = false;
  @Input() right?: boolean = false;
  @Input() trailingZero?: boolean = false;

  backgroundColor: string = 'e8eaed';
  color: string= '#202124';

  constructor() { }

  ngOnInit(): void {
    switch(this.sign) {
      case 'neg':
        this.backgroundColor = '#fce8e6';
        this.color = '#a50e0e';
        break;
      case 'pos':
        this.backgroundColor = '#e6f4ea';
        this.color = '#137333';
        break;
      case 'neu':
        this.backgroundColor = '#e8eaed';
        this.color = '#202124';
        break;
      default: // 'raw'
        this.backgroundColor = 'transparent';
        this.color = '#202124';
    }
  }

}
