import { Component, inject, OnInit } from '@angular/core';
import { ProductServiceService } from '../../service/product-service.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

interface Product {
  title: string;
  price: number;
  rating: number;
  image: string;
  link: string;
  seller?: string;
  source?: string;
}

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  productService = inject(ProductServiceService);
  searchText: string = '';
  resultsBySource: { [source: string]: Product[] } = {};
  loading = false;
  error = '';

  objectKeys = Object.keys; // to use Object.keys in template

  fetchData() {
    if (!this.searchText.trim()) {
      alert('Please enter a search term');
      return;
    }

    this.loading = true;
    this.error = '';
    this.resultsBySource = {};

    this.productService.getProducts(this.searchText).subscribe({
      next: (res: any) => {
        this.loading = false;
        this.resultsBySource = res.results_by_source || {};
        if (Object.keys(this.resultsBySource).length === 0) {
          this.error = 'No results found.';
        }
      },
      error: (err) => {
        this.loading = false;
        this.error = 'Error fetching data.';
        console.error(err);
      }
    });
  }

  ngOnInit(): void {}
}
