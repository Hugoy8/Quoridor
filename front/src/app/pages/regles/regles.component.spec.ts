import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReglesComponent } from './regles.component';

describe('ReglesComponent', () => {
  let component: ReglesComponent;
  let fixture: ComponentFixture<ReglesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ReglesComponent]
    });
    fixture = TestBed.createComponent(ReglesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
