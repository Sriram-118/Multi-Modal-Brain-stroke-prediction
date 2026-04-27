#!/usr/bin/env python
"""
Template Modernization Verification Script
Verifies that all templates have been modernized correctly
"""

import os
import re
from pathlib import Path


class TemplateVerifier:
    """Verifies template modernization"""
    
    def __init__(self, templates_dir):
        self.templates_dir = Path(templates_dir)
        self.results = {
            'passed': [],
            'failed': [],
            'warnings': []
        }
    
    def verify_all(self):
        """Run all verification checks"""
        print("="*70)
        print("TEMPLATE MODERNIZATION VERIFICATION")
        print("="*70)
        print()
        
        templates = [
            'base.html',
            'index.html',
            'UserLogin.html',
            'Register.html',
            'Predict.html',
            'UserScreen.html'
        ]
        
        for template in templates:
            print(f"Verifying {template}...")
            self.verify_template(template)
            print()
        
        self.print_summary()
    
    def verify_template(self, template_name):
        """Verify a single template"""
        template_path = self.templates_dir / template_name
        
        if not template_path.exists():
            self.results['failed'].append(f"{template_name}: File not found")
            print(f"  ❌ File not found")
            return
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Run checks
        checks = [
            self.check_extends_base,
            self.check_no_deprecated_tags,
            self.check_no_inline_styles,
            self.check_bootstrap_classes,
            self.check_semantic_html,
            self.check_accessibility,
            self.check_responsive_design
        ]
        
        for check in checks:
            check(template_name, content)
    
    def check_extends_base(self, template_name, content):
        """Check if template extends base.html (except base.html itself)"""
        if template_name == 'base.html':
            return
        
        if "{% extends 'base.html' %}" in content or '{% extends "base.html" %}' in content:
            self.results['passed'].append(f"{template_name}: Extends base.html ✓")
            print(f"  ✓ Extends base.html")
        else:
            self.results['failed'].append(f"{template_name}: Does not extend base.html")
            print(f"  ❌ Does not extend base.html")
    
    def check_no_deprecated_tags(self, template_name, content):
        """Check for deprecated HTML tags"""
        deprecated_tags = ['<font', '<center', '<marquee', '<blink']
        found_deprecated = []
        
        for tag in deprecated_tags:
            if tag in content.lower():
                found_deprecated.append(tag)
        
        if found_deprecated:
            self.results['failed'].append(f"{template_name}: Contains deprecated tags: {', '.join(found_deprecated)}")
            print(f"  ❌ Contains deprecated tags: {', '.join(found_deprecated)}")
        else:
            self.results['passed'].append(f"{template_name}: No deprecated tags ✓")
            print(f"  ✓ No deprecated tags")
    
    def check_no_inline_styles(self, template_name, content):
        """Check for inline styles (except in style blocks)"""
        # Remove style blocks from content
        content_no_style_blocks = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
        
        # Check for style attributes
        inline_styles = re.findall(r'style\s*=\s*["\'][^"\']*["\']', content_no_style_blocks)
        
        if inline_styles and len(inline_styles) > 2:  # Allow a few for dynamic styles
            self.results['warnings'].append(f"{template_name}: Contains {len(inline_styles)} inline styles")
            print(f"  ⚠ Contains {len(inline_styles)} inline styles")
        else:
            self.results['passed'].append(f"{template_name}: Minimal inline styles ✓")
            print(f"  ✓ Minimal inline styles")
    
    def check_bootstrap_classes(self, template_name, content):
        """Check for Bootstrap classes"""
        bootstrap_classes = ['container', 'row', 'col-', 'btn', 'form-', 'card', 'navbar']
        found_classes = []
        
        for cls in bootstrap_classes:
            if cls in content:
                found_classes.append(cls)
        
        if len(found_classes) >= 4:
            self.results['passed'].append(f"{template_name}: Uses Bootstrap classes ✓")
            print(f"  ✓ Uses Bootstrap classes ({len(found_classes)} types found)")
        else:
            self.results['warnings'].append(f"{template_name}: Limited Bootstrap usage")
            print(f"  ⚠ Limited Bootstrap usage ({len(found_classes)} types found)")
    
    def check_semantic_html(self, template_name, content):
        """Check for semantic HTML5 elements"""
        semantic_elements = ['<nav', '<main', '<header', '<footer', '<section', '<article']
        found_elements = []
        
        for element in semantic_elements:
            if element in content.lower():
                found_elements.append(element)
        
        if len(found_elements) >= 2:
            self.results['passed'].append(f"{template_name}: Uses semantic HTML ✓")
            print(f"  ✓ Uses semantic HTML ({len(found_elements)} types found)")
        else:
            self.results['warnings'].append(f"{template_name}: Limited semantic HTML")
            print(f"  ⚠ Limited semantic HTML ({len(found_elements)} types found)")
    
    def check_accessibility(self, template_name, content):
        """Check for accessibility features"""
        accessibility_features = ['aria-label', 'aria-', 'role=', 'alt=']
        found_features = []
        
        for feature in accessibility_features:
            if feature in content.lower():
                found_features.append(feature)
        
        if len(found_features) >= 2:
            self.results['passed'].append(f"{template_name}: Has accessibility features ✓")
            print(f"  ✓ Has accessibility features ({len(found_features)} types found)")
        else:
            self.results['warnings'].append(f"{template_name}: Limited accessibility features")
            print(f"  ⚠ Limited accessibility features ({len(found_features)} types found)")
    
    def check_responsive_design(self, template_name, content):
        """Check for responsive design features"""
        responsive_features = ['col-md-', 'col-lg-', 'col-sm-', 'd-none', 'd-md-', 'viewport']
        found_features = []
        
        for feature in responsive_features:
            if feature in content:
                found_features.append(feature)
        
        if len(found_features) >= 2:
            self.results['passed'].append(f"{template_name}: Has responsive design ✓")
            print(f"  ✓ Has responsive design ({len(found_features)} features found)")
        else:
            self.results['warnings'].append(f"{template_name}: Limited responsive features")
            print(f"  ⚠ Limited responsive features ({len(found_features)} features found)")
    
    def print_summary(self):
        """Print verification summary"""
        print("="*70)
        print("VERIFICATION SUMMARY")
        print("="*70)
        print()
        
        print(f"✓ Passed Checks: {len(self.results['passed'])}")
        print(f"❌ Failed Checks: {len(self.results['failed'])}")
        print(f"⚠ Warnings: {len(self.results['warnings'])}")
        print()
        
        if self.results['failed']:
            print("FAILED CHECKS:")
            for failure in self.results['failed']:
                print(f"  ❌ {failure}")
            print()
        
        if self.results['warnings']:
            print("WARNINGS:")
            for warning in self.results['warnings']:
                print(f"  ⚠ {warning}")
            print()
        
        print("="*70)
        
        # Overall status
        if not self.results['failed']:
            print("✓ ALL CRITICAL CHECKS PASSED")
            return True
        else:
            print("❌ SOME CHECKS FAILED")
            return False


