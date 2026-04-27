#!/usr/bin/env python3
"""
Asset Optimization Script
Minifies CSS and JavaScript files for production deployment
"""

import re
import os
from pathlib import Path

class AssetOptimizer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.static_path = self.base_path / 'StrokeApp' / 'static'
        self.optimized_count = 0
    
    def minify_css(self, content):
        """Minify CSS content"""
        # Remove comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # Remove whitespace
        content = re.sub(r'\s+', ' ', content)
        # Remove spaces around special characters
        content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', content)
        # Remove trailing semicolons
        content = re.sub(r';}', '}', content)
        return content.strip()
    
    def minify_js(self, content):
        """Minify JavaScript content (basic minification)"""
        # Remove single-line comments (but preserve URLs)
        content = re.sub(r'(?<!:)//.*?$', '', content, flags=re.MULTILINE)
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # Remove excessive whitespace (but preserve string literals)
        lines = content.split('\n')
        minified_lines = []
        for line in lines:
            line = line.strip()
            if line:
                minified_lines.append(line)
        content = '\n'.join(minified_lines)
        return content
    
    def optimize_file(self, file_path):
        """Optimize a single file"""
        if '.min.' in file_path.name:
            print(f"⏭️  Skipping already minified: {file_path.name}")
            return
        
        try:
            content = file_path.read_text(encoding='utf-8')
            original_size = len(content)
            
            # Determine file type and minify
            if file_path.suffix == '.css':
                minified = self.minify_css(content)
                file_type = 'CSS'
            elif file_path.suffix == '.js':
                minified = self.minify_js(content)
                file_type = 'JavaScript'
            else:
                return
            
            minified_size = len(minified)
            savings = ((original_size - minified_size) / original_size) * 100
            
            # Create minified version
            min_path = file_path.parent / f"{file_path.stem}.min{file_path.suffix}"
            min_path.write_text(minified, encoding='utf-8')
            
            print(f"✅ Optimized {file_type}: {file_path.name}")
            print(f"   Original: {original_size:,} bytes")
            print(f"   Minified: {minified_size:,} bytes")
            print(f"   Savings: {savings:.1f}%")
            print(f"   Output: {min_path.name}\n")
            
            self.optimized_count += 1
            
        except Exception as e:
            print(f"❌ Error optimizing {file_path.name}: {e}\n")
    
    def optimize_all(self):
        """Optimize all CSS and JS files"""
        print("🚀 Starting Asset Optimization...\n")
        print("="*80)
        
        # Optimize CSS files
        print("\n📝 Optimizing CSS Files:")
        print("-"*80)
        css_files = list(self.static_path.glob('css/*.css'))
        for css_file in css_files:
            self.optimize_file(css_file)
        
        # Optimize JS files
        print("\n📝 Optimizing JavaScript Files:")
        print("-"*80)
        js_files = list(self.static_path.glob('js/*.js'))
        for js_file in js_files:
            if js_file.parent.name != 'compiled':  # Skip compiled TypeScript
                self.optimize_file(js_file)
        
        print("="*80)
        print(f"\n✨ Optimization Complete!")
        print(f"📊 Total files optimized: {self.optimized_count}")
        print(f"💡 Minified files created with .min.css and .min.js extensions")
        print(f"📌 Update templates to use minified versions in production\n")

if __name__ == '__main__':
    base_path = Path(__file__).parent
    optimizer = AssetOptimizer(base_path)
    optimizer.optimize_all()
