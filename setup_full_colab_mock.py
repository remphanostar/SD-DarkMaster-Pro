#!/usr/bin/env python3
"""
Create a full Colab mock environment with proper file structure
"""
import os
import sys
import subprocess
from pathlib import Path
import shutil

print("🎯 Setting up FULL Colab mock environment...")

# 1. Copy the entire SD-DarkMaster-Pro to /content (not symlink)
content_dir = Path('/content')
if not content_dir.exists():
    subprocess.run(['sudo', 'mkdir', '-p', '/content'], check=True)
    subprocess.run(['sudo', 'chmod', '777', '/content'], check=True)

# Remove old symlink if exists
sd_path = Path('/content/SD-DarkMaster-Pro')
if sd_path.is_symlink():
    print("🗑️ Removing old symlink...")
    subprocess.run(['sudo', 'rm', str(sd_path)], check=True)

# Copy the project to /content (like Colab would clone it)
if not sd_path.exists():
    print("📦 Copying SD-DarkMaster-Pro to /content...")
    subprocess.run(['sudo', 'cp', '-r', '/workspace/SD-DarkMaster-Pro', '/content/'], check=True)
    subprocess.run(['sudo', 'chmod', '-R', '777', '/content/SD-DarkMaster-Pro'], check=True)
    print("✅ Project copied to /content/SD-DarkMaster-Pro")

# 2. Create enhanced mock google.colab module
mock_path = Path('/workspace/google_colab_mock')
mock_path.mkdir(exist_ok=True)

# Create setup.py for the mock package
setup_py = mock_path / 'setup.py'
setup_py.write_text('''
from setuptools import setup, find_packages

setup(
    name='google-colab-mock',
    version='1.0.0',
    packages=['google', 'google.colab'],
)
''')

# Create google package
google_dir = mock_path / 'google'
google_dir.mkdir(exist_ok=True)
(google_dir / '__init__.py').write_text('__path__ = __import__("pkgutil").extend_path(__path__, __name__)')

# Create enhanced colab module
colab_dir = google_dir / 'colab'
colab_dir.mkdir(exist_ok=True)
(colab_dir / '__init__.py').write_text('''"""
Enhanced mock google.colab module for realistic Colab testing
"""
import os
import sys

class _MockAuth:
    def authenticate_user(self):
        print("[Mock Colab] Authenticating user...")
        
class _MockDrive:
    def mount(self, path, force_remount=False):
        print(f"[Mock Colab] Mounting Google Drive at {path}")
        os.makedirs(path, exist_ok=True)
        
class _MockFiles:
    def upload(self):
        print("[Mock Colab] Opening file upload dialog...")
        return {}
    
    def download(self, path):
        print(f"[Mock Colab] Downloading {path}")

class _MockOutput:
    def clear(self):
        print("[Mock Colab] Clearing output")
    
    def enable_custom_widget_manager(self):
        print("[Mock Colab] Enabling custom widget manager")

# Mock modules
auth = _MockAuth()
drive = _MockDrive()
files = _MockFiles()
output = _MockOutput()

# Indicate we're in Colab environment
IN_COLAB = True
print("🎭 Google Colab environment detected (mock)")
''')

# Install the mock package
print("📦 Installing mock google.colab package...")
subprocess.run([sys.executable, '-m', 'pip', 'install', '-e', str(mock_path)], 
               capture_output=True, check=True)

print("\n✅ FULL Colab mock environment ready!")
print("📁 Project available at: /content/SD-DarkMaster-Pro")
print("🎭 google.colab module installed system-wide")
