import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormControl } from '@angular/forms';

@Component({
  selector: 'app-classement',
  templateUrl: './classement.component.html',
  styleUrls: ['./classement.component.css']
})
export class ClassementComponent implements OnInit {
  searchForm!: FormControl;
  topPlayers: any[] = [];
  defaultPlayers: any[] = [];
  searchPlayersList: any[] = [];


  constructor(private http: HttpClient, private formBuilder: FormBuilder) {}

  ngOnInit() {
    this.searchForm = new FormControl('');

    this.getTopPlayers();
    this.getDefaultPlayers();
  }

  getTopPlayers() {
    this.http.get<any[]>('https://quoridor-api.onrender.com/api/top-players').subscribe(
      (response) => {
        this.topPlayers = response;
      },
      (error) => {
        console.error('Erreur lors de la récupération des meilleurs joueurs :', error);
      }
    );
  }

  getDefaultPlayers() {
    this.http.get<any[]>('https://quoridor-api.onrender.com/api/default-players').subscribe(
      (response) => {
        this.defaultPlayers = response;
      },
      (error) => {
        console.error('Erreur lors de la récupération des joueurs par défaut :', error);
      }
    );
  }

  getMedal(i: number): string {
    if (i === 0) {
      return 'gold';
    } else if (i === 1) {
      return 'argent';
    } else if (i === 2) {
      return 'bronze';
    } else {
      return 'Erreur';
    }
  }

  defaultPlayersDisplay: boolean = true;
  searchPlayersDisplay: boolean = false;
  
  onInputChange() {
      this.defaultPlayersDisplay = false;
      this.searchPlayersDisplay = true;
  };
  
  searchPlayers() {
    this.onInputChange();
    const searchTerm = this.searchForm.value;
    this.http
      .get<any[]>('https://quoridor-api.onrender.com/api/search-players?username=' + searchTerm)
      .subscribe(
        (response) => {
          this.searchPlayersList = response;
        },
        (error) => {
          console.error('Erreur lors de la recherche des joueurs :', error);
        }
      );
  }  
}
