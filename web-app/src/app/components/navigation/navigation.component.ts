import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit {

  open: boolean = false;

  constructor() { }

  ngOnInit(): void {
  }

  onMenuClick(): void {
    this.open = !this.open;
  }

  onLinkClick(): void {
    this.open = false;
  }
}
