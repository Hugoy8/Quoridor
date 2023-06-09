import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ProfileService } from 'src/app/profile.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  profile: any;

  constructor(private route: ActivatedRoute, private profileService: ProfileService) {}

  ngOnInit() {
    const userId = this.route.snapshot.params['id'];
    this.profileService.getProfile(userId).subscribe(
      (profile) => {
        this.profile = profile;
      },
      (error) => {
        console.error('Erreur lors de la récupération du profil utilisateur :', error);
      }
    );
  }
}
