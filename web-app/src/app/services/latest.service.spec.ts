import {TestBed} from '@angular/core/testing';
import {Firestore} from '@angular/fire/firestore';
import {FirestoreStub} from './firestore-stub';

import {LatestService} from './latest.service';

describe('LatestService', () => {
  let service: LatestService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: Firestore, useValue: FirestoreStub},
      ],
    });
    service = TestBed.inject(LatestService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
