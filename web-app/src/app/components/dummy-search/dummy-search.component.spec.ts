import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SearchService } from 'src/app/services/search.service';

import { DummySearchComponent } from './dummy-search.component';

describe('DummySearchComponent', () => {
  let component: DummySearchComponent;
  let fixture: ComponentFixture<DummySearchComponent>;

  beforeEach(async () => {
    let mockSearchService: jasmine.SpyObj<SearchService> = jasmine.createSpyObj("SearchService", ["query"]);
    mockSearchService.query.and.returnValue(true);

    await TestBed.configureTestingModule({
      declarations: [ DummySearchComponent ],
      providers: [
        { provide: SearchService, useValue: mockSearchService },
      ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DummySearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
