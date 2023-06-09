import { Component, OnInit } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthService } from 'src/app/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-authentification',
  templateUrl: './authentification.component.html',
  styleUrls: ['./authentification.component.css']
})
export class AuthentificationComponent implements OnInit {
  inscriptionForm!: FormGroup;
  loginForm!: FormGroup;

  inscription = false;
  login = true;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.inscriptionForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      confirmPassword: ['', Validators.required]
    });

    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  switchTo(category: any) {
    if (category == 'inscription') {
      this.inscription = true;
      this.login = false;
    } else if (category == 'login') {
      this.login = true;
      this.inscription = false;
    }
  }

  badResponse: boolean = false;
  goodResponse: boolean = false;

  onInscription() {
    this.badResponse = false;

    if (this.inscriptionForm!.valid) {
      const { username, password, confirmPassword } = this.inscriptionForm!.value;
  
      // Vérifiez que les deux mots de passe sont identiques
      if (password !== confirmPassword) {
        this.badResponse = true;
        this.goodResponse = false;
      }
  
      this.authService.signup(username, password, confirmPassword).subscribe(
        (response) => {

          this.badResponse = false;
  
          // Appel à la méthode login pour se connecter directement après l'inscription
          this.authService.login(username, password).subscribe(
            (loginResponse) => {
              this.goodResponse = true;
              setTimeout(() => {
                this.router.navigateByUrl('/');
              }, 1500);
            },
            (loginError) => {
              this.badResponse = true;
              this.goodResponse = false;
            }
          );
        },
        (error) => {
          this.badResponse = true;
          this.goodResponse = false;
        }
      );      
    }
  }
  
  onLogin() {
    this.badResponse = false;

    if (this.loginForm!.valid) {
      const { username, password } = this.loginForm!.value;
  
      this.authService.login(username, password).subscribe(
        (response) => {
          this.goodResponse = true;
          setTimeout(() => {
            this.router.navigateByUrl('/');
          }, 1500);
        },
        (error) => {
          this.badResponse = true;
          this.goodResponse = false;
        }
      );
    }
  }
  

}  
