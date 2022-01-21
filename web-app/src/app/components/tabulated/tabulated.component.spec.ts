import {ComponentFixture, TestBed} from '@angular/core/testing';

import {TabulatedComponent} from './tabulated.component';

describe('TabulatedComponent', () => {
  let component: TabulatedComponent;
  let fixture: ComponentFixture<TabulatedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TabulatedComponent],
    })
        .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TabulatedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
