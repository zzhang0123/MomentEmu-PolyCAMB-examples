#!/usr/bin/env python3
"""
Setup script for MomentEmu PolyCAMB Examples

This script helps set up the environment and dependencies needed
to run the PolyCAMB examples.
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def install_requirements():
    """Install required packages."""
    print("Installing requirements...")
    success, output = run_command("pip install -r requirements.txt")
    if success:
        print("✓ Requirements installed successfully")
    else:
        print(f"✗ Error installing requirements: {output}")
        return False
    return True

def check_dependencies():
    """Check if key dependencies are available."""
    dependencies = ['numpy', 'scipy', 'matplotlib', 'camb', 'MomentEmu']
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✓ {dep} is available")
        except ImportError:
            print(f"✗ {dep} is missing")
            missing.append(dep)
    
    return len(missing) == 0, missing

def main():
    """Main setup function."""
    print("🚀 Setting up MomentEmu PolyCAMB Examples\n")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    print("\nChecking dependencies...")
    deps_ok, missing = check_dependencies()
    
    if not deps_ok:
        print(f"\n⚠️  Missing dependencies: {missing}")
        print("Please install them manually or check the requirements.txt file")
        sys.exit(1)
    
    print("\n✅ Setup complete! You can now:")
    print("   1. Run 'jupyter notebook notebooks/poly_camb.ipynb' for tutorials")
    print("   2. Use the pre-trained emulators in the emulators/ directory") 
    print("   3. Generate your own training data using PolyCAMB.py functions")
    print("\n📖 See README.md for detailed usage instructions")

if __name__ == "__main__":
    main()
