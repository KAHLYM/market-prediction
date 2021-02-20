import { ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';
import { SearchService } from 'src/app/services/search.service';

export interface Result {
  currency: string;
  description: string;
  name: string;
  ticker: string;
}

@Component({
  selector: 'app-discover',
  templateUrl: './discover.component.html',
  styleUrls: ['./discover.component.scss']
})
export class DiscoverComponent implements OnInit {

  @ViewChild('searchInput', { static: false }) searchInput: any;

  open: boolean = false;
  searchValue: string = '';
  searchFocused: boolean = true;
  results: Result[] = [];
  company: Result = {currency: '', description: '', name: '', ticker: ''};

  constructor(
    private searchService: SearchService) { }

  ngOnInit(): void {
  }

  onSearchClear(): void {
    this.searchValue = '';
    this.searchInput.nativeElement.focus();
  }

  onSearchFocus(): void {
    this.searchFocused = true;
  }

  onSearchKeyUp(): void {
    this.results = [];
    // Only search if if more that three chracters to improve performance
    if (this.searchValue.length >= 3) {
      this.searchService.search(this.searchValue).forEach(item => {
        var result: Result = { currency: '$', description: '', name: item[1], ticker: item[0] };
        this.results.push(result);
      });
    }
  }

  onResultClick(result: Result): void {
    this.searchFocused = false;
    this.searchValue = '';
    this.results = []
    this.company = result;
  }
  
}
