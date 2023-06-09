import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import AOS from 'aos';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'quoridor-new';

  constructor(private router: Router) { }

  ngOnInit() {
    this.router.events.subscribe((evt) => {
      if (!(evt instanceof NavigationEnd)) {
        return;
      }
      this.scrollToTop()
    });
    AOS.init();
  }

  scrollToTop() {
    window.scrollTo(0, 0);
  }
}
