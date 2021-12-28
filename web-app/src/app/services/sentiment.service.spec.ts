import { TestBed } from '@angular/core/testing';
import { Firestore } from '@angular/fire/firestore';
import { BehaviorSubject } from 'rxjs';

import { SentimentService } from './sentiment.service';

describe('SentimentService', () => {
  let service: SentimentService;

  const FirestoreStub = {
    collection: (name: string) => ({
      doc: (_id: string) => ({
        valueChanges: () => new BehaviorSubject({ foo: 'bar' }),
        set: (_d: any) => new Promise<void>((resolve, _reject) => resolve()),
      }),
    }),
  };

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
