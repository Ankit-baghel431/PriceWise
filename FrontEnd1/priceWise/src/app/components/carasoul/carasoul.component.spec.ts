import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CarasoulComponent } from './carasoul.component';

describe('CarasoulComponent', () => {
  let component: CarasoulComponent;
  let fixture: ComponentFixture<CarasoulComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CarasoulComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CarasoulComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
