import { ɵgetComponentViewDefinitionFactory } from '@angular/core';
import { TestBed } from '@angular/core/testing';

import { SearchService } from './search.service';

describe('SearchService', () => {
  let service: SearchService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SearchService);

    service.data = {'TestTicker': 'TestName'};
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('serach', () => {
    it('should be return empty array if no matches', () => {
      const matches: [string, string][] = service.search('no match');
      expect(matches).toEqual([]);
    });

    it('should be case-insensitive', () => {
      const matches: [string, string][] = service.search('ticker');
      expect(matches).toEqual([['TestTicker', 'TestName']]);
    });
  })
});
