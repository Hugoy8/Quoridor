import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AccueilComponent } from './pages/accueil/accueil.component';
import { ReglesComponent } from './pages/regles/regles.component';
import { EquipeComponent } from './pages/equipe/equipe.component';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { ContactComponent } from './pages/contact/contact.component';
import { DownloadComponent } from './pages/download/download.component';
import { ClassementComponent } from './pages/classement/classement.component';
import { LeadingZeroPipe } from './leading-zero.pipe';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { ProfileComponent } from './pages/profile/profile.component';
import { AuthentificationComponent } from './pages/authentification/authentification.component';
import { PanelComponent } from './pages/panel/panel.component';
import { BoutiqueComponent } from './pages/boutique/boutique.component';

@NgModule({
  declarations: [
    AppComponent,
    AccueilComponent,
    ReglesComponent,
    EquipeComponent,
    HeaderComponent,
    FooterComponent,
    ContactComponent,
    DownloadComponent,
    ClassementComponent,
    LeadingZeroPipe,
    ProfileComponent,
    AuthentificationComponent,
    PanelComponent,
    BoutiqueComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
