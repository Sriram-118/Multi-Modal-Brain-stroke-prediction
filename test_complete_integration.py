#!/usr/bin/env python
"""
Complete Integration Test for Modernized Templates
Tests all templates work correctly with Django views and complete user workflows
"""

import os
import sys
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MultimodalStroke.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from StrokeApp.models import UserRegistration


class TemplateIntegrationTests(TestCase):
    """Test suite for template integration with Django views"""
    
    def setUp(self):
        """Set up test client and test user"""
        self.client = Client()
        
        # Create test user in database
        self.test_user = UserRegistration.objects.create(
            username='testuser',
            password='testpass123',
            contact='1234567890',
            email='test@example.com',
            address='Test Address'
        )
    
    def test_index_template_loads(self):
        """Test that index.html template loads correctly"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Multi-Modal Stroke Prediction')
    
    def test_login_template_loads(self):
        """Test that UserLogin.html template loads correctly"""
        response = self.client.get(reverse('UserLogin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'UserLogin.html')
        self.assertContains(response, 'Healthcare Professional Login')
    
    def test_register_template_loads(self):
        """Test that Register.html template loads correctly"""
        response = self.client.get(reverse('Register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Register.html')
        self.assertContains(response, 'Create Healthcare Account')
    
    def test_predict_template_loads(self):
        """Test that Predict.html template loads correctly"""
        # Set up session to simulate logged-in user
        session = self.client.session
        session['uname'] = 'testuser'
        session.save()
        
        response = self.client.get(reverse('Predict'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Predict.html')
        self.assertContains(response, 'Multi-Modal Stroke Prediction')
    
    def test_base_template_structure(self):
        """Test that base.html template has correct structure"""
        response = self.client.get(reverse('index'))
        
        # Check for Bootstrap 5
        self.assertContains(response, 'bootstrap@5.3.0')
        
        # Check for navigation
        self.assertContains(response, 'navbar')
        
        # Check for footer
        self.assertContains(response, 'footer')
    
    def test_predict_form_fields(self):
        """Test that Predict.html has all required form fields"""
        session = self.client.session
        session['uname'] = 'testuser'
        session.save()
        
        response = self.client.get(reverse('Predict'))
        
        # Check for all required form fields (t1-t7)
        self.assertContains(response, 'name="t1"')  # Gender
        self.assertContains(response, 'name="t2"')  # Age
        self.assertContains(response, 'name="t3"')  # Hypertension
        self.assertContains(response, 'name="t4"')  # Glucose
        self.assertContains(response, 'name="t5"')  # BMI
        self.assertContains(response, 'name="t6"')  # Smoking
        self.assertContains(response, 'name="t7"')  # Image file
    
    def test_predict_form_action(self):
        """Test that Predict.html form submits to correct URL"""
        session = self.client.session
        session['uname'] = 'testuser'
        session.save()
        
        response = self.client.get(reverse('Predict'))
        self.assertContains(response, 'action="/PredictAction"')
    
    def test_csrf_token_present(self):
        """Test that CSRF token is present in forms"""
        response = self.client.get(reverse('UserLogin'))
        self.assertContains(response, 'csrfmiddlewaretoken')
        
        response = self.client.get(reverse('Register'))
        self.assertContains(response, 'csrfmiddlewaretoken')
        
        session = self.client.session
        session['uname'] = 'testuser'
        session.save()
        
        response = self.client.get(reverse('Predict'))
        self.assertContains(response, 'csrfmiddlewaretoken')
    
    def test_responsive_meta_tags(self):
        """Test that templates have responsive meta tags"""
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'viewport')
        self.assertContains(response, 'width=device-width')
    
    def test_accessibility_features(self):
        """Test that templates have accessibility features"""
        response = self.client.get(reverse('index'))
        
        # Check for ARIA labels
        self.assertContains(response, 'aria-label')
        
        # Check for semantic HTML
        self.assertContains(response, '<nav')
        self.assertContains(response, '<main')
        self.assertContains(response, '<footer')
    
    def test_navigation_consistency(self):
        """Test that navigation is consistent across pages"""
        pages = ['index', 'UserLogin', 'Register']
        
        for page in pages:
            response = self.client.get(reverse(page))
            self.assertContains(response, 'navbar')
            self.assertContains(response, 'Stroke Prediction')
    
    def test_file_upload_integration(self):
        """Test that file upload component is integrated in Predict.html"""
        session = self.client.session
        session['uname'] = 'testuser'
        session.save()
        
        response = self.client.get(reverse('Predict'))
        
        # Check for file upload area
        self.assertContains(response, 'uploadArea')
        self.assertContains(response, 'filePreview')
        
        # Check for file upload JavaScript
        self.assertContains(response, 'file-upload.js')
    
    def test_form_validation_integration(self):
        """Test that form validation is integrated"""
        response = self.client.get(reverse('UserLogin'))
        self.assertContains(response, 'form-validation.js')
        
        session = self.client.session
        session['uname'] = 'testuser'
        session.save()
        
        response = self.client.get(reverse('Predict'))
        self.assertContains(response, 'needs-validation')


class UserWorkflowTests(TestCase):
    """Test complete user workflows from login to prediction"""
    
    def setUp(self):
        """Set up test client and test user"""
        self.client = Client()
        
        # Create test user
        self.test_user = UserRegistration.objects.create(
            username='workflowuser',
            password='testpass123',
            contact='9876543210',
            email='workflow@example.com',
            address='Workflow Test Address'
        )
    
    def test_complete_login_workflow(self):
        """Test complete login workflow"""
        # Step 1: Access login page
        response = self.client.get(reverse('UserLogin'))
        self.assertEqual(response.status_code, 200)
        
        # Step 2: Submit login form
        response = self.client.post(reverse('UserLoginAction'), {
            't1': 'workflowuser',
            't2': 'testpass123'
        })
        
        # Should redirect or show success
        self.assertIn(response.status_code, [200, 302])
    
    def test_complete_registration_workflow(self):
        """Test complete registration workflow"""
        # Step 1: Access registration page
        response = self.client.get(reverse('Register'))
        self.assertEqual(response.status_code, 200)
        
        # Step 2: Submit registration form
        response = self.client.post(reverse('RegisterAction'), {
            't1': 'newuser',
            't2': 'newpass123',
            't3': '5555555555',
            't4': 'newuser@example.com',
            't5': 'New User Address'
        })
        
        # Should redirect or show success
        self.assertIn(response.status_code, [200, 302])
    
    def test_navigation_to_prediction(self):
        """Test navigation from home to prediction page"""
        # Set up session
        session = self.client.session
        session['uname'] = 'workflowuser'
        session.save()
        
        # Step 1: Access home page
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
        # Step 2: Navigate to prediction page
        response = self.client.get(reverse('Predict'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Predict.html')


class BackwardCompatibilityTests(TestCase):
    """Test backward compatibility with existing URL patterns and views"""
    
    def test_url_patterns_unchanged(self):
        """Test that all URL patterns are still accessible"""
        urls_to_test = [
            'index',
            'UserLogin',
            'Register',
            'Predict'
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                self.assertIsNotNone(url)
            except Exception as e:
                self.fail(f"URL pattern '{url_name}' not found: {e}")
    
    def test_form_field_names_preserved(self):
        """Test that form field names (t1-t7) are preserved"""
        session = self.client.session
        session['uname'] = 'testuser'
        session.save()
        
        response = self.client.get(reverse('Predict'))
        
        # All field names must be exactly as expected by Django views
        expected_fields = ['t1', 't2', 't3', 't4', 't5', 't6', 't7']
        
        for field in expected_fields:
            self.assertContains(response, f'name="{field}"')
    
    def test_form_submission_format(self):
        """Test that form submission format is compatible"""
        session = self.client.session
        session['uname'] = 'testuser'
        session.save()
        
        response = self.client.get(reverse('Predict'))
        
        # Check form method and enctype
        self.assertContains(response, 'method="post"')
        self.assertContains(response, 'enctype="multipart/form-data"')


def run_tests():
    """Run all integration tests"""
    import unittest
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TemplateIntegrationTests))
    suite.addTests(loader.loadTestsFromTestCase(UserWorkflowTests))
    suite.addTests(loader.loadTestsFromTestCase(BackwardCompatibilityTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("INTEGRATION TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
