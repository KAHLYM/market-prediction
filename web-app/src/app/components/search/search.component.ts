import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import {SearchService} from 'src/app/services/search.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {

  @ViewChild('SearchInput') searchElement!: ElementRef;

  results: string[] = [];

  constructor(private searchService: SearchService) {
    this.searchService = searchService;
  }

  ngOnInit(): void {
  }

  onKey(event: KeyboardEvent): void {
    this.results = this.searchService.query((<HTMLInputElement>event.target).value);
    console.log(this.results);
  }

  onClear(event: MouseEvent): void {
    this.searchElement.nativeElement.value = "";
    this.searchElement.nativeElement.focus();
  }
}
