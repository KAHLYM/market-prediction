import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SentimentService } from 'src/app/services/sentiment.service';

import { DummyComponent } from './dummy.component';

describe('DummyComponent', () => {
  let component: DummyComponent;
  let fixture: ComponentFixture<DummyComponent>;

  beforeEach(async () => {
    let mockSentimentService: jasmine.SpyObj<SentimentService> = jasmine.createSpyObj("SentimentService", ["getSubredditSentiments"]);
    mockSentimentService.getSubredditSentiments.and.returnValue(Promise.resolve([]));

    await TestBed.configureTestingModule({
      declarations: [ DummyComponent ],
      providers: [
        { provide: SentimentService, useValue: mockSentimentService },
      ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DummyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
