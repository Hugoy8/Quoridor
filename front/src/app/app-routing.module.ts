import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AccueilComponent } from './pages/accueil/accueil.component';
import { ReglesComponent } from './pages/regles/regles.component';
import { EquipeComponent } from './pages/equipe/equipe.component';
import { ContactComponent } from './pages/contact/contact.component';
import { DownloadComponent } from './pages/download/download.component';
import { ClassementComponent } from './pages/classement/classement.component';
import { ProfileComponent } from './pages/profile/profile.component';
import { AuthentificationComponent } from './pages/authentification/authentification.component';
import { PanelComponent } from './pages/panel/panel.component';
import { BoutiqueComponent } from './pages/boutique/boutique.component';

const routes: Routes = [
  { path: '', component: AccueilComponent },
  { path: 'regles', component: ReglesComponent },
  { path: 'equipe', component: EquipeComponent },
  { path: 'contact', component: ContactComponent},
  { path: 'download', component: DownloadComponent},
  { path: 'classement', component: ClassementComponent},
  { path: 'profil/:id', component: ProfileComponent },
  { path: 'auth', component: AuthentificationComponent },
  { path: 'panel', component: PanelComponent },
  { path: 'boutique', component: BoutiqueComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
