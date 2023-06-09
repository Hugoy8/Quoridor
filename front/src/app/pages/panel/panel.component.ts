import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/auth.service';
import { Router } from '@angular/router';
import { UserService } from 'src/app/user.service';

@Component({
  selector: 'app-panel',
  templateUrl: './panel.component.html',
  styleUrls: ['./panel.component.css']
})
export class PanelComponent implements OnInit {
  user: any;
  gameHistory!: any[];
  purchaseHistory: any;

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

        this.userService.getPurchaseHistory(userId).subscribe(
          (data) => {
            this.purchaseHistory = data;
          },
          (error) => {
            console.error('Erreur lors de la récupération de l\'historique des achats :', error);
          }
        );

        this.userService.getGameHistory(userId).subscribe(
          (data) => {
            this.gameHistory = data;
          },
          (error) => {
            console.error('Erreur lors de la récupération de l\'historique des parties :', error);
          }
        );
      }
    }
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/']);
  }

  displayInventoryPurchases: boolean = true;
  displayGameHistory: boolean = false;

  panelSwitch() {
    this.displayInventoryPurchases = !this.displayInventoryPurchases;
    this.displayGameHistory = !this.displayGameHistory;
  }
}