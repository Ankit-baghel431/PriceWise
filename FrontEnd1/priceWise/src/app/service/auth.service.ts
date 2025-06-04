import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private baseUrl = 'https://prisewise-authentication-api.onrender.com/user_auth/';

  constructor(private http: HttpClient) {}

  login(data: { email: string; password: string }): Observable<any> {
    return this.http.post(this.baseUrl + 'login/', data);
  }

  register(data: { username: string; name: string; email: string; password: string }): Observable<any> {
    return this.http.post(this.baseUrl + 'register/', data);
  }
} 