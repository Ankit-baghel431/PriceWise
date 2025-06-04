import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router, RouterModule, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../service/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  imports: [ReactiveFormsModule, CommonModule, RouterModule],
  standalone: true
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  error: string = '';
  isSubmitting: boolean = false;
  successMessage: string = '';

  constructor(
    private fb: FormBuilder, 
    private router: Router, 
    private authService: AuthService,
    private route: ActivatedRoute
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]]
    });
  }

  ngOnInit() {
    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Check for success message from registration
    this.route.queryParams.subscribe(params => {
      if (params['message']) {
        this.successMessage = params['message'];
        // Pre-fill email if provided
        if (params['email']) {
          this.loginForm.patchValue({ email: params['email'] });
        }
        // Clear success message after 5 seconds
        setTimeout(() => {
          this.successMessage = '';
        }, 5000);
      }
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.isSubmitting = true;
      this.error = '';
      
      // Prepare form data
      const formData = {
        email: this.loginForm.value.email.toLowerCase().trim(),
        password: this.loginForm.value.password
      };
      
      this.authService.login(formData).subscribe({
        next: (response) => {
          // Success - redirect to dashboard or intended page
          this.router.navigate(['/dashboard']);
        },
        error: (err) => {
          this.isSubmitting = false;
          this.handleLoginError(err);
        },
        complete: () => {
          this.isSubmitting = false;
        }
      });
    } else {
      // Mark all fields as touched to show validation errors
      this.markAllFieldsAsTouched();
      this.error = 'Please correct all errors before submitting.';
      
      // Scroll to first error
      this.scrollToFirstError();
    }
  }

  private handleLoginError(err: any) {
    if (err.error && typeof err.error === 'object') {
      // Handle specific error responses from backend
      const errorObj = err.error;
      
      if (errorObj.email) {
        this.error = `Email: ${Array.isArray(errorObj.email) ? errorObj.email[0] : errorObj.email}`;
      } else if (errorObj.password) {
        this.error = `Password: ${Array.isArray(errorObj.password) ? errorObj.password[0] : errorObj.password}`;
      } else if (errorObj.non_field_errors) {
        this.error = Array.isArray(errorObj.non_field_errors) ? errorObj.non_field_errors[0] : errorObj.non_field_errors;
      } else if (errorObj.detail) {
        this.error = errorObj.detail;
      } else if (errorObj.message) {
        this.error = errorObj.message;
      } else {
        this.error = 'Invalid email or password. Please try again.';
      }
    } else if (err.message) {
      this.error = err.message;
    } else if (err.status === 401) {
      this.error = 'Invalid email or password. Please check your credentials and try again.';
    } else if (err.status === 0) {
      this.error = 'Unable to connect to the server. Please check your internet connection.';
    } else {
      this.error = 'Login failed. Please try again later.';
    }
  }

  private markAllFieldsAsTouched() {
    Object.keys(this.loginForm.controls).forEach(key => {
      const control = this.loginForm.get(key);
      control?.markAsTouched();
    });
  }

  private scrollToFirstError() {
    setTimeout(() => {
      const firstError = document.querySelector('.error');
      if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 100);
  }

  // Helper method to check if field has error
  hasError(fieldName: string): boolean {
    const field = this.loginForm.get(fieldName);
    return !!(field?.invalid && field?.touched);
  }
}