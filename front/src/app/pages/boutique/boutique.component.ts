import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/auth.service';
import { Router } from '@angular/router';
import { UserService } from 'src/app/user.service';

@Component({
  selector: 'app-boutique',
  templateUrl: './boutique.component.html',
  styleUrls: ['./boutique.component.css']
})
export class BoutiqueComponent implements OnInit {
  user: any;

  Electricity: boolean = false;
  Ice: boolean = false;
  Sugar: boolean = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private userService: UserService
  ) { }

  ngOnInit() {
      if (!this.authService.isAuthenticated()) {
          this.router.navigate(['/']);
      } else {
          const userId = this.authService.getUserId();
          if (userId !== null) {
              this.userService.getAuthUserProfile(userId).subscribe(
                  (data) => {
                      this.user = data;
                      const userMaps = data.maps.split(',').map((map: string) => map.trim());
                      this.Electricity = userMaps.includes('Electricity');
                      this.Ice = userMaps.includes('Ice');
                      this.Sugar = userMaps.includes('Sugar');
                  },
                  (error) => {
                      console.error('Erreur lors de la récupération du profil de l\'utilisateur :', error);
                  }
              );
          }
      }
  }

  displayError: boolean = false;
  displayGood: boolean = false;

  buyMap(mapName: string): void {
      const userId = this.authService.getUserId();
      if (!userId) {
          this.router.navigate(['/']);
          return;
      }

      this.userService.buyMap(userId, mapName).subscribe(res => {
          // Actualisez le solde du joueur
          this.userService.getUserProfile(userId);
          switch (mapName) {
              case 'Electricity':
                  this.Electricity = true;
                  break;
              case 'Ice':
                  this.Ice = true;
                  break;
              case 'Sugar':
                  this.Sugar = true;
                  break;
          }
          this.displayGood = true;
      }, err => {
          // Affichez l'erreur
          this.displayError = true;
      });
  }

}
