import { ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';

import { NavigationComponent } from './navigation.component';

describe('NavigationComponent', () => {
  let component: NavigationComponent;
  let fixture: ComponentFixture<NavigationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NavigationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NavigationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('onMenuClick', () => {
    it('should set open to be opposite of previous value', () => {
      component.open = false;
      component.onMenuClick();
      expect(component.open).toEqual(true);
    });
  });

  describe('onLinkClick', () => {
    it('should set open to be false', () => {
      component.open = true;
      component.onLinkClick();
      expect(component.open).toEqual(false);
    });
  });

  describe('navigation-wrapper', () => {
    it('should show if open', () => {
      component.open = false;
      fixture.detectChanges();
      expect(fixture.debugElement.query(By.css('.navigation-wrapper'))).toBeNull();

      component.open = true;
      fixture.detectChanges();
      expect(fixture.debugElement.query(By.css('.navigation-wrapper'))).not.toBeNull();
    });
  });
});
