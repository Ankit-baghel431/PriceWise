// src/app/services/product.service.ts
import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

export interface Product {
  title?: string;
  name?: string;
  image: string;
  link: string;
  price: number;
}

export interface ProductResponse {
  results_by_source: {
    [source: string]: Product[];
  };
}

@Injectable({
  providedIn: 'root'
})
export class ProductServiceService {
  private baseUrl = 'http://127.0.0.1:8000/api/search'; 
  http = inject(HttpClient);

  constructor() {}

  getProducts(query: string): Observable<ProductResponse> {
    const fullUrl = `${this.baseUrl}/?query=${encodeURIComponent(query)}`;
    return this.http.get<ProductResponse>(fullUrl);
  }
}
