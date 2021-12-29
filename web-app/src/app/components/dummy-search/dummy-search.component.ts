import {Component, OnInit} from '@angular/core';
import {SearchService} from 'src/app/services/search.service';

@Component({
  selector: 'app-dummy-search',
  templateUrl: './dummy-search.component.html',
  styleUrls: ['./dummy-search.component.scss'],
})
export class DummySearchComponent implements OnInit {
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
}
