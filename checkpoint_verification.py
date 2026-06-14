#!/usr/bin/env python3
"""
Checkpoint Verification Script for Task 4
Verifies base structure and home page implementation
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and report"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MISSING: {filepath}")
        return False

def check_file_contains(filepath, search_strings, description):
    """Check if a file contains specific strings"""
    if not os.path.exists(filepath):
        print(f"❌ {description}: File not found - {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        missing = []
        for search_str in search_strings:
            if search_str not in content:
                missing.append(search_str)
        
        if missing:
            print(f"⚠️  {description}: Missing elements - {', '.join(missing)}")
            return False
        else:
            print(f"✅ {description}")
            return True
    except Exception as e:
        print(f"❌ {description}: Error reading file - {str(e)}")
        return False

def main():
    print("="*70)
    print("CHECKPOINT VERIFICATION - Task 4")
    print("Verifying base structure and home page modernization")
    print("="*70)
    print()
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    results = []
    
    # Task 1: Base Infrastructure
    print("📋 Task 1: Base Infrastructure")
    print("-" * 70)
    
    results.append(check_file_exists(
        os.path.join(base_path, "StrokeApp/templates/base.html"),
        "Base template"
    ))
    
    results.append(check_file_exists(
        os.path.join(base_path, "StrokeApp/static/css/modern.css"),
        "Modern CSS"
    ))
    
    results.append(check_file_exists(
        os.path.join(base_path, "StrokeApp/static/js/modern.js"),
        "Modern JavaScript"
    ))
    
    results.append(check_file_exists(
        os.path.join(base_path, "package.json"),
        "Package.json (npm configuration)"
    ))
    
    results.append(check_file_exists(
        os.path.join(base_path, "tsconfig.json"),
        "TypeScript configuration"
    ))
    
    print()
    
    # Task 2.1: Base Template with Navigation
    print("📋 Task 2.1: Base Template with Navigation")
    print("-" * 70)
    
    base_template = os.path.join(base_path, "StrokeApp/templates/base.html")
    results.append(check_file_contains(
        base_template,
        ["<!DOCTYPE html>", "navbar", "navbar-toggler", "Bootstrap", "modern.css"],
        "Base template structure"
    ))
    
    results.append(check_file_contains(
        base_template,
        ["aria-label", "role=", "Skip to main content"],
        "Accessibility features"
    ))
    
    results.append(check_file_contains(
        base_template,
        ["navbar-nav", "nav-link", "active"],
        "Navigation structure"
    ))
    
    print()
    
    # Task 2.3: Active Page Indication
    print("📋 Task 2.3: Active Page Indication")
    print("-" * 70)
    
    results.append(check_file_contains(
        base_template,
        ["nav-link active", "aria-current"],
        "Active page indication"
    ))
    
    results.append(check_file_contains(
        os.path.join(base_path, "StrokeApp/static/css/modern.css"),
        [".nav-link.active", ".nav-item.active"],
        "Active state CSS"
    ))
    
    print()
    
    # Task 3.1: Home Page Modernization
    print("📋 Task 3.1: Home Page Modernization")
    print("-" * 70)
    
    index_template = os.path.join(base_path, "StrokeApp/templates/index.html")
    results.append(check_file_exists(index_template, "Home page template"))
    
    results.append(check_file_contains(
        index_template,
        ["{% extends 'base.html' %}", "hero-section", "feature-card", "Bootstrap"],
        "Home page structure"
    ))
    
    results.append(check_file_contains(
        index_template,
        ["col-md-", "col-lg-", "container", "row"],
        "Responsive grid system"
    ))
    
    results.append(check_file_contains(
        index_template,
        ["Multi-Modal Stroke Prediction", "CNN", "LSTM"],
        "Content elements"
    ))
    
    print()
    
    # Task 3.3: Loading States and Transitions
    print("📋 Task 3.3: Loading States and Transitions")
    print("-" * 70)
    
    results.append(check_file_contains(
        os.path.join(base_path, "StrokeApp/static/css/modern.css"),
        ["loading-overlay", "loading-spinner", "@keyframes", "transition"],
        "Loading states CSS"
    ))
    
    results.append(check_file_contains(
        os.path.join(base_path, "StrokeApp/static/js/modern.js"),
        ["LoadingManager", "show", "hide"],
        "Loading manager JavaScript"
    ))
    
    print()
    
    # Additional Checks
    print("📋 Additional Verification")
    print("-" * 70)
    
    results.append(check_file_exists(
        os.path.join(base_path, "StrokeApp/static/js/navigation.js"),
        "Navigation JavaScript"
    ))
    
    results.append(check_file_exists(
        os.path.join(base_path, "StrokeApp/static/js/form-validation.js"),
        "Form validation JavaScript"
    ))
    
    results.append(check_file_exists(
        os.path.join(base_path, "StrokeApp/static/js/accessibility.js"),
        "Accessibility JavaScript"
    ))
    
    results.append(check_file_exists(
        os.path.join(base_path, "StrokeApp/static/js/polyfills.js"),
        "Browser polyfills"
    ))
    
    results.append(check_file_exists(
        os.path.join(base_path, "StrokeApp/static/css/browser-fallbacks.css"),
        "Browser fallbacks CSS"
    ))
    
    print()
    
    # Summary
    print("="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    print(f"Checks Passed: {passed}/{total} ({percentage:.1f}%)")
    
    if passed == total:
        print("\n✅ ALL CHECKS PASSED!")
        print("Base structure and home page are properly implemented.")
        return 0
    elif percentage >= 80:
        print("\n⚠️  MOSTLY COMPLETE")
        print("Most checks passed, but some elements may need attention.")
        return 0
    else:
        print("\n❌ VERIFICATION FAILED")
        print("Several checks failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
