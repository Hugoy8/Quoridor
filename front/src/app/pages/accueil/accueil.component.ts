import { Component } from '@angular/core';

@Component({
  selector: 'app-accueil',
  templateUrl: './accueil.component.html',
  styleUrls: ['./accueil.component.css']
})
export class AccueilComponent {

  scrollToCategories(): void {
    const categoriesElement = document.getElementById('axes-section');
    if (categoriesElement) {
      categoriesElement.scrollIntoView({ behavior: 'smooth' });
    }
  }

}
