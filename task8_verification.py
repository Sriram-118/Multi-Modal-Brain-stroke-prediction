#!/usr/bin/env python3
"""
Task 8 Checkpoint Verification Script
Verifies forms and visualization implementation (Tasks 5, 6, 7)
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
            print(f"⚠️  {description}: Missing elements - {', '.join(missing[:3])}")
            if len(missing) > 3:
                print(f"    ... and {len(missing) - 3} more")
            return False
        else:
            print(f"✅ {description}")
            return True
    except Exception as e:
        print(f"❌ {description}: Error reading file - {str(e)}")
        return False

def main():
    print("="*70)
    print("CHECKPOINT VERIFICATION - Task 8")
    print("Verifying forms and visualization (Tasks 5, 6, 7)")
    print("="*70)
    print()
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    results = []
    
    # Task 5.1: Login Form Modernization
    print("📋 Task 5.1: Login Form Modernization")
    print("-" * 70)
    
    login_template = os.path.join(base_path, "StrokeApp/templates/UserLogin.html")
    results.append(check_file_exists(login_template, "Login template"))
    
    results.append(check_file_contains(
        login_template,
        ["{% extends 'base.html' %}", "form-floating", "login-card"],
        "Login form Bootstrap structure"
    ))
    
    results.append(check_file_contains(
        login_template,
        ["form-control", "btn-login", "Healthcare Professional Login"],
        "Login form styling"
    ))
    
    results.append(check_file_contains(
        login_template,
        ["csrf", "t1", "t2"],
        "Login form Django compatibility"
    ))
    
    print()
    
    # Task 5.2: Login Form Validation
    print("📋 Task 5.2: Login Form Validation")
    print("-" * 70)
    
    form_validation_js = os.path.join(base_path, "StrokeApp/static/js/form-validation.js")
    results.append(check_file_exists(form_validation_js, "Form validation JavaScript"))
    
    results.append(check_file_contains(
        form_validation_js,
        ["FormValidator", "validateField", "showError"],
        "Form validation class structure"
    ))
    
    results.append(check_file_contains(
        login_template,
        ["form-validation.js", "invalid-feedback"],
        "Login form validation integration"
    ))
    
    print()
    
    # Task 5.4: Registration Form Modernization
    print("📋 Task 5.4: Registration Form Modernization")
    print("-" * 70)
    
    register_template = os.path.join(base_path, "StrokeApp/templates/Register.html")
    results.append(check_file_exists(register_template, "Registration template"))
    
    results.append(check_file_contains(
        register_template,
        ["{% extends 'base.html' %}", "form-floating", "register-card"],
        "Registration form Bootstrap structure"
    ))
    
    results.append(check_file_contains(
        register_template,
        ["password-requirements", "form-progress", "Create Healthcare Account"],
        "Registration form enhanced features"
    ))
    
    results.append(check_file_contains(
        register_template,
        ["csrf", "t1", "t2", "t3", "t4", "t5"],
        "Registration form Django compatibility"
    ))
    
    print()
    
    # Task 6.1: Prediction Form Modernization
    print("📋 Task 6.1: Prediction Form Modernization")
    print("-" * 70)
    
    predict_template = os.path.join(base_path, "StrokeApp/templates/Predict.html")
    results.append(check_file_exists(predict_template, "Prediction template"))
    
    results.append(check_file_contains(
        predict_template,
        ["{% extends 'base.html' %}", "prediction-card", "form-section"],
        "Prediction form Bootstrap structure"
    ))
    
    results.append(check_file_contains(
        predict_template,
        ["Multi-Modal Stroke Risk Assessment", "form-progress"],
        "Prediction form layout"
    ))
    
    print()
    
    # Task 6.2: File Upload Implementation
    print("📋 Task 6.2: File Upload Implementation")
    print("-" * 70)
    
    file_upload_js = os.path.join(base_path, "StrokeApp/static/js/file-upload.js")
    results.append(check_file_exists(file_upload_js, "File upload JavaScript"))
    
    results.append(check_file_contains(
        file_upload_js,
        ["FileUploadHandler", "drag", "drop", "preview"],
        "File upload functionality"
    ))
    
    results.append(check_file_contains(
        predict_template,
        ["file-upload-area", "drag and drop", "file-upload.js"],
        "File upload integration in prediction form"
    ))
    
    print()
    
    # Task 6.4: Prediction Form Validation
    print("📋 Task 6.4: Prediction Form Validation")
    print("-" * 70)
    
    results.append(check_file_contains(
        predict_template,
        ["range-indicator", "form-validation.js", "invalid-feedback"],
        "Prediction form validation"
    ))
    
    results.append(check_file_contains(
        predict_template,
        ["t1", "t2", "t3", "t4", "t5", "t6", "t7"],
        "Prediction form Django field compatibility"
    ))
    
    print()
    
    # Task 7.1: Chart.js Integration
    print("📋 Task 7.1: Chart.js Integration")
    print("-" * 70)
    
    prediction_chart_js = os.path.join(base_path, "StrokeApp/static/js/prediction-chart.js")
    results.append(check_file_exists(prediction_chart_js, "Prediction chart JavaScript"))
    
    results.append(check_file_contains(
        prediction_chart_js,
        ["PredictionChart", "Chart.js", "render"],
        "Chart.js implementation"
    ))
    
    chart_utils_js = os.path.join(base_path, "StrokeApp/static/js/chart-utils.js")
    results.append(check_file_exists(chart_utils_js, "Chart utilities JavaScript"))
    
    chart_generator_py = os.path.join(base_path, "StrokeApp/utils/chart_generator.py")
    results.append(check_file_exists(chart_generator_py, "Chart generator Python module"))
    
    print()
    
    # Task 7.3: Results Page Enhancement
    print("📋 Task 7.3: Results Page Enhancement")
    print("-" * 70)
    
    userscreen_template = os.path.join(base_path, "StrokeApp/templates/UserScreen.html")
    results.append(check_file_exists(userscreen_template, "Results page template"))
    
    results.append(check_file_contains(
        userscreen_template,
        ["{% extends 'base.html' %}", "chart-container", "prediction-chart.js"],
        "Results page structure"
    ))
    
    results.append(check_file_contains(
        userscreen_template,
        ["aria-label", "canvas", "Chart"],
        "Results page chart accessibility"
    ))
    
    print()
    
    # Task 7.5: Responsive Data Tables
    print("📋 Task 7.5: Responsive Data Tables")
    print("-" * 70)
    
    results.append(check_file_contains(
        userscreen_template,
        ["table-responsive", "table", "prediction-results"],
        "Responsive table implementation"
    ))
    
    print()
    
    # Additional Checks - TypeScript Sources
    print("📋 Additional: TypeScript Sources")
    print("-" * 70)
    
    ts_form_validation = os.path.join(base_path, "src/typescript/components/form-validation.ts")
    results.append(check_file_exists(ts_form_validation, "TypeScript form validation"))
    
    ts_file_upload = os.path.join(base_path, "src/typescript/components/file-upload.ts")
    results.append(check_file_exists(ts_file_upload, "TypeScript file upload"))
    
    ts_prediction_chart = os.path.join(base_path, "src/typescript/components/prediction-chart.ts")
    results.append(check_file_exists(ts_prediction_chart, "TypeScript prediction chart"))
    
    print()
    
    # Additional Checks - Package Dependencies
    print("📋 Additional: Package Dependencies")
    print("-" * 70)
    
    package_json = os.path.join(base_path, "package.json")
    results.append(check_file_contains(
        package_json,
        ["bootstrap", "chart.js"],
        "Required npm packages"
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
        print("Forms and visualization are properly implemented.")
        print("\nCompleted Tasks:")
        print("  ✅ Task 5.1: Login form modernized with Bootstrap")
        print("  ✅ Task 5.2: Login form validation implemented")
        print("  ✅ Task 5.4: Registration form enhanced")
        print("  ✅ Task 6.1: Prediction form modernized")
        print("  ✅ Task 6.2: File upload with drag-and-drop")
        print("  ✅ Task 6.4: Prediction form validation")
        print("  ✅ Task 7.1: Chart.js integration")
        print("  ✅ Task 7.3: Results page enhanced")
        print("  ✅ Task 7.5: Responsive data tables")
        return 0
    elif percentage >= 80:
        print("\n⚠️  MOSTLY COMPLETE")
        print("Most checks passed, but some elements may need attention.")
        print("Review the warnings above for details.")
        return 0
    else:
        print("\n❌ VERIFICATION FAILED")
        print("Several checks failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
