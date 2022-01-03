import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { Auth, getAuth, signInAnonymously } from '@angular/fire/auth';
import {SearchService} from 'src/app/services/search.service';

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent implements OnInit {

  @ViewChild('SearchInput') searchElement!: ElementRef;

  results: string[] = [];

  constructor(private searchService: SearchService, auth: Auth) {
    this.searchService = searchService;

    // TODO: Move to be global
    signInAnonymously(getAuth())
    .then(() => {
      console.log("Signed in anonymously");
      // Signed in..
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      console.log("Failed to sign in anonymously with error code ", errorCode, "and message ", errorMessage);
      // ...
    });
  }

  ngOnInit(): void {
  }

  onKey(event: KeyboardEvent): void {
    this.results = this.searchService.query((<HTMLInputElement>event.target).value);
    console.log("onKey ", this.results);
  }

  onClear(event: MouseEvent): void {
    this.searchElement.nativeElement.value = "";
    this.searchElement.nativeElement.focus();
  }

  onResult(event: MouseEvent, result: string): void {
    console.log("onResult ", result);
  }
}
