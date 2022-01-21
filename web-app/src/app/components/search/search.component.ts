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

  results: string[] = [];
  showResults: boolean = true;

  constructor(private searchService: SearchService, private sentimentService: SentimentService, private router: Router, auth: Auth) {
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

  ngOnInit(): void {
  }

  onKey(event: KeyboardEvent): void {
    this.results = this.searchService.query((<HTMLInputElement>event.target).value);
  }

  onClear(event: MouseEvent): void {
    this.searchElement.nativeElement.value = '';
    this.searchElement.nativeElement.focus();
    this.results.length = 0;
  }

  onResult(event: MouseEvent, result: string): void {
    this.searchElement.nativeElement.value = result;
    this.sentimentService.queryTicker(result).then(() => {
      this.router.navigate(['tabulated']);
    });
  }

  onFocus(event: MouseEvent) : void {
    this.showResults = true;
  }

  onFocusOut(event: FocusEvent): void {
    this.showResults = false;
  }
}
