import { ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {

  @ViewChild('searchInput', { static: false }) searchInput: any;

  open: boolean = false;
  searchValue: string = '';

  constructor(private changeDetectorRef: ChangeDetectorRef) { }

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
  
  onSearch(): void {
    this.setOpen(true);
    this.changeDetectorRef.detectChanges();
    this.onClear();
  }

}
