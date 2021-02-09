import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SecurityCardComponent } from './security-card.component';

describe('SecurityCardComponent', () => {
  let component: SecurityCardComponent;
  let fixture: ComponentFixture<SecurityCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SecurityCardComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SecurityCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
