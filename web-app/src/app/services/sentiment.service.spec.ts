import { TestBed } from '@angular/core/testing';
import { Firestore } from '@angular/fire/firestore';
import { FirestoreStub } from './firestore-stub';

import { SentimentService } from './sentiment.service';

describe('SentimentService', () => {
  let service: SentimentService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        { provide: Firestore, useValue: FirestoreStub }
      ]
    });
    service = TestBed.inject(SentimentService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
