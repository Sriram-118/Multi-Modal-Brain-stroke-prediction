#!/usr/bin/env python3
"""
Template verification script for stroke UI modernization
Verifies all templates are properly modernized and compatible with Django
"""

import os
import re
from pathlib import Path

class TemplateVerifier:
    """Verifies that all templates meet modernization requirements"""
    
    def __init__(self, template_dir):
        self.template_dir = Path(template_dir)
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
        
        # Define verification criteria
        self.required_elements = {
            'base.html': [
                'Bootstrap 5',
                'modern.css',
                'csrf_token',
                'navbar',
                'accessibility.js',
                'security.js'
            ],
            'index.html': [
                'extends.*base.html',
                'hero-section',
                'feature-cards',
                'btn-primary'
            ],
            'UserLogin.html': [
                'extends.*base.html',
                'csrf_token',
                'form-floating',
                'login-card',
                'form-validation'
            ],
            'Register.html': [
                'extends.*base.html',
                'csrf_token',
                'form-floating',
                'register-card',
                'password-requirements'
            ],
            'Predict.html': [
                'extends.*base.html',
                'csrf_token',
                'form-section',
                'file-upload-area',
                'form-progress'
            ],
            'UserScreen.html': [
                'extends.*base.html',
                'prediction-results',
                'chart-container',
                'responsive'
            ]
        }
        
        self.deprecated_elements = [
            '<font',
            '<center',
            '<table.*layout',
            'align=',
            'bgcolor=',
            'style=.*position:absolute',
            'onclick=',
            'javascript:'
        ]
        
        self.security_requirements = [
            'csrf_token',
            'csrfmiddlewaretoken'
        ]
    
    def verify_all_templates(self):
        """Verify all templates in the directory"""
        print("🔍 Starting template verification...")
        print(f"Template directory: {self.template_dir}")
        print("="*60)
        
        template_files = list(self.template_dir.glob('*.html'))
        
        if not template_files:
            print("❌ No HTML templates found!")
            return False
        
        for template_file in template_files:
            self.verify_template(template_file)
        
        self.print_results()
        return len(self.results['failed']) == 0
    
    def verify_template(self, template_path):
        """Verify a single template file"""
        template_name = template_path.name
        print(f"\n📄 Verifying {template_name}...")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for required elements
            self.check_required_elements(template_name, content)
            
            # Check for deprecated elements
            self.check_deprecated_elements(template_name, content)
            
            # Check security requirements
            self.check_security_requirements(template_name, content)
            
            # Check Bootstrap integration
            self.check_bootstrap_integration(template_name, content)
            
            # Check accessibility features
            self.check_accessibility_features(template_name, content)
            
            # Check responsive design
            self.check_responsive_design(template_name, content)
            
            print(f"✅ {template_name} verification completed")
            
        except Exception as e:
            error_msg = f"Error reading {template_name}: {str(e)}"
            self.results['failed'].append(error_msg)
            print(f"❌ {error_msg}")
    
    def check_required_elements(self, template_name, content):
        """Check for required modernization elements"""
        if template_name in self.required_elements:
            missing_elements = []
            
            for element in self.required_elements[template_name]:
                if not re.search(element, content, re.IGNORECASE):
                    missing_elements.append(element)
            
            if missing_elements:
                error_msg = f"{template_name}: