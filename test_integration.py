#!/usr/bin/env python3
"""
Integration test script for stroke UI modernization
Tests all templates and user workflows to ensure proper functionality
"""

import os
import sys
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.utils import override_settings
import tempfile
from PIL import Image
import io

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MultimodalStroke.settings')
django.setup()

class StrokeUIIntegrationTest(TestCase):
    """
    Comprehensive integration tests for the modernized stroke prediction UI
    """
    
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create a test image for file upload tests
        self.test_image = self.create_test_image()
    
    def create_test_image(self):
        """Create a test image file for upload testing"""
        # Create a simple test image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)
        
        return SimpleUploadedFile(
            name='test_brain_scan.png',
            content=image_io.getvalue(),
            content_type='image/png'
        )
    
    def test_home_page_rendering(self):
        """Test that the home page renders correctly with modern UI"""
        response = self.client.get(reverse('index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Multi-Modal Stroke Prediction System')
        self.assertContains(response, 'Bootstrap')  # Check for Bootstrap inclusion
        self.assertContains(response, 'modern.css')  # Check for custom CSS
        self.assertContains(response, 'navbar')  # Check for navigation
        
        # Check for modern UI elements
        self.assertContains(response, 'hero-section')
        self.assertContains(response, 'feature-cards')
        self.assertContains(response, 'btn-primary')
    
    def test_login_page_modernization(self):
        """Test that the login page has been properly modernized"""
        response = self.client.get(reverse('UserLogin'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'login-card')
        self.assertContains(response, 'form-floating')
        self.assertContains(response, 'Healthcare Professional Login')
        self.assertContains(response, 'csrf')  # Check CSRF token
        
        # Check for Bootstrap form elements
        self.assertContains(response, 'form-control')
        self.assertContains(response, 'btn-login')
    
    def test_registration_page_modernization(self):
        """Test that the registration page has been properly modernized"""
        response = self.client.get(reverse('Register'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'register-card')
        self.assertContains(response, 'form-floating')
        self.assertContains(response, 'Create Healthcare Account')
        self.assertContains(response, 'csrf')  # Check CSRF token
        
        # Check for enhanced validation elements
        self.assertContains(response, 'password-requirements')
        self.assertContains(response, 'form-progress')
    
    def test_prediction_form_modernization(self):
        """Test that the prediction form has been properly modernized"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('Predict'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'prediction-card')
        self.assertContains(response, 'form-section')
        self.assertContains(response, 'Multi-Modal Stroke Risk Assessment')
        self.assertContains(response, 'csrf')  # Check CSRF token
        
        # Check for file upload area
        self.assertContains(response, 'file-upload-area')
        self.assertContains(response, 'drag and drop')
        
        # Check for form validation elements
        self.assertContains(response, 'form-progress')
        self.assertContains(response, 'range-indicator')
    
    def test_user_authentication_workflow(self):
        """Test complete user authentication workflow"""
        # Test registration
        registration_data = {
            't1': 'newtestuser',
            't2': 'newpass123',
            't3': '1234567890',
            't4': 'newtest@example.com',
            't5': '123 Test Street, Test City'
        }
        
        response = self.client.post(reverse('RegisterAction'), registration_data)
        # Should redirect or show success message
        self.assertIn(response.status_code, [200, 302])
        
        # Test login
        login_data = {
            't1': 'testuser',
            't2': 'testpass123'
        }
        
        response = self.client.post(reverse('UserLoginAction'), login_data)
        # Should redirect to dashboard or show success
        self.assertIn(response.status_code, [200, 302])
    
    def test_prediction_workflow(self):
        """Test complete prediction workflow"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        
        # Test prediction form submission
        prediction_data = {
            't1': 'Male',
            't2': '65',
            't3': '1',  # Has hypertension
            't4': '150.5',  # Glucose level
            't5': '28.5',  # BMI
            't6': 'formerly smoked',
            't7': self.test_image
        }
        
        response = self.client.post(reverse('PredictAction'), prediction_data)
        
        # Should process successfully (200) or redirect to results (302)
        self.assertIn(response.status_code, [200, 302])
        
        # If successful, should not contain error messages
        if response.status_code == 200:
            self.assertNotContains(response, 'error', status_code=200)
    
    def test_responsive_navigation(self):
        """Test that navigation works correctly across different pages"""
        pages_to_test = [
            ('index', {}),
            ('UserLogin', {}),
            ('Register', {}),
        ]
        
        for url_name, kwargs in pages_to_test:
            response = self.client.get(reverse(url_name, kwargs=kwargs))
            
            # Check navigation elements
            self.assertContains(response, 'navbar')
            self.assertContains(response, 'navbar-toggler')  # Mobile menu
            self.assertContains(response, 'navbar-brand')
            
            # Check for active page indication
            self.assertContains(response, 'nav-link')
    
    def test_accessibility_features(self):
        """Test that accessibility features are properly implemented"""
        response = self.client.get(reverse('index'))
        
        # Check for accessibility elements
        self.assertContains(response, 'aria-label')
        self.assertContains(response, 'role=')
        self.assertContains(response, 'Skip to main content')
        
        # Check for proper heading structure
        self.assertContains(response, '<h1')
        self.assertContains(response, 'alt=')  # Image alt text
    
    def test_security_features(self):
        """Test that security features are properly implemented"""
        # Test CSRF protection on forms
        response = self.client.get(reverse('UserLogin'))
        self.assertContains(response, 'csrfmiddlewaretoken')
        
        response = self.client.get(reverse('Register'))
        self.assertContains(response, 'csrfmiddlewaretoken')
        
        # Test that forms require CSRF token
        login_data = {
            't1': 'testuser',
            't2': 'testpass123'
            # Intentionally omitting CSRF token
        }
        
        # This should fail due to missing CSRF token
        response = self.client.post(reverse('UserLoginAction'), login_data)
        self.assertEqual(response.status_code, 403)  # Forbidden due to CSRF
    
    def test_file_upload_security(self):
        """Test file upload security measures"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test with valid image
        valid_data = {
            't1': 'Male',
            't2': '65',
            't3': '1',
            't4': '150.5',
            't5': '28.5',
            't6': 'never smoked',
            't7': self.test_image
        }
        
        response = self.client.post(reverse('PredictAction'), valid_data)
        self.assertIn(response.status_code, [200, 302])
        
        # Test with invalid file type (should be handled by client-side validation)
        # Server-side validation should also reject non-image files
        invalid_file = SimpleUploadedFile(
            name='test.txt',
            content=b'This is not an image',
            content_type='text/plain'
        )
        
        invalid_data = valid_data.copy()
        invalid_data['t7'] = invalid_file
        
        response = self.client.post(reverse('PredictAction'), invalid_data)
        # Should either reject or handle gracefully
        self.assertIn(response.status_code, [200, 400, 302])
    
    def test_form_validation(self):
        """Test client-side and server-side form validation"""
        # Test login form validation
        response = self.client.get(reverse('UserLogin'))
        self.assertContains(response, 'form-validation.js')
        self.assertContains(response, 'required')
        
        # Test registration form validation
        response = self.client.get(reverse('Register'))
        self.assertContains(response, 'password-requirements')
        self.assertContains(response, 'form-progress')
        
        # Test prediction form validation
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('Predict'))
        self.assertContains(response, 'range-indicator')
        self.assertContains(response, 'file-upload.js')
    
    def test_performance_optimizations(self):
        """Test that performance optimizations are in place"""
        response = self.client.get(reverse('index'))
        
        # Check for performance-related elements
        self.assertContains(response, 'preconnect')  # DNS prefetching
        self.assertContains(response, 'performance.js')  # Performance monitoring
        
        # Check for proper caching headers (would be set by Django middleware)
        # This is more of a server configuration test
        
        # Check for minified resources in production
        # self.assertContains(response, '.min.css')
        # self.assertContains(response, '.min.js')
    
    def test_cross_browser_compatibility(self):
        """Test cross-browser compatibility features"""
        response = self.client.get(reverse('index'))
        
        # Check for polyfills
        self.assertContains(response, 'polyfills.js')
        self.assertContains(response, 'browser-fallbacks.css')
        
        # Check for vendor prefixes in CSS (would be in the CSS files)
        # This is more of a static file test
    
    def test_error_handling(self):
        """Test error handling and user feedback"""
        # Test 404 handling
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
        
        # Test form error handling
        invalid_login = {
            't1': '',  # Empty username
            't2': ''   # Empty password
        }
        
        response = self.client.post(reverse('UserLoginAction'), invalid_login)
        # Should show validation errors
        self.assertIn(response.status_code, [200, 400])
    
    def test_mobile_responsiveness(self):
        """Test mobile responsiveness features"""
        # Simulate mobile user agent
        response = self.client.get(reverse('index'), HTTP_USER_AGENT='Mobile')
        
        # Check for responsive elements
        self.assertContains(response, 'viewport')
        self.assertContains(response, 'navbar-toggler')
        self.assertContains(response, 'col-md-')  # Bootstrap responsive classes
        
        # Check for mobile-specific CSS
        self.assertContains(response, '@media')  # Would be in CSS files


def run_integration_tests():
    """Run all integration tests and report results"""
    import unittest
    
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(StrokeUIIntegrationTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Report results
    print(f"\n{'='*60}")
    print("STROKE UI MODERNIZATION - INTEGRATION TEST RESULTS")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    print(f"\n{'='*60}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    print("Starting Stroke UI Modernization Integration Tests...")
    print("This will test all templates, workflows, and functionality.")
    print(f"{'='*60}")
    
    success = run_integration_tests()
    
    if success:
        print("✅ All integration tests passed!")
        print("The stroke UI modernization is ready for production.")
    else:
        print("❌ Some tests failed.")
        print("Please review the failures above and fix any issues.")
    
    sys.exit(0 if success else 1)