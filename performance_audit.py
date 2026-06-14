#!/usr/bin/env python3
"""
Performance Audit Script for Stroke UI Modernization
Conducts comprehensive performance analysis and optimization recommendations
"""

import os
import json
import gzip
import hashlib
from pathlib import Path
from datetime import datetime

class PerformanceAuditor:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.static_path = self.base_path / 'StrokeApp' / 'static'
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'file_analysis': {},
            'optimization_recommendations': [],
            'performance_metrics': {}
        }
    
    def analyze_file_sizes(self):
        """Analyze sizes of CSS and JS files"""
        print("📊 Analyzing file sizes...")
        
        css_files = list(self.static_path.glob('css/*.css'))
        js_files = list(self.static_path.glob('js/*.js'))
        
        for file_path in css_files + js_files:
            if file_path.is_file():
                size = file_path.stat().st_size
                file_type = 'CSS' if file_path.suffix == '.css' else 'JavaScript'
                
                self.results['file_analysis'][str(file_path.relative_to(self.base_path))] = {
                    'type': file_type,
                    'size_bytes': size,
                    'size_kb': round(size / 1024, 2)
                }
                
                # Recommendations based on size
                if size > 100 * 1024:  # > 100KB
                    self.results['optimization_recommendations'].append({
                        'file': str(file_path.name),
                        'issue': f'Large {file_type} file ({round(size/1024, 2)}KB)',
                        'recommendation': 'Consider minification and code splitting'
                    })
    
    def check_minification_potential(self):
        """Check if files can be minified"""
        print("🔍 Checking minification potential...")
        
        css_files = list(self.static_path.glob('css/*.css'))
        js_files = list(self.static_path.glob('js/*.js'))
        
        for file_path in css_files + js_files:
            if file_path.is_file() and '.min.' not in file_path.name:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                # Simple heuristics for minification potential
                has_comments = '/*' in content or '//' in content
                has_whitespace = '  ' in content or '\n\n' in content
                
                if has_comments or has_whitespace:
                    self.results['optimization_recommendations'].append({
                        'file': str(file_path.name),
                        'issue': 'File not minified',
                        'recommendation': 'Minify to reduce file size by 20-40%'
                    })
    
    def analyze_image_optimization(self):
        """Analyze image files for optimization opportunities"""
        print("🖼️  Analyzing images...")
        
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.jfif']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(self.static_path.glob(f'**/*{ext}'))
        
        for img_path in image_files:
            if img_path.is_file():
                size = img_path.stat().st_size
                
                self.results['file_analysis'][str(img_path.relative_to(self.base_path))] = {
                    'type': 'Image',
                    'size_bytes': size,
                    'size_kb': round(size / 1024, 2)
                }
                
                if size > 500 * 1024:  # > 500KB
                    self.results['optimization_recommendations'].append({
                        'file': str(img_path.name),
                        'issue': f'Large image file ({round(size/1024, 2)}KB)',
                        'recommendation': 'Compress image and consider WebP format'
                    })
    
    def check_caching_headers(self):
        """Check if Django settings have proper caching configuration"""
        print("💾 Checking caching configuration...")
        
        settings_path = self.base_path / 'Stroke' / 'settings.py'
        if settings_path.exists():
            content = settings_path.read_text()
            
            has_cache_middleware = 'CacheMiddleware' in content
            has_static_cache = 'STATICFILES_STORAGE' in content
            
            if not has_cache_middleware:
                self.results['optimization_recommendations'].append({
                    'file': 'settings.py',
                    'issue': 'No cache middleware configured',
                    'recommendation': 'Add Django cache middleware for better performance'
                })
    
    def analyze_template_loading(self):
        """Analyze template structure for loading optimization"""
        print("📄 Analyzing templates...")
        
        template_path = self.base_path / 'StrokeApp' / 'templates'
        templates = list(template_path.glob('*.html'))
        
        for template in templates:
            if template.is_file():
                content = template.read_text(encoding='utf-8', errors='ignore')
                
                # Check for blocking scripts
                if '<script src=' in content and 'defer' not in content and 'async' not in content:
                    self.results['optimization_recommendations'].append({
                        'file': str(template.name),
                        'issue': 'Scripts without defer/async attributes',
                        'recommendation': 'Add defer or async to non-critical scripts'
                    })
                
                # Check for inline styles
                if 'style=' in content:
                    self.results['optimization_recommendations'].append({
                        'file': str(template.name),
                        'issue': 'Inline styles detected',
                        'recommendation': 'Move inline styles to external CSS'
                    })
    
    def calculate_performance_score(self):
        """Calculate overall performance score"""
        print("📈 Calculating performance score...")
        
        total_issues = len(self.results['optimization_recommendations'])
        total_files = len(self.results['file_analysis'])
        
        # Simple scoring algorithm
        if total_issues == 0:
            score = 100
        else:
            score = max(0, 100 - (total_issues * 5))
        
        self.results['performance_metrics'] = {
            'overall_score': score,
            'total_files_analyzed': total_files,
            'total_issues_found': total_issues,
            'status': 'Excellent' if score >= 90 else 'Good' if score >= 70 else 'Needs Improvement'
        }
    
    def generate_report(self):
        """Generate comprehensive performance report"""
        print("\n" + "="*80)
        print("🎯 PERFORMANCE AUDIT REPORT")
        print("="*80)
        
        metrics = self.results['performance_metrics']
        print(f"\n📊 Overall Performance Score: {metrics['overall_score']}/100 ({metrics['status']})")
        print(f"📁 Files Analyzed: {metrics['total_files_analyzed']}")
        print(f"⚠️  Issues Found: {metrics['total_issues_found']}")
        
        if self.results['optimization_recommendations']:
            print("\n🔧 OPTIMIZATION RECOMMENDATIONS:")
            print("-" * 80)
            
            for i, rec in enumerate(self.results['optimization_recommendations'], 1):
                print(f"\n{i}. {rec['file']}")
                print(f"   Issue: {rec['issue']}")
                print(f"   Recommendation: {rec['recommendation']}")
        
        print("\n" + "="*80)
        
        # Save detailed report
        report_path = self.base_path / 'performance_audit_report.json'
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✅ Detailed report saved to: {report_path}")
    
    def run_audit(self):
        """Run complete performance audit"""
        print("🚀 Starting Performance Audit...\n")
        
        self.analyze_file_sizes()
        self.check_minification_potential()
        self.analyze_image_optimization()
        self.check_caching_headers()
        self.analyze_template_loading()
        self.calculate_performance_score()
        self.generate_report()

if __name__ == '__main__':
    base_path = Path(__file__).parent
    auditor = PerformanceAuditor(base_path)
    auditor.run_audit()
