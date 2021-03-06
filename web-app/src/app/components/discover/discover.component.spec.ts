import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { SearchService } from 'src/app/services/search.service';

import { DiscoverComponent, Result} from './discover.component';

describe('DiscoverComponent', () => {
  let component: DiscoverComponent;
  let fixture: ComponentFixture<DiscoverComponent>;

  let injectedSearchService: SearchService;
  
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DiscoverComponent ],
      providers: [{ provider: SearchService, useValue: injectedSearchService }]
    })
    .compileComponents();

    injectedSearchService = TestBed.get(SearchService);
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DiscoverComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  function getTestResult(currency: string = 'TestCurrency', description: string = 'TestDescription', name: string = 'TestName', ticker: string = 'TestTicker'): Result {
    return {
      currency: currency,
      description: description,
      name: name,
      ticker: ticker
    };
  }

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('onSearchClear', () => {
    it('should set searchValue to an empty string', () => {
      component.searchValue = 'DummyInput';
      component.onSearchClear();
      expect(component.searchValue).toEqual('');
    });

    it('should set results to an empty array', () => {
      component.results = [getTestResult()];
      component.onSearchClear();
      expect(component.results).toEqual([]);
    });

    it('should focus on input', () => {
      spyOn(component.searchInput.nativeElement, 'focus');
      component.onSearchClear();
      expect(component.searchInput.nativeElement.focus).toBeTruthy();
    });
  });

  describe('onSearchFocus', () => {
    it('should set searchFocused to be true', () => {
      component.searchFocused = false;
      component.onSearchFocus();
      expect(component.searchFocused).toEqual(true);
    });
  });

  describe('onSearchKeyUp', () => {
    it('should only search if atleast three characters', () => {
      spyOn(injectedSearchService, 'search').and.returnValue([['TestTicker', 'TestName']]);
      
      component.searchValue = '12';
      component.onSearchKeyUp();
      expect(injectedSearchService.search).not.toHaveBeenCalled();
      expect(component.results).toEqual([]);

      component.searchValue = '123';
      component.onSearchKeyUp();
      expect(injectedSearchService.search).toHaveBeenCalled();
      expect(component.results).toEqual([{currency: '$', description: '', ticker: 'TestTicker', name: 'TestName'}]);
    });

    it('should clear existing results', () => {
      component.results = [getTestResult()];
      component.onSearchKeyUp();
      expect(component.results).toEqual([]);
    })
  });

  describe('onResultClick', () => {
    it('should set searchFocused to an false', () => {
      component.searchFocused = true;
      component.onResultClick(getTestResult());
      expect(component.searchFocused).toEqual(false);
    });

    it('should set searchValue to be an empty string', () => {
      component.searchValue = 'DummyInput';
      component.onResultClick(getTestResult());
      expect(component.searchValue).toEqual('');
    });

    it('should set results to an empty array', () => {
      component.results = [getTestResult()];
      component.onResultClick(getTestResult());
      expect(component.results).toEqual([]);
    });

    it('should set company to be the parameter result', () => {
      const result: Result = getTestResult();
      expect(component.company).not.toEqual(result);
      component.onResultClick(result);
      expect(component.company).toEqual(result);
    });
  });

  describe('discover-results', () => {
    it('should show if searchFocused', () => {
      component.searchFocused = false;
      fixture.detectChanges();
      expect(fixture.debugElement.query(By.css('.discover-results'))).toBeNull();

      component.searchFocused = true;
      fixture.detectChanges();
      expect(fixture.debugElement.query(By.css('.discover-results'))).not.toBeNull();
    });

    it('should display correctly formatted upper text', () => {
      component.searchFocused = true;
      const result: Result = getTestResult();
      component.results = [result];
      const expectedString: String = result.name;
      fixture.detectChanges();
      expect(fixture.debugElement.query(By.css('.discover-results > .result > .result-right > .upper')).nativeElement.textContent).toContain(expectedString);
    });

    it('should display correctly formatted lower text', () => {
      component.searchFocused = true;
      const result: Result = getTestResult();
      component.results = [result];
      const expectedString: String = result.currency + result.ticker + ' · ' + result.description;
      fixture.detectChanges();
      expect(fixture.debugElement.query(By.css('.discover-results > .result > .result-right > .lower')).nativeElement.textContent).toContain(expectedString);
    });

    it('should be able to display more than one result', () => {
      component.searchFocused = true;
      component.results = [getTestResult(), getTestResult()];
      fixture.detectChanges();
      const resultCount: number = fixture.debugElement.queryAll(By.css('.discover-results > .result')).length;
      expect(resultCount).toBe(component.results.length);
    });
  });

  describe('company', () => {
    it('should not show if searchFocused', () => {
      component.searchFocused = false;
      fixture.detectChanges();
      expect(fixture.debugElement.query(By.css('.company'))).not.toBeNull();

      component.searchFocused = true;
      fixture.detectChanges();
      expect(fixture.debugElement.query(By.css('.company'))).toBeNull();
    });

    it('should display correctly formatted upper text', () => {
      component.searchFocused = false;
      const company: Result = getTestResult();
      component.company = company;
      const expectedString: String = company.name;
      fixture.detectChanges();
      expect(fixture.debugElement.query(By.css('.company > .company-header > div:nth-child(2) > .upper')).nativeElement.textContent).toContain(expectedString);
    });

    it('should display correctly formatted lower text', () => {
      component.searchFocused = false;
      const company: Result = getTestResult();
      component.company = company;
      const expectedString: String = company.currency + company.ticker + ' · ' + company.description;
      fixture.detectChanges();
      expect(fixture.debugElement.query(By.css('.company > .company-header > div:nth-child(3) > .lower')).nativeElement.textContent).toContain(expectedString);
    });
  });
});
