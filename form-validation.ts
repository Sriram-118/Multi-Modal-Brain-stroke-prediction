/**
 * Enhanced Form Validation for Authentication Forms
 * Provides real-time validation with visual feedback and accessibility support
 */

import { ValidationState, ValidationRule, ValidationResult } from '../types';

export class AuthFormValidator {
  private form: HTMLFormElement;
  private validationState: ValidationState;
  private validationRules: Map<string, ValidationRule[]>;
  private submitButton: HTMLButtonElement | null;

  constructor(formSelector: string) {
    const form = document.querySelector(formSelector) as HTMLFormElement;
    if (!form) {
      throw new Error(`Form not found: ${formSelector}`);
    }

    this.form = form;
    this.validationState = {
      isValid: false,
      errors: new Map(),
      touched: new Set(),
      submitted: false
    };
    this.validationRules = new Map();
    this.submitButton = form.querySelector('button[type="submit"]') as HTMLButtonElement;

    this.init();
  }

  private init(): void {
    this.setupValidationRules();
    this.setupEventListeners();
    this.setupAccessibility();
  }

  private setupValidationRules(): void {
    // Username validation rules
    this.validationRules.set('t1', [
      {
        required: true,
        custom: (value: string) => {
          if (!value || value.length < 3) {
            return { isValid: false, message: 'Username must be at least 3 characters long' };
          }
          if (!/^[a-zA-Z0-9_]+$/.test(value)) {
            return { isValid: false, message: 'Username can only contain letters, numbers, and underscores' };
          }
          return { isValid: true };
        }
      }
    ]);

    // Password validation rules
    this.validationRules.set('t2', [
      {
        required: true,
        min: 6,
        custom: (value: string) => {
          if (!value || value.length < 6) {
            return { isValid: false, message: 'Password must be at least 6 characters long' };
          }
          return { isValid: true };
        }
      }
    ]);
  }

  private setupEventListeners(): void {
    // Form submission
    this.form.addEventListener('submit', (e) => this.handleSubmit(e));

    // Field validation
    const inputs = this.form.querySelectorAll('input[name]') as NodeListOf<HTMLInputElement>;
    inputs.forEach(input => {
      input.addEventListener('blur', () => this.validateField(input));
      input.addEventListener('input', () => this.handleInput(input));
      input.addEventListener('focus', () => this.handleFocus(input));
    });

    // Real-time form state updates
    this.form.addEventListener('input', () => this.updateFormState());
  }

  private setupAccessibility(): void {
    // Add ARIA attributes
    const inputs = this.form.querySelectorAll('input[name]') as NodeListOf<HTMLInputElement>;
    inputs.forEach(input => {
      input.setAttribute('aria-describedby', `${input.name}-feedback`);
      
      // Create feedback element if it doesn't exist
      let feedback = document.getElementById(`${input.name}-feedback`);
      if (!feedback) {
        feedback = document.createElement('div');
        feedback.id = `${input.name}-feedback`;
        feedback.className = 'invalid-feedback';
        feedback.setAttribute('role', 'alert');
        feedback.setAttribute('aria-live', 'polite');
        input.parentNode?.appendChild(feedback);
      }
    });
  }

  private handleSubmit(event: Event): void {
    event.preventDefault();
    this.validationState.submitted = true;

    // Validate all fields
    const inputs = this.form.querySelectorAll('input[name]') as NodeListOf<HTMLInputElement>;
    let isFormValid = true;

    inputs.forEach(input => {
      const isFieldValid = this.validateField(input);
      if (!isFieldValid) {
        isFormValid = false;
      }
    });

    if (isFormValid) {
      this.handleValidSubmission();
    } else {
      this.handleInvalidSubmission();
    }
  }

  private handleInput(input: HTMLInputElement): void {
    // Only validate if field has been touched or form has been submitted
    if (this.validationState.touched.has(input.name) || this.validationState.submitted) {
      this.validateField(input);
    }
  }

  private handleFocus(input: HTMLInputElement): void {
    // Clear error state on focus
    this.clearFieldError(input);
  }

  private validateField(input: HTMLInputElement): boolean {
    const fieldName = input.name;
    const value = input.value.trim();
    
    this.validationState.touched.add(fieldName);

    // Get validation rules for this field
    const rules = this.validationRules.get(fieldName) || [];
    
    // Clear previous errors
    this.validationState.errors.delete(fieldName);
    this.clearFieldError(input);

    // Apply validation rules
    for (const rule of rules) {
      const result = this.applyValidationRule(value, rule);
      if (!result.isValid) {
        this.validationState.errors.set(fieldName, result.message || 'Invalid input');
        this.showFieldError(input, result.message || 'Invalid input');
        return false;
      }
    }

    // Field is valid
    this.showFieldSuccess(input);
    return true;
  }

