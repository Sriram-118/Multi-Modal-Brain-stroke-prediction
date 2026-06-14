#!/usr/bin/env python3
"""
Integration Test for Performance Optimizations
Verifies that all performance optimizations are correctly implemented
"""

import os
from pathlib import Path

class PerformanceOptimizationTest:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.static_path = self.base_path / 'StrokeApp' / 'static'
        self.template_path = self.base_path / 'StrokeApp' / 'templates'
        self.passed = 0
        self.failed = 0
        self.warnings = 0
    
    def test_minified_files_exist(self):
        """Test that minified versions of all CSS and JS files exist"""
        print("\n📋 Test 1: Checking minified files exist...")
        
        css_files = ['browser-fallbacks.css', 'modern.css']
        js_files = [
            'accessibility.js', 'chart-utils.js', 'file-upload.js',
            'form-validation.js', 'modern.js', 'navigation.js',
            'page-transitions.js', 'performance-monitor.js', 'performance.js',
            'polyfills.js', 'prediction-chart.js', 'security.js'
        ]
        
        all_passed = True
        
        for css_file in css_files:
            min_file = css_file.replace('.css', '.min.css')
            min_path = self.static_path / 'css' / min_file
            if min_path.exists():
                print(f"  ✅ {min_file} exists")
            else:
                print(f"  ❌ {min_file} NOT FOUND")
                all_passed = False
        
        for js_file in js_files:
            min_file = js_file.replace('.js', '.min.js')
            min_path = self.static_path / 'js' / min_file
            if min_path.exists():
                print(f"  ✅ {min_file} exists")
            else:
                print(f"  ❌ {min_file} NOT FOUND")
                all_passed = False
        
        if all_passed:
            print("  ✅ All minified files exist")
            self.passed += 1
        else:
            print("  ❌ Some minified files are missing")
            self.failed += 1
    
    def test_base_template_uses_minified(self):
        """Test that base template references minified assets"""
        print("\n📋 Test 2: Checking base template uses minified assets...")
        
        base_template = self.template_path / 'base.html'
        if not base_template.exists():
            print("  ❌ base.html not found")
            self.failed += 1
            return
        
        content = base_template.read_text()
        
        checks = [
            ('modern.min.css', 'modern.min.css' in content),
            ('browser-fallbacks.min.css', 'browser-fallbacks.min.css' in content),
            ('defer attribute', 'defer' in content),
            ('minified JS', '.min.js' in content)
        ]
        
        all_passed = True
        for check_name, result in checks:
            if result:
                print(f"  ✅ {check_name} found")
            else:
                print(f"  ❌ {check_name} NOT FOUND")
                all_passed = False
        
        if all_passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def test_no_inline_styles(self):
        """Test that templates don't have inline styles"""
        print("\n📋 Test 3: Checking for inline styles in templates...")
        
        templates_to_check = ['index.html', 'Register.html']
        all_passed = True
        
        for template_name in templates_to_check:
            template_path = self.template_path / template_name
            if not template_path.exists():
                print(f"  ⚠️  {template_name} not found")
                self.warnings += 1
                continue
            
            content = template_path.read_text()
            
            # Check for common inline style patterns
            inline_style_patterns = [
                'style="width:',
                'style="height:',
                'style="display:',
                'style="font-size:'
            ]
            
            has_inline_styles = any(pattern in content for pattern in inline_style_patterns)
            
            if has_inline_styles:
                print(f"  ⚠️  {template_name} may have inline styles")
                all_passed = False
            else:
                print(f"  ✅ {template_name} has no common inline styles")
        
        if all_passed:
            self.passed += 1
        else:
            self.warnings += 1
    
    def test_caching_configured(self):
        """Test that Django caching is configured"""
        print("\n📋 Test 4: Checking Django caching configuration...")
        
        settings_path = self.base_path / 'Stroke' / 'settings.py'
        if not settings_path.exists():
            print("  ❌ settings.py not found")
            self.failed += 1
            return
        
        content = settings_path.read_text()
        
        checks = [
            ('CACHES configuration', 'CACHES' in content),
            ('Cache middleware', 'CacheMiddleware' in content),
            ('Cache timeout', 'CACHE_MIDDLEWARE_SECONDS' in content)
        ]
        
        all_passed = True
        for check_name, result in checks:
            if result:
                print(f"  ✅ {check_name} found")
            else:
                print(f"  ❌ {check_name} NOT FOUND")
                all_passed = False
        
        if all_passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def test_performance_css_classes(self):
        """Test that performance CSS classes are defined"""
        print("\n📋 Test 5: Checking performance CSS classes...")
        
        modern_css = self.static_path / 'css' / 'modern.css'
        if not modern_css.exists():
            print("  ❌ modern.css not found")
            self.failed += 1
            return
        
        content = modern_css.read_text()
        
        classes = [
            'hero-image-optimized',
            'step-number-badge',
            'gpu-accelerated',
            'fadeIn',
            'prefers-reduced-motion'
        ]
        
        all_passed = True
        for class_name in classes:
            if class_name in content:
                print(f"  ✅ .{class_name} defined")
            else:
                print(f"  ❌ .{class_name} NOT FOUND")
                all_passed = False
        
        if all_passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def test_lazy_loading_implemented(self):
        """Test that lazy loading is implemented"""
        print("\n📋 Test 6: Checking lazy loading implementation...")
        
        index_template = self.template_path / 'index.html'
        if not index_template.exists():
            print("  ⚠️  index.html not found")
            self.warnings += 1
            return
        
        content = index_template.read_text()
        
        if 'loading="lazy"' in content:
            print("  ✅ Lazy loading attribute found")
            self.passed += 1
        else:
            print("  ⚠️  Lazy loading attribute not found")
            self.warnings += 1
    
    def run_all_tests(self):
        """Run all performance optimization tests"""
        print("="*80)
        print("🚀 PERFORMANCE OPTIMIZATION INTEGRATION TESTS")
        print("="*80)
        
        self.test_minified_files_exist()
        self.test_base_template_uses_minified()
        self.test_no_inline_styles()
        self.test_caching_configured()
        self.test_performance_css_classes()
        self.test_lazy_loading_implemented()
        
        print("\n" + "="*80)
        print("📊 TEST RESULTS SUMMARY")
        print("="*80)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"⚠️  Warnings: {self.warnings}")
        
        total = self.passed + self.failed + self.warnings
        if total > 0:
            success_rate = (self.passed / total) * 100
            print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 All critical tests passed!")
            return True
        else:
            print(f"\n⚠️  {self.failed} test(s) failed. Please review.")
            return False

if __name__ == '__main__':
    base_path = Path(__file__).parent
    tester = PerformanceOptimizationTest(base_path)
    success = tester.run_all_tests()
    exit(0 if success else 1)
