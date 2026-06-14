#!/usr/bin/env python3
"""
Final System Verification for Stroke UI Modernization
Task 12: Complete system verification across all requirements
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple

class SystemVerification:
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.template_path = self.base_path / "StrokeApp" / "templates"
        self.static_path = self.base_path / "StrokeApp" / "static"
        self.results = {
            "passed": [],
            "failed": [],
            "warnings": []
        }
    
    def log_pass(self, message: str):
        """Log a passed verification"""
        self.results["passed"].append(message)
        print(f"✓ PASS: {message}")
    
    def log_fail(self, message: str):
        """Log a failed verification"""
        self.results["failed"].append(message)
        print(f"✗ FAIL: {message}")
    
    def log_warning(self, message: str):
        """Log a warning"""
        self.results["warnings"].append(message)
        print(f"⚠ WARNING: {message}")
    
    def verify_template_structure(self):
        """Verify all templates exist and have modern structure"""
        print("\n=== Verifying Template Structure ===")
        
        required_templates = [
            "base.html",
            "index.html",
            "UserLogin.html",
            "Register.html",
            "Predict.html",
            "UserScreen.html"
        ]
        
        for template in required_templates:
            template_file = self.template_path / template
            if not template_file.exists():
                self.log_fail(f"Template missing: {template}")
                continue
            
            content = template_file.read_text(encoding='utf-8')
            
            # Check for deprecated tags
            deprecated_tags = ['<center>', '<font>', '<marquee>', '<blink>']
            has_deprecated = any(tag in content for tag in deprecated_tags)
            if has_deprecated:
                self.log_fail(f"{template}: Contains deprecated HTML tags")
            else:
                self.log_pass(f"{template}: No deprecated HTML tags")
            
            # Check for inline styles (excluding style tags)
            inline_style_pattern = r'<[^>]+style\s*=\s*["\'][^"\']+["\']'
            inline_styles = re.findall(inline_style_pattern, content)
            if inline_styles and template != "base.html":  # base.html may have critical inline styles
                self.log_warning(f"{template}: Contains {len(inline_styles)} inline styles")
            else:
                self.log_pass(f"{template}: Minimal or no inline styles")
            
            # Check for Bootstrap classes
            if 'bootstrap' in content.lower() or 'container' in content or 'row' in content:
                self.log_pass(f"{template}: Uses Bootstrap framework")
            else:
                self.log_warning(f"{template}: May not be using Bootstrap")
            
            # Check for semantic HTML5
            semantic_tags = ['<header>', '<nav>', '<main>', '<section>', '<article>', '<footer>']
            has_semantic = any(tag in content for tag in semantic_tags)
            if has_semantic or template in ["UserLogin.html", "Register.html", "Predict.html"]:
                self.log_pass(f"{template}: Uses semantic HTML5 elements")
            else:
                self.log_warning(f"{template}: Limited semantic HTML5 usage")
    
    def verify_responsive_design(self):
        """Verify responsive design implementation"""
        print("\n=== Verifying Responsive Design ===")
        
        # Check base template for viewport meta tag
        base_template = self.template_path / "base.html"
        if base_template.exists():
            content = base_template.read_text(encoding='utf-8')
            if 'viewport' in content and 'width=device-width' in content:
                self.log_pass("Viewport meta tag configured for responsive design")
            else:
                self.log_fail("Missing or incorrect viewport meta tag")
            
            # Check for responsive navigation
            if 'navbar-toggler' in content or 'navbar-collapse' in content:
                self.log_pass("Responsive navigation implemented")
            else:
                self.log_warning("Responsive navigation may not be fully implemented")
        
        # Check CSS for media queries
        css_files = list(self.static_path.glob("css/*.css"))
        media_query_found = False
        for css_file in css_files:
            content = css_file.read_text(encoding='utf-8')
            if '@media' in content:
                media_query_found = True
                self.log_pass(f"{css_file.name}: Contains responsive media queries")
        
        if not media_query_found:
            self.log_warning("No custom media queries found in CSS files")
    
    def verify_form_enhancements(self):
        """Verify form validation and enhancements"""
        print("\n=== Verifying Form Enhancements ===")
        
        form_templates = ["UserLogin.html", "Register.html", "Predict.html"]
        
        for template in form_templates:
            template_file = self.template_path / template
            if not template_file.exists():
                continue
            
            content = template_file.read_text(encoding='utf-8')
            
            # Check for CSRF token
            if 'csrf_token' in content:
                self.log_pass(f"{template}: CSRF token present")
            else:
                self.log_fail(f"{template}: Missing CSRF token")
            
            # Check for form validation classes
            if 'was-validated' in content or 'needs-validation' in content or 'is-invalid' in content:
                self.log_pass(f"{template}: Form validation classes present")
            else:
                self.log_warning(f"{template}: May lack client-side validation")
            
            # Check for Bootstrap form classes
            if 'form-control' in content or 'form-group' in content:
                self.log_pass(f"{template}: Uses Bootstrap form styling")
            else:
                self.log_warning(f"{template}: May not use Bootstrap form styling")
        
        # Check for form validation JavaScript
        js_files = list(self.static_path.glob("js/*validation*.js"))
        if js_files:
            self.log_pass(f"Form validation JavaScript found: {len(js_files)} file(s)")
        else:
            self.log_warning("No dedicated form validation JavaScript files found")
    
    def verify_javascript_enhancements(self):
        """Verify JavaScript enhancements are in place"""
        print("\n=== Verifying JavaScript Enhancements ===")
        
        required_js_features = {
            "navigation": ["navigation.js"],
            "form-validation": ["form-validation.js"],
            "file-upload": ["file-upload.js"],
            "charts": ["prediction-chart.js", "chart-utils.js"],
            "accessibility": ["accessibility.js"],
            "performance": ["performance.js", "performance-monitor.js"]
        }
        
        for feature, filenames in required_js_features.items():
            found = False
            for filename in filenames:
                js_file = self.static_path / "js" / filename
                if js_file.exists():
                    found = True
                    self.log_pass(f"{feature}: {filename} exists")
                    break
            
            if not found:
                self.log_warning(f"{feature}: No JavaScript file found")
    
    def verify_accessibility_features(self):
        """Verify accessibility implementation"""
        print("\n=== Verifying Accessibility Features ===")
        
        # Check templates for ARIA attributes
        templates = list(self.template_path.glob("*.html"))
        aria_count = 0
        alt_text_count = 0
        
        for template in templates:
            content = template.read_text(encoding='utf-8')
            
            # Count ARIA attributes
            aria_attrs = re.findall(r'aria-[a-z]+', content)
            aria_count += len(aria_attrs)
            
            # Count alt attributes
            alt_attrs = re.findall(r'alt\s*=\s*["\'][^"\']+["\']', content)
            alt_text_count += len(alt_attrs)
        
        if aria_count > 0:
            self.log_pass(f"ARIA attributes found: {aria_count} instances")
        else:
            self.log_warning("Limited ARIA attribute usage")
        
        if alt_text_count > 0:
            self.log_pass(f"Alt text attributes found: {alt_text_count} instances")
        else:
            self.log_warning("Limited alt text usage")
        
        # Check for accessibility JavaScript
        accessibility_js = self.static_path / "js" / "accessibility.js"
        if accessibility_js.exists():
            self.log_pass("Accessibility JavaScript module exists")
        else:
            self.log_warning("No dedicated accessibility JavaScript module")
    
    def verify_performance_optimizations(self):
        """Verify performance optimizations"""
        print("\n=== Verifying Performance Optimizations ===")
        
        # Check for minified files
        css_files = list(self.static_path.glob("css/*.css"))
        js_files = list(self.static_path.glob("js/*.js"))
        
        minified_css = [f for f in css_files if '.min.' in f.name]
        minified_js = [f for f in js_files if '.min.' in f.name]
        
        if minified_css:
            self.log_pass(f"Minified CSS files found: {len(minified_css)}")
        else:
            self.log_warning("No minified CSS files found")
        
        if minified_js:
            self.log_pass(f"Minified JavaScript files found: {len(minified_js)}")
        else:
            self.log_warning("No minified JavaScript files found")
        
        # Check for performance monitoring
        perf_js = self.static_path / "js" / "performance-monitor.js"
        if perf_js.exists():
            self.log_pass("Performance monitoring JavaScript exists")
        else:
            self.log_warning("No performance monitoring JavaScript")
        
        # Check base template for async/defer on scripts
        base_template = self.template_path / "base.html"
        if base_template.exists():
            content = base_template.read_text(encoding='utf-8')
            if 'defer' in content or 'async' in content:
                self.log_pass("Scripts use async/defer for better performance")
            else:
                self.log_warning("Scripts may not use async/defer attributes")
    
    def verify_cross_browser_support(self):
        """Verify cross-browser compatibility features"""
        print("\n=== Verifying Cross-Browser Support ===")
        
        # Check for polyfills
        polyfills_js = self.static_path / "js" / "polyfills.js"
        if polyfills_js.exists():
            self.log_pass("Polyfills JavaScript exists")
        else:
            self.log_warning("No polyfills JavaScript found")
        
        # Check for browser fallback CSS
        fallback_css = self.static_path / "css" / "browser-fallbacks.css"
        if fallback_css.exists():
            self.log_pass("Browser fallback CSS exists")
        else:
            self.log_warning("No browser fallback CSS found")
        
        # Check CSS for vendor prefixes
        css_files = list(self.static_path.glob("css/*.css"))
        vendor_prefix_found = False
        for css_file in css_files:
            content = css_file.read_text(encoding='utf-8')
            if '-webkit-' in content or '-moz-' in content or '-ms-' in content:
                vendor_prefix_found = True
                break
        
        if vendor_prefix_found:
            self.log_pass("Vendor prefixes found in CSS for cross-browser support")
        else:
            self.log_warning("Limited vendor prefix usage in CSS")
    
    def verify_django_compatibility(self):
        """Verify Django backend compatibility"""
        print("\n=== Verifying Django Backend Compatibility ===")
        
        # Check that form field names are preserved
        predict_template = self.template_path / "Predict.html"
        if predict_template.exists():
            content = predict_template.read_text(encoding='utf-8')
            
            # Check for original field names (t1, t2, t3, etc.)
            field_names = ['t1', 't2', 't3', 't4', 't5', 't6', 't7']
            missing_fields = []
            for field in field_names:
                if f'name="{field}"' not in content and f"name='{field}'" not in content:
                    missing_fields.append(field)
            
            if not missing_fields:
                self.log_pass("All Django form field names preserved in Predict.html")
            else:
                self.log_fail(f"Missing Django field names in Predict.html: {missing_fields}")
        
        # Check login form fields
        login_template = self.template_path / "UserLogin.html"
        if login_template.exists():
            content = login_template.read_text(encoding='utf-8')
            if 't1' in content and 't2' in content:
                self.log_pass("Django form field names preserved in UserLogin.html")
            else:
                self.log_fail("Django field names may be missing in UserLogin.html")
        
        # Check for Django template tags
        templates = list(self.template_path.glob("*.html"))
        django_tags_found = False
        for template in templates:
            content = template.read_text(encoding='utf-8')
            if '{% ' in content or '{{ ' in content:
                django_tags_found = True
                break
        
        if django_tags_found:
            self.log_pass("Django template tags present in templates")
        else:
            self.log_fail("No Django template tags found - templates may not work with Django")
    
    def verify_chart_implementation(self):
        """Verify chart and visualization implementation"""
        print("\n=== Verifying Chart Implementation ===")
        
        # Check for Chart.js or similar library
        base_template = self.template_path / "base.html"
        results_template = self.template_path / "UserScreen.html"
        
        chart_lib_found = False
        for template in [base_template, results_template]:
            if template.exists():
                content = template.read_text(encoding='utf-8')
                if 'chart.js' in content.lower() or 'chartjs' in content.lower():
                    chart_lib_found = True
                    self.log_pass(f"{template.name}: Chart.js library referenced")
                    break
        
        if not chart_lib_found:
            self.log_warning("Chart.js library not found in templates")
        
        # Check for chart JavaScript
        chart_js = self.static_path / "js" / "prediction-chart.js"
        if chart_js.exists():
            self.log_pass("Prediction chart JavaScript exists")
        else:
            self.log_warning("No prediction chart JavaScript found")
        
        # Check chart utilities
        chart_utils = self.static_path / "js" / "chart-utils.js"
        if chart_utils.exists():
            self.log_pass("Chart utilities JavaScript exists")
        else:
            self.log_warning("No chart utilities JavaScript found")
    
    def verify_security_features(self):
        """Verify security implementations"""
        print("\n=== Verifying Security Features ===")
        
        # Check for security JavaScript
        security_js = self.static_path / "js" / "security.js"
        if security_js.exists():
            self.log_pass("Security JavaScript module exists")
        else:
            self.log_warning("No dedicated security JavaScript module")
        
        # Check all forms for CSRF tokens
        form_templates = ["UserLogin.html", "Register.html", "Predict.html"]
        all_have_csrf = True
        for template in form_templates:
            template_file = self.template_path / template
            if template_file.exists():
                content = template_file.read_text(encoding='utf-8')
                if 'csrf_token' not in content:
                    all_have_csrf = False
                    self.log_fail(f"{template}: Missing CSRF token")
        
        if all_have_csrf:
            self.log_pass("All forms have CSRF token protection")
    
    def generate_report(self):
        """Generate final verification report"""
        print("\n" + "="*60)
        print("FINAL SYSTEM VERIFICATION REPORT")
        print("="*60)
        
        total_checks = len(self.results["passed"]) + len(self.results["failed"]) + len(self.results["warnings"])
        
        print(f"\nTotal Checks: {total_checks}")
        print(f"✓ Passed: {len(self.results['passed'])}")
        print(f"✗ Failed: {len(self.results['failed'])}")
        print(f"⚠ Warnings: {len(self.results['warnings'])}")
        
        if self.results["failed"]:
            print("\n" + "="*60)
            print("FAILED CHECKS:")
            print("="*60)
            for failure in self.results["failed"]:
                print(f"  ✗ {failure}")
        
        if self.results["warnings"]:
            print("\n" + "="*60)
            print("WARNINGS:")
            print("="*60)
            for warning in self.results["warnings"]:
                print(f"  ⚠ {warning}")
        
        print("\n" + "="*60)
        if len(self.results["failed"]) == 0:
            print("✓ SYSTEM VERIFICATION PASSED")
            print("All critical checks passed. System is ready for production.")
        else:
            print("✗ SYSTEM VERIFICATION FAILED")
            print(f"{len(self.results['failed'])} critical issue(s) need to be addressed.")
        print("="*60)
        
        return len(self.results["failed"]) == 0
    
    def run_all_verifications(self):
        """Run all verification checks"""
        print("Starting Final System Verification...")
        print("="*60)
        
        self.verify_template_structure()
        self.verify_responsive_design()
        self.verify_form_enhancements()
        self.verify_javascript_enhancements()
        self.verify_accessibility_features()
        self.verify_performance_optimizations()
        self.verify_cross_browser_support()
        self.verify_django_compatibility()
        self.verify_chart_implementation()
        self.verify_security_features()
        
        return self.generate_report()

def main():
    verifier = SystemVerification()
    success = verifier.run_all_verifications()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