  private applyValidationRule(value: string, rule: ValidationRule): ValidationResult {
    // Required validation
    if (rule.required && (!value || value.length === 0)) {
      return { isValid: false, message: 'This field is required' };
    }

    // Skip other validations if field is empty and not required
    if (!value && !rule.required) {
      return { isValid: true };
    }

    // Min length validation
    if (rule.min && value.length < rule.min) {
      return { isValid: false, message: `Must be at least ${rule.min} characters long` };
    }

    // Max length validation
    if (rule.max && value.length > rule.max) {
      return { isValid: false, message: `Must be no more than ${rule.max} characters long` };
    }

    // Pattern validation
    if (rule.pattern && !rule.pattern.test(value)) {
      return { isValid: false, message: 'Invalid format' };
    }

    // Custom validation
    if (rule.custom) {
      return rule.custom(value);
    }

    return { isValid: true };
  }

  private showFieldError(input: HTMLInputElement, message: string): void {
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
    input.setAttribute('aria-invalid', 'true');

    const feedback = document.getElementById(`${input.name}-feedback`);
    if (feedback) {
      feedback.textContent = message;
      feedback.style.display = 'block';
    }

    // Announce error to screen readers
    this.announceToScreenReader(`Error in ${this.getFieldLabel(input)}: ${message}`);
  }

  private showFieldSuccess(input: HTMLInputElement): void {
    input.classList.add('is-valid');
    input.classList.remove('is-invalid');
    input.setAttribute('aria-invalid', 'false');

    const feedback = document.getElementById(`${input.name}-feedback`);
    if (feedback) {
      feedback.style.display = 'none';
    }
  }

  private clearFieldError(input: HTMLInputElement): void {
    input.classList.remove('is-invalid', 'is-valid');
    input.removeAttribute('aria-invalid');

    const feedback = document.getElementById(`${input.name}-feedback`);
    if (feedback) {
      feedback.style.display = 'none';
    }
  }

  private getFieldLabel(input: HTMLInputElement): string {
    const label = this.form.querySelector(`label[for="${input.id}"]`) as HTMLLabelElement;
    if (label) {
      return label.textContent?.replace(/[*:]/g, '').trim() || input.name;
    }
    
    // Fallback to field name mapping
    const fieldLabels: Record<string, string> = {
      't1': 'Username',
      't2': 'Password'
    };
    
    return fieldLabels[input.name] || input.name;
  }

  private updateFormState(): void {
    const hasErrors = this.validationState.errors.size > 0;
    const allFieldsTouched = this.form.querySelectorAll('input[required]').length === this.validationState.touched.size;
    
    this.validationState.isValid = !hasErrors && allFieldsTouched;
    
    // Update submit button state
    if (this.submitButton) {
      this.submitButton.disabled = !this.validationState.isValid && this.validationState.submitted;
    }
  }

  private handleValidSubmission(): void {
    if (!this.submitButton) return;

    // Show loading state
    const originalText = this.submitButton.innerHTML;
    this.submitButton.disabled = true;
    this.submitButton.innerHTML = `
      <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
      Signing In...
    `;

    // Add loading class to form
    this.form.classList.add('form-loading');

    // Announce to screen readers
    this.announceToScreenReader('Form is being submitted, please wait...');

    // Submit form after brief delay for UX
    setTimeout(() => {
      this.form.submit();
    }, 500);

    // Fallback to restore button state
    setTimeout(() => {
      this.submitButton!.disabled = false;
      this.submitButton!.innerHTML = originalText;
      this.form.classList.remove('form-loading');
    }, 10000);
  }

  private handleInvalidSubmission(): void {
    // Focus first invalid field
    const firstInvalidField = this.form.querySelector('.is-invalid') as HTMLInputElement;
    if (firstInvalidField) {
      firstInvalidField.focus();
      
      // Scroll to field if needed
      firstInvalidField.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'center' 
      });
    }

    // Announce error to screen readers
    const errorCount = this.validationState.errors.size;
    this.announceToScreenReader(`Form has ${errorCount} error${errorCount !== 1 ? 's' : ''}. Please correct and try again.`);
  }

  private announceToScreenReader(message: string): void {
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'assertive');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    // Remove after announcement
    setTimeout(() => {
      document.body.removeChild(announcement);
    }, 1000);
  }

  // Public methods
  public addValidationRule(fieldName: string, rule: ValidationRule): void {
    const existingRules = this.validationRules.get(fieldName) || [];
    existingRules.push(rule);
    this.validationRules.set(fieldName, existingRules);
  }

  public validateForm(): boolean {
    const inputs = this.form.querySelectorAll('input[name]') as NodeListOf<HTMLInputElement>;
    let isValid = true;

    inputs.forEach(input => {
      if (!this.validateField(input)) {
        isValid = false;
      }
    });

    return isValid;
  }

  public getValidationState(): ValidationState {
    return { ...this.validationState };
  }

  public reset(): void {
    this.validationState = {
      isValid: false,
      errors: new Map(),
      touched: new Set(),
      submitted: false
    };

    // Clear all field states
    const inputs = this.form.querySelectorAll('input[name]') as NodeListOf<HTMLInputElement>;
    inputs.forEach(input => {
      this.clearFieldError(input);
    });

    // Reset form
    this.form.reset();
  }
}

