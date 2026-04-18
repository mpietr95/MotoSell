import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  username = '';
  password = '';
  password2 = '';
  email = '';
  error = '';
  success = '';

  constructor(private http: HttpClient, private router: Router) { }

  onSubmit() {
    if (this.password !== this.password2) {
      this.error = 'Hasła nie są identyczne.';
      return;
    }

    this.http.post(`${environment.apiUrl}/api/rejestracja/`, {
      username: this.username,
      password: this.password,
      email: this.email,
    }).subscribe({
      next: () => {
        this.success = 'Konto zostało utworzone. Możesz się teraz zalogować.';
        this.error = '';
        setTimeout(() => this.router.navigate(['/logowanie']), 2000);
      },
      error: (err) => {
        this.error = err.error?.detail || 'Wystąpił błąd rejestracji.';
      }
    });
  }
}
