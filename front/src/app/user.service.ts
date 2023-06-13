import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'https://quoridor-api.onrender.com/api';

  constructor(private http: HttpClient) { }

  getUserProfile(userId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/profil/${userId}`);
  }

  getAuthUserProfile(userId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/profile/${userId}`);
  }

  getGameHistory(userId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/game-history/${userId}`);
  }

  getPurchaseHistory(userId: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/purchase-history/${userId}`);
  }

  buyMap(userId: number, mapName: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/purchase-map`, { userId, mapName });
  }

}
