import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  authenticated: boolean = false;

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit() {
    this.authenticated = this.authService.isAuthenticated();
  }

  authOrPanel() {
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/panel']);
      this.authenticated = true;
    } else {
      this.router.navigate(['/auth']);
      this.authenticated = false;
    };
  }

  menuState: boolean = false;

  openMenu() {
    this.menuState = true;
  }

  closeMenu() {
    this.menuState = false;
  }
}