def verify_predict_template_specifics():
    """Verify Predict.html specific requirements"""
    print("\n" + "="*70)
    print("PREDICT.HTML SPECIFIC VERIFICATION")
    print("="*70)
    print()
    
    template_path = Path('StrokeApp/templates/Predict.html')
    
    if not template_path.exists():
        print("❌ Predict.html not found")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        "Extends base.html": "{% extends 'base.html' %}" in content or '{% extends "base.html" %}' in content,
        "Has form fields t1-t7": all(f'name="t{i}"' in content for i in range(1, 8)),
        "Form action is PredictAction": 'action="{% url \'PredictAction\' %}"' in content or 'action="/PredictAction"' in content,
        "Has file upload": 'type="file"' in content and 'name="t7"' in content,
        "Has CSRF token": '{% csrf_token %}' in content,
        "Has file-upload.js": 'file-upload.js' in content,
        "Has form validation": 'needs-validation' in content or 'form-validation' in content,
        "Has Bootstrap form classes": 'form-floating' in content or 'form-control' in content,
        "Has progress indicators": 'progress' in content.lower(),
        "Has drag-and-drop area": 'uploadArea' in content or 'upload-area' in content,
        "No deprecated tags": not any(tag in content.lower() for tag in ['<font', '<center']),
        "Has accessibility features": 'aria-' in content.lower()
    }
    
    passed = 0
    failed = 0
    
    for check_name, result in checks.items():
        if result:
            print(f"  ✓ {check_name}")
            passed += 1
        else:
            print(f"  ❌ {check_name}")
            failed += 1
    
    print()
    print(f"Passed: {passed}/{len(checks)}")
    print(f"Failed: {failed}/{len(checks)}")
    print("="*70)
    
    return failed == 0


def verify_django_compatibility():
    """Verify Django backend compatibility"""
    print("\n" + "="*70)
    print("DJANGO COMPATIBILITY VERIFICATION")
    print("="*70)
    print()
    
    template_path = Path('StrokeApp/templates/Predict.html')
    
    if not template_path.exists():
        print("❌ Predict.html not found")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check field names match Django view expectations
    expected_fields = {
        't1': 'Gender',
        't2': 'Age',
        't3': 'Hypertension',
        't4': 'Glucose',
        't5': 'BMI',
        't6': 'Smoking',
        't7': 'Image file'
    }
    
    print("Checking form field names:")
    all_present = True
    for field, description in expected_fields.items():
        if f'name="{field}"' in content:
            print(f"  ✓ {field} ({description})")
        else:
            print(f"  ❌ {field} ({description}) - NOT FOUND")
            all_present = False
    
    print()
    print("Checking form attributes:")
    
    checks = {
        "Method is POST": 'method="post"' in content.lower(),
        "Has enctype for file upload": 'enctype="multipart/form-data"' in content,
        "Action URL is correct": 'PredictAction' in content,
        "CSRF token present": '{% csrf_token %}' in content
    }
    
    for check_name, result in checks.items():
        if result:
            print(f"  ✓ {check_name}")
        else:
            print(f"  ❌ {check_name}")
            all_present = False
    
    print()
    print("="*70)
    
    if all_present:
        print("✓ DJANGO COMPATIBILITY VERIFIED")
        return True
    else:
        print("❌ DJANGO COMPATIBILITY ISSUES FOUND")
        return False


def main():
    """Main verification function"""
    templates_dir = Path('StrokeApp/templates')
    
    if not templates_dir.exists():
        print(f"❌ Templates directory not found: {templates_dir}")
        return False
    
    # Run general template verification
    verifier = TemplateVerifier(templates_dir)
    general_passed = verifier.verify_all()
    
    # Run Predict.html specific verification
    predict_passed = verify_predict_template_specifics()
    
    # Run Django compatibility verification
    django_passed = verify_django_compatibility()
    
    # Overall result
    print("\n" + "="*70)
    print("OVERALL VERIFICATION RESULT")
    print("="*70)
    
    if general_passed and predict_passed and django_passed:
        print("✓ ALL VERIFICATIONS PASSED")
        print("✓ Templates are modernized and compatible with Django backend")
        return True
    else:
        print("❌ SOME VERIFICATIONS FAILED")
        if not general_passed:
            print("  - General template checks failed")
        if not predict_passed:
            print("  - Predict.html specific checks failed")
        if not django_passed:
            print("  - Django compatibility checks failed")
        return False


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
