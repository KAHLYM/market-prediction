import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {Auth, getAuth, signInAnonymously} from '@angular/fire/auth';
import {Router} from '@angular/router';
import {SearchService} from 'src/app/services/search.service';
import {SentimentService} from 'src/app/services/sentiment.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss'],
})
export class SearchComponent implements OnInit {
  @ViewChild('SearchInput') searchElement!: ElementRef;

  results: Array<[string, string]> = [];
  showResults: boolean = true;

  constructor(
    private searchService: SearchService,
    private sentimentService: SentimentService,
    private router: Router,
    private auth: Auth) {
    // TODO: Move to be global
    signInAnonymously(getAuth())
        .then(() => {
          console.log('Signed in anonymously');
          // Signed in..
        })
        .catch((error) => {
          const errorCode = error.code;
          const errorMessage = error.message;
          console.log('Failed to sign in anonymously with error code ', errorCode, 'and message ', errorMessage);
          // ...
        });
  }

  ngOnInit(): void { }
  

  // Helpers

  updateInputValue(value: string) : void {
    this.searchElement.nativeElement.value = value;
    (this.searchElement.nativeElement as HTMLInputElement).selectionStart = value.length;
  }

  readonly RESULT_INDEX_MIN : number = 0;
  readonly RESULT_INDEX_MAX : number = 4;
  resultIndex: number = -1; // zero-indexed
  updateResultElements() : void {
    let elements = document.getElementsByClassName("SearchResultContainer")[0].querySelectorAll(".SearchResult");
    elements.forEach((element, index) => {
      if (element.getAttribute("mouseon") == "false") {
        (element as HTMLElement).setAttribute("selected", index == this.resultIndex ? "true" : "false");
      }
    });
  }
  
  // Global Events
   
  onFocusOut(event: FocusEvent): void {
    this.showResults = false;
  }

  // Input Events

  onInputKey(event: KeyboardEvent) : void {
      switch(event.key) {
      case "Enter":
        if (this.resultIndex >= this.RESULT_INDEX_MIN && this.resultIndex <= this.RESULT_INDEX_MAX) {
          let query = document.getElementsByClassName("SearchResultContainer")[0].querySelectorAll(".SearchResult")[this.resultIndex].querySelectorAll("div")[1].innerHTML;
          this.searchService.setQuery(query);
          this.updateInputValue(query);
          this.router.navigate(['result']);
          this.sentimentService.query(query, "ticker"); // TODO Fix query second parameter
        }
        break;
      case "ArrowUp":
        if (this.resultIndex == this.RESULT_INDEX_MIN ||
            this.resultIndex == this.RESULT_INDEX_MIN - 1) {
          this.resultIndex = this.RESULT_INDEX_MAX + 1;
        } else {
          this.resultIndex--;
        }
        this.updateResultElements();
        break;
      case "ArrowDown":
        if (this.resultIndex == this.RESULT_INDEX_MAX || 
            this.resultIndex == this.RESULT_INDEX_MAX + 1) {
          this.resultIndex = this.RESULT_INDEX_MIN - 1;
        } else {
          this.resultIndex++;
        }
        this.updateResultElements();
        break;
      default:
        this.results.length = 0;
        this.searchService.query((<HTMLInputElement>event.target).value).map((result) => {
          this.results.push([result, this.searchService.getType(result)]);
        });
        break;
    }
  }

  onInputFocus(event: MouseEvent) : void {
    this.showResults = true;
  }

  onInputClear(event: MouseEvent): void {
    this.searchElement.nativeElement.value = '';
    this.searchElement.nativeElement.focus();
    this.results.length = 0;
  }

  // Result Events
  
  onResultMouseDown(event: MouseEvent, result: [string, string]): void {
    this.searchService.setQuery(result[0]);
    this.updateInputValue(result[0]);
    this.router.navigate(['result']);
    this.sentimentService.query(result[0], result[1]);
  }

  onResultMouseEnter(event: MouseEvent, index: number): void {
    this.resultIndex = index;
    (event.target as HTMLElement).setAttribute("selected", "true");
    (event.target as HTMLElement).setAttribute("mouseon", "true");
    this.updateResultElements();
  }

  onResultMouseLeave(event: MouseEvent) : void{
    (event.target as HTMLElement).setAttribute("selected", "false");
    (event.target as HTMLElement).setAttribute("mouseon", "false");
    this.updateResultElements();
  }
}
