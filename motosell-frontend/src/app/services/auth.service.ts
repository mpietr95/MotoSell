import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {

  private tokenUrl = `${environment.apiUrl}/api/token/`;
  private refreshUrl = `${environment.apiUrl}/api/token/refresh/`;

  constructor(private http: HttpClient, private router: Router) { }

  login(username: string, password: string) {
    return this.http.post<{ access: string; refresh: string }>(this.tokenUrl, { username, password }).pipe(
      tap(tokens => {
        localStorage.setItem('access_token', tokens.access);
        localStorage.setItem('refresh_token', tokens.refresh);
      })
    );
  }

  refreshToken() {
    const refresh = this.getRefreshToken();
    return this.http.post<{ access: string; refresh: string }>(this.refreshUrl, { refresh }).pipe(
      tap(tokens => {
        localStorage.setItem('access_token', tokens.access);
      })
    );
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.router.navigate(['/logowanie']);
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}