/**
 * Password Strength Validator
 * Provides password strength assessment and visual feedback
 */
export class PasswordStrengthValidator {
  private passwordInput: HTMLInputElement;
  private strengthIndicator: HTMLElement | null;
  private strengthText: HTMLElement | null;

  constructor(passwordInputSelector: string) {
    const input = document.querySelector(passwordInputSelector) as HTMLInputElement;
    if (!input) {
      throw new Error(`Password input not found: ${passwordInputSelector}`);
    }

    this.passwordInput = input;
    this.strengthIndicator = null;
    this.strengthText = null;
    
    this.init();
  }

  private init(): void {
    this.createStrengthIndicator();
    this.setupEventListeners();
  }

  private createStrengthIndicator(): void {
    const container = this.passwordInput.parentElement;
    if (!container) return;

    // Create strength indicator container
    const strengthContainer = document.createElement('div');
    strengthContainer.className = 'password-strength mt-2';
    
    // Create strength bar
    this.strengthIndicator = document.createElement('div');
    this.strengthIndicator.className = 'strength-bar';
    this.strengthIndicator.innerHTML = `
      <div class="strength-fill" style="width: 0%; transition: all 0.3s ease;"></div>
    `;
    
    // Create strength text
    this.strengthText = document.createElement('small');
    this.strengthText.className = 'strength-text text-muted';
    this.strengthText.textContent = 'Enter password to see strength';
    
    strengthContainer.appendChild(this.strengthIndicator);
    strengthContainer.appendChild(this.strengthText);
    container.appendChild(strengthContainer);

    // Add CSS styles
    const style = document.createElement('style');
    style.textContent = `
      .strength-bar {
        height: 4px;
        background-color: #e9ecef;
        border-radius: 2px;
        overflow: hidden;
        margin-bottom: 0.5rem;
      }
      .strength-fill {
        height: 100%;
        border-radius: 2px;
        transition: all 0.3s ease;
      }
      .strength-weak { background-color: #dc3545; }
      .strength-fair { background-color: #fd7e14; }
      .strength-good { background-color: #ffc107; }
      .strength-strong { background-color: #28a745; }
    `;
    document.head.appendChild(style);
  }

  private setupEventListeners(): void {
    this.passwordInput.addEventListener('input', () => {
      this.updateStrengthIndicator();
    });
  }

  private updateStrengthIndicator(): void {
    const password = this.passwordInput.value;
    const strength = this.calculatePasswordStrength(password);
    
    if (!this.strengthIndicator || !this.strengthText) return;

    const fill = this.strengthIndicator.querySelector('.strength-fill') as HTMLElement;
    if (!fill) return;

    // Update visual indicator
    fill.style.width = `${strength.percentage}%`;
    fill.className = `strength-fill strength-${strength.level}`;
    
    // Update text
    this.strengthText.textContent = strength.message;
    this.strengthText.className = `strength-text text-${strength.color}`;
  }

  private calculatePasswordStrength(password: string): {
    level: string;
    percentage: number;
    message: string;
    color: string;
  } {
    if (!password) {
      return { level: 'weak', percentage: 0, message: 'Enter password to see strength', color: 'muted' };
    }

    let score = 0;
    const checks = {
      length: password.length >= 8,
      lowercase: /[a-z]/.test(password),
      uppercase: /[A-Z]/.test(password),
      numbers: /\d/.test(password),
      symbols: /[^A-Za-z0-9]/.test(password)
    };

    // Calculate score
    if (checks.length) score += 20;
    if (checks.lowercase) score += 20;
    if (checks.uppercase) score += 20;
    if (checks.numbers) score += 20;
    if (checks.symbols) score += 20;

    // Determine strength level
    if (score < 40) {
      return { level: 'weak', percentage: score, message: 'Weak password', color: 'danger' };
    } else if (score < 60) {
      return { level: 'fair', percentage: score, message: 'Fair password', color: 'warning' };
    } else if (score < 80) {
      return { level: 'good', percentage: score, message: 'Good password', color: 'info' };
    } else {
      return { level: 'strong', percentage: score, message: 'Strong password', color: 'success' };
    }
  }
}

// Auto-initialize for login forms
document.addEventListener('DOMContentLoaded', () => {
  // Initialize login form validator
  const loginForm = document.querySelector('#loginForm');
  if (loginForm) {
    try {
      window.StrokeApp = window.StrokeApp || {};
      window.StrokeApp.loginValidator = new AuthFormValidator('#loginForm');
    } catch (error) {
      console.warn('Login form validator initialization failed:', error);
    }
  }
});

// Export for global access
declare global {
  interface Window {
    StrokeApp: {
      AuthFormValidator: typeof AuthFormValidator;
      PasswordStrengthValidator: typeof PasswordStrengthValidator;
      [key: string]: any;
    };
  }
}

export { AuthFormValidator, PasswordStrengthValidator };