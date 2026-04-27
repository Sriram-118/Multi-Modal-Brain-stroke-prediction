#!/usr/bin/env python3
"""
Frontend Infrastructure Setup Script
Helps set up the modern frontend infrastructure for the Stroke Prediction application
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def print_step(step, text):
    """Print a formatted step"""
    print(f"\n[{step}] {text}")

def check_node_npm():
    """Check if Node.js and npm are installed"""
    try:
        node_version = subprocess.check_output(['node', '--version'], stderr=subprocess.DEVNULL).decode().strip()
        npm_version = subprocess.check_output(['npm', '--version'], stderr=subprocess.DEVNULL).decode().strip()
        print(f"✓ Node.js {node_version} found")
        print(f"✓ npm {npm_version} found")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Node.js and/or npm not found")
        print("Please install Node.js from https://nodejs.org/")
        return False

def install_npm_dependencies():
    """Install npm dependencies"""
    try:
        print("Installing npm dependencies...")
        subprocess.check_call(['npm', 'install'], stdout=subprocess.DEVNULL)
        print("✓ npm dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install npm dependencies")
        return False

def compile_typescript():
    """Compile TypeScript files"""
    try:
        print("Compiling TypeScript files...")
        subprocess.check_call(['npm', 'run', 'build'], stdout=subprocess.DEVNULL)
        print("✓ TypeScript compiled successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to compile TypeScript")
        print("Note: This is optional - JavaScript files are already provided")
        return False

def verify_static_files():
    """Verify that static files are in place"""
    static_dir = Path('StrokeApp/static')
    required_files = [
        'css/modern.css',
        'js/modern.js',
        'js/chart-utils.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = static_dir / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def verify_templates():
    """Verify that template files are in place"""
    templates_dir = Path('StrokeApp/templates')
    required_files = [
        'base.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = templates_dir / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def create_directories():
    """Create necessary directories"""
    directories = [
        'StrokeApp/static/css',
        'StrokeApp/static/js',
        'StrokeApp/static/js/compiled',
        'StrokeApp/static/images',
        'src/typescript/components',
        'src/typescript/utils'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def main():
    """Main setup function"""
    print_header("Stroke Prediction - Frontend Infrastructure Setup")
    
    # Change to the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print_step(1, "Checking prerequisites")
    if not check_node_npm():
        print("\nSetup cannot continue without Node.js and npm.")
        print("Please install Node.js and run this script again.")
        sys.exit(1)
    
    print_step(2, "Creating directories")
    create_directories()
    
    print_step(3, "Verifying static files")
    if not verify_static_files():
        print("Some static files are missing. Please ensure all files are properly created.")
    
    print_step(4, "Verifying templates")
    if not verify_templates():
        print("Some template files are missing. Please ensure all files are properly created.")
    
    print_step(5, "Installing npm dependencies")
    if os.path.exists('package.json'):
        install_npm_dependencies()
    else:
        print("package.json not found - skipping npm install")
    
    print_step(6, "Compiling TypeScript (optional)")
    if os.path.exists('tsconfig.json'):
        compile_typescript()
    else:
        print("tsconfig.json not found - skipping TypeScript compilation")
    
    print_header("Setup Complete!")
    print("\nNext steps:")
    print("1. Run Django development server: python manage.py runserver")
    print("2. Visit http://127.0.0.1:8000 to see the modernized UI")
    print("3. Check the README-Frontend.md for detailed documentation")
    
    print("\nOptional development commands:")
    print("- npm run watch    # Watch TypeScript files for changes")
    print("- npm run lint     # Lint JavaScript files")
    print("- npm run format   # Format code with Prettier")
    
    print("\nFor any issues, refer to the documentation or check the console for errors.")

if __name__ == "__main__":
    main()