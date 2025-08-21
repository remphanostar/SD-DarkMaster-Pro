#!/usr/bin/env python3
"""
Set up a Colab-like environment for testing SD-DarkMaster-Pro
"""
import os
import sys
import subprocess
from pathlib import Path

print("🎯 Setting up Colab-like testing environment...")

# 1. Create /content directory structure (Colab's default)
content_dir = Path('/content')
if not content_dir.exists():
    print("📁 Creating /content directory (requires sudo)...")
    subprocess.run(['sudo', 'mkdir', '-p', '/content'], check=True)
    subprocess.run(['sudo', 'chmod', '777', '/content'], check=True)

# 2. Create symlink from /content to our project
sd_darkmaster_link = Path('/content/SD-DarkMaster-Pro')
if not sd_darkmaster_link.exists():
    print("🔗 Creating symlink /content/SD-DarkMaster-Pro -> /workspace/SD-DarkMaster-Pro")
    subprocess.run(['sudo', 'ln', '-sf', '/workspace/SD-DarkMaster-Pro', '/content/SD-DarkMaster-Pro'], check=True)

# 3. Create mock google.colab module
mock_colab_path = Path('/workspace/google_colab_mock')
mock_colab_path.mkdir(exist_ok=True)

# Create __init__.py for google package
google_init = mock_colab_path / '__init__.py'
google_init.write_text('')

# Create colab subpackage
colab_dir = mock_colab_path / 'colab'
colab_dir.mkdir(exist_ok=True)

# Create colab module with Colab-like features
colab_init = colab_dir / '__init__.py'
colab_init.write_text('''"""
Mock google.colab module for testing Colab-specific code
"""

class _MockAuth:
    def authenticate_user(self):
        print("[Mock] Authenticating user...")
        
class _MockDrive:
    def mount(self, path, force_remount=False):
        print(f"[Mock] Mounting drive at {path}")
        
class _MockFiles:
    def upload(self):
        print("[Mock] File upload dialog")
        return {}
    
    def download(self, path):
        print(f"[Mock] Downloading {path}")

class _MockOutput:
    def clear(self):
        print("[Mock] Clearing output")
    
    def enable_custom_widget_manager(self):
        print("[Mock] Enabling custom widget manager")

# Mock modules
auth = _MockAuth()
drive = _MockDrive()
files = _MockFiles()
output = _MockOutput()

# Indicate we're in Colab environment
IN_COLAB = True

print("🎭 Mock google.colab module loaded - simulating Colab environment")
''')

print("✅ Created mock google.colab module")

# 4. Install Colab-specific dependencies
print("\n📦 Installing Colab-specific dependencies...")
deps = [
    'pyngrok',  # For ngrok tunneling
    'ipywidgets',  # For Colab widgets
    'nest-asyncio',  # For async in notebooks
]

for dep in deps:
    print(f"  Installing {dep}...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', dep, '-q'], check=False)

# 5. Create test runner script
test_script = Path('/workspace/test_as_colab.py')
test_script.write_text('''#!/usr/bin/env python3
"""
Test SD-DarkMaster-Pro notebook as if running in Colab
"""
import sys
import os
from pathlib import Path

# Add mock google.colab to path FIRST
sys.path.insert(0, '/workspace/google_colab_mock')

# Now we can import and it will detect as Colab
import subprocess
import time

print("🧪 Testing SD-DarkMaster-Pro in Colab-like environment")
print("="*60)

# Test platform detection
try:
    import google.colab
    print("✅ google.colab module detected (mock)")
except ImportError:
    print("❌ google.colab module not found")

# Change to content directory (like Colab)
os.chdir('/content')
print(f"📍 Working directory: {os.getcwd()}")

# Test with papermill
print("\\n🎯 Testing notebook with papermill (Colab mode)...")
result = subprocess.run([
    'timeout', '120',
    sys.executable, '-m', 'papermill',
    '/workspace/SD-DarkMaster-Pro/notebook/SD-DarkMaster-Pro.ipynb',
    '/workspace/SD-DarkMaster-Pro/notebook/SD-DarkMaster-Pro-colab-test.ipynb',
    '--kernel', 'python3'
], capture_output=True, text=True)

if result.returncode == 0:
    print("✅ Notebook executed successfully in Colab mode!")
else:
    print(f"❌ Notebook execution failed: {result.returncode}")
    if result.stdout:
        print("STDOUT:", result.stdout[-1000:])  # Last 1000 chars
    if result.stderr:
        print("STDERR:", result.stderr[-1000:])

print("\\n💡 To run individual cells in Colab mode:")
print("   1. Start Python: python3")
print("   2. Run: import sys; sys.path.insert(0, '/workspace/google_colab_mock')")
print("   3. Now 'google.colab' will be detected")
''')

test_script.chmod(0o755)
print(f"✅ Created test script: {test_script}")

# 6. Create environment report
print("\n" + "="*60)
print("📊 COLAB-LIKE ENVIRONMENT SETUP COMPLETE")
print("="*60)
print("✅ /content directory created and linked")
print("✅ Mock google.colab module installed")
print("✅ Colab dependencies installed (pyngrok, ipywidgets, nest-asyncio)")
print("✅ Test script created: /workspace/test_as_colab.py")
print("\n🎯 To test in Colab mode:")
print("   python3 /workspace/test_as_colab.py")
print("\n🔧 To use mock in Python:")
print("   import sys")
print("   sys.path.insert(0, '/workspace/google_colab_mock')")
print("   import google.colab  # Will now work!")
print("="*60)
