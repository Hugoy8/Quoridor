import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import jwt_decode from 'jwt-decode';

// Créez une interface pour le contenu de votre JWT.
interface JwtPayload {
  id: number;
  username: string;
  // Ajoutez ici d'autres champs que vous attendez dans le token.
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'https://quoridor-api.onrender.com/api';

  constructor(private http: HttpClient) {}

  signup(username: string, password: string, confirmPassword: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/signup`, { username, password, confirmPassword });
  }

  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, { username, password }).pipe(
      tap((res: any) => {
        localStorage.setItem('token', res.token);
      })
    );
  }

  isAuthenticated(): boolean {
    return localStorage.getItem('token') !== null;
  }

  logout(): void {
    localStorage.removeItem('token');
  }

  getUserId(): number | null {
    const token = localStorage.getItem('token');
    if (!token) {
      return null;
    }

    const decodedToken = jwt_decode(token) as JwtPayload;
    return decodedToken.id;
  }
}