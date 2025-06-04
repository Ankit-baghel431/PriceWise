import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-carasoul',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './carasoul.component.html',
  styleUrl: './carasoul.component.css'
})
export class CarasoulComponent implements OnInit {
    carouselItems = [
    {
      id: 1,
      title: 'Fashion Flash Sales',
      description: 'Top brands, incredible discounts, limited time only',
      image: 'https://storage.pixteller.com/designs/designs-images/2020-12-21/04/gym-fashion-final-sale-banner-1-5fe0b6ef9d952.png',
      color: '#f3e8ff'
    },
    {
      id: 2,
      title: 'Discover Amazing Tech Deals',
      description: 'Find the latest gadgets at unbeatable prices',
      image: 'https://i.pcmag.com/imagery/articles/00JPvvhfkY1XHmRFByCAqok-6..v1737141667.jpg',
      color: '#dbeafe'
    },
    {
      id: 3,
      title: 'Home & Kitchen Essentials',
      description: 'Transform your space with the best deals on home products',
      image: 'https://www.mealime.com/images/kitchen.jpg',
      color: '#fef3c7'
    }
  ];

  currentSlide = 0;
  intervalId: any;

  ngOnInit(): void {
    this.intervalId = setInterval(() => {
      this.nextSlide();
    }, 5000);
  }

  ngOnDestroy(): void {
    clearInterval(this.intervalId);
  }

  nextSlide(): void {
    this.currentSlide = (this.currentSlide + 1) % this.carouselItems.length;
  }

  prevSlide(): void {
    this.currentSlide =
      (this.currentSlide - 1 + this.carouselItems.length) % this.carouselItems.length;
  }

  goToSlide(index: number): void {
    this.currentSlide = index;
  }
}
