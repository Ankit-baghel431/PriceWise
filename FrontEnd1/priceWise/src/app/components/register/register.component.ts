import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../service/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
  imports: [ReactiveFormsModule, CommonModule, RouterModule],
  standalone: true
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup;
  error: string = '';
  isSubmitting: boolean = false;
  showPassword: boolean = false;
  showConfirmPassword: boolean = false;

  constructor(
    private fb: FormBuilder, 
    private router: Router, 
    private authService: AuthService
  ) {
    this.registerForm = this.fb.group({
      username: ['', [
        Validators.required, 
        Validators.minLength(3),
        Validators.maxLength(20),
        Validators.pattern(/^[a-zA-Z0-9_]+$/)
      ]],
      name: ['', [
        Validators.required, 
        Validators.minLength(2),
        Validators.maxLength(50),
        Validators.pattern(/^[a-zA-Z\s]+$/)
      ]],
      email: ['', [
        Validators.required, 
        Validators.email,
        Validators.maxLength(100)
      ]],
      password: ['', [
        Validators.required, 
        Validators.minLength(8),
        this.passwordStrengthValidator
      ]],
      password2: ['', [Validators.required]],
      terms_conditions: [false, [Validators.requiredTrue]]
    }, { 
      validators: this.passwordMatchValidator 
    });
  }

  ngOnInit() {
    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
  }

  // Enhanced password strength validator
  passwordStrengthValidator(control: AbstractControl) {
    const password = control.value;
    if (!password) return null;
    
    const hasNumber = /[0-9]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    const strengthChecks = [hasNumber, hasUpper, hasLower, hasSpecial];
    const passedChecks = strengthChecks.filter(check => check).length;
    
    if (passedChecks < 3) {
      return { passwordStrength: true };
    }
    
    return null;
  }

  // Password match validator
  passwordMatchValidator(form: AbstractControl) {
    const password = form.get('password');
    const password2 = form.get('password2');
    
    if (!password || !password2) return null;
    
    return password.value === password2.value ? null : { passwordMismatch: true };
  }

  // Get comprehensive error messages
  getErrorMessage(fieldName: string): string {
    const field = this.registerForm.get(fieldName);
    if (!field || !field.errors || !field.touched) return '';

    const errors = field.errors;
    
    switch (fieldName) {
      case 'username':
        if (errors['required']) return 'Username is required';
        if (errors['minlength']) return 'Username must be at least 3 characters';
        if (errors['maxlength']) return 'Username cannot exceed 20 characters';
        if (errors['pattern']) return 'Username can only contain letters, numbers, and underscores';
        break;
        
      case 'name':
        if (errors['required']) return 'Full name is required';
        if (errors['minlength']) return 'Name must be at least 2 characters';
        if (errors['maxlength']) return 'Name cannot exceed 50 characters';
        if (errors['pattern']) return 'Name can only contain letters and spaces';
        break;
        
      case 'email':
        if (errors['required']) return 'Email address is required';
        if (errors['email']) return 'Please enter a valid email address';
        if (errors['maxlength']) return 'Email cannot exceed 100 characters';
        break;
        
      case 'password':
        if (errors['required']) return 'Password is required';
        if (errors['minlength']) return 'Password must be at least 8 characters';
        if (errors['passwordStrength']) {
          return 'Password must contain at least 3 of: uppercase, lowercase, number, special character';
        }
        break;
        
      case 'password2':
        if (errors['required']) return 'Please confirm your password';
        break;
        
      case 'terms_conditions':
        if (errors['required']) return 'You must accept the terms and conditions to continue';
        break;
    }
    return '';
  }

  // Check for password mismatch error
  get passwordMismatchError(): string {
    const form = this.registerForm;
    const password2 = form.get('password2');
    
    if (form.errors?.['passwordMismatch'] && password2?.touched) {
      return 'Passwords do not match';
    }
    return '';
  }

  // Get password strength indicator
  getPasswordStrength(): string {
    const password = this.registerForm.get('password')?.value || '';
    if (!password) return '';
    
    const hasNumber = /[0-9]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    const strengthChecks = [hasNumber, hasUpper, hasLower, hasSpecial];
    const passedChecks = strengthChecks.filter(check => check).length;
    
    if (password.length < 6) return 'weak';
    if (passedChecks < 2) return 'weak';
    if (passedChecks < 3) return 'medium';
    return 'strong';
  }

  onSubmit() {
    if (this.registerForm.valid) {
      this.isSubmitting = true;
      this.error = '';
      
      // Prepare form data for API
      const formData = {
        username: this.registerForm.value.username.trim(),
        name: this.registerForm.value.name.trim(),
        email: this.registerForm.value.email.toLowerCase().trim(),
        password: this.registerForm.value.password,
        password2: this.registerForm.value.password2,
        terms_conditions: this.registerForm.value.terms_conditions
      };
      
      this.authService.register(formData).subscribe({
        next: (response) => {
          // Success - redirect to login with success message
          this.router.navigate(['/login'], { 
            queryParams: { 
              message: 'Account created successfully! Please sign in.',
              email: formData.email 
            }
          });
        },
        error: (err) => {
          this.isSubmitting = false;
          this.handleRegistrationError(err);
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

  private handleRegistrationError(err: any) {
    if (err.error && typeof err.error === 'object') {
      // Handle field-specific errors from backend
      const errorObj = err.error;
      
      if (errorObj.username) {
        this.error = `Username: ${Array.isArray(errorObj.username) ? errorObj.username[0] : errorObj.username}`;
      } else if (errorObj.email) {
        this.error = `Email: ${Array.isArray(errorObj.email) ? errorObj.email[0] : errorObj.email}`;
      } else if (errorObj.password) {
        this.error = `Password: ${Array.isArray(errorObj.password) ? errorObj.password[0] : errorObj.password}`;
      } else if (errorObj.password2) {
        this.error = `Password confirmation: ${Array.isArray(errorObj.password2) ? errorObj.password2[0] : errorObj.password2}`;
      } else if (errorObj.non_field_errors) {
        this.error = Array.isArray(errorObj.non_field_errors) ? errorObj.non_field_errors[0] : errorObj.non_field_errors;
      } else if (errorObj.detail) {
        this.error = errorObj.detail;
      } else if (errorObj.message) {
        this.error = errorObj.message;
      } else {
        this.error = 'Registration failed. Please check your information and try again.';
      }
    } else if (err.message) {
      this.error = err.message;
    } else {
      this.error = 'Unable to create account. Please try again later.';
    }
  }

  private markAllFieldsAsTouched() {
    Object.keys(this.registerForm.controls).forEach(key => {
      const control = this.registerForm.get(key);
      control?.markAsTouched();
      
      // Also mark nested controls if any
      if (control?.hasOwnProperty('controls')) {
        const nestedForm = control as FormGroup;
        Object.keys(nestedForm.controls).forEach(nestedKey => {
          nestedForm.get(nestedKey)?.markAsTouched();
        });
      }
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
    const field = this.registerForm.get(fieldName);
    return !!(field?.invalid && field?.touched);
  }

  // Toggle password visibility
  togglePasswordVisibility(field: 'password' | 'confirmPassword') {
    if (field === 'password') {
      this.showPassword = !this.showPassword;
    } else {
      this.showConfirmPassword = !this.showConfirmPassword;
    }
  }
}