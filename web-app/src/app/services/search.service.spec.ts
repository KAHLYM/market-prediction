import {TestBed} from '@angular/core/testing';
import {Firestore} from '@angular/fire/firestore';
import {FirestoreStub} from './firestore-stub';

import {SearchService} from './search.service';

describe('SearchService', () => {
  // let service: SearchService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: Firestore, useValue: FirestoreStub},
      ],
    });
    // service = TestBed.inject(SearchService);
  });

// FIXME
// Error: Either AngularFireModule has not been provided in your AppModule (this can be done manually or implictly using
// provideFirebaseApp) or you're calling an AngularFire method outside of an NgModule (which is not supported).
//   it('should be created', () => {
//     expect(service).toBeTruthy();
//   });
});
