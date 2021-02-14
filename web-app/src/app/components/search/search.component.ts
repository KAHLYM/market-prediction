import { ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';
import { SearchService } from 'src/app/services/search.service';

export interface Result {
  currency: string;
  description: string;
  name: string;
  ticker: string;
}

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {

  @ViewChild('searchInput', { static: false }) searchInput: any;

  open: boolean = false;
  searchValue: string = '';
  results: Result[] = [];

  constructor(
    private changeDetectorRef: ChangeDetectorRef,
    private searchService: SearchService) { }

  ngOnInit(): void {
  }

  setOpen(open: boolean): void {
    this.open = open;
    this.changeDetectorRef.detectChanges();
  }

  onBack(): void {
    this.setOpen(false);
  }

  onClear(): void {
    this.searchValue = '';
    this.searchInput.nativeElement.focus();
  }

  onKeyUp(): void {
    this.results = [];
    // Only search if if more that three chracters to improve performance
    if (this.searchValue.length >= 3) {
      this.searchService.search(this.searchValue).forEach(item => {
        var result: Result = { currency: '$', description: '', name: item[1], ticker: item[0] };
        this.results.push(result);
      });
    }
  }
  
  onSearch(): void {
    this.setOpen(true);
    this.changeDetectorRef.detectChanges();
    this.onClear();
  }

}
