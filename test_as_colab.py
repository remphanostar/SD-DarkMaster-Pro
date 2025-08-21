#!/usr/bin/env python3
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
    print("🎭 Mock modules available: auth, drive, files, output")
except ImportError:
    print("❌ google.colab module not found")

# Change to content directory (like Colab)
os.chdir('/content')
print(f"📍 Working directory: {os.getcwd()}")
print(f"📁 /content/SD-DarkMaster-Pro -> {os.path.realpath('/content/SD-DarkMaster-Pro')}")

# Test with papermill
print("\n🎯 Testing notebook with papermill (Colab mode)...")

# Set PYTHONPATH to include mock module
env = os.environ.copy()
env['PYTHONPATH'] = '/workspace/google_colab_mock:' + env.get('PYTHONPATH', '')

result = subprocess.run([
    'timeout', '120',
    sys.executable, '-m', 'papermill',
    '/workspace/notebook/SD-DarkMaster-Pro.ipynb',  # Correct path
    '/workspace/notebook/SD-DarkMaster-Pro-colab-test.ipynb',
    '--kernel', 'python3'
], capture_output=True, text=True, env=env)

if result.returncode == 0:
    print("✅ Notebook executed successfully in Colab mode!")
    print("\n📊 Output notebook: /workspace/notebook/SD-DarkMaster-Pro-colab-test.ipynb")
else:
    print(f"❌ Notebook execution failed: {result.returncode}")
    if result.returncode == 124:
        print("⏱️ Execution timed out (>120 seconds)")
    if result.stdout:
        print("\nSTDOUT (last 1000 chars):")
        print(result.stdout[-1000:])
    if result.stderr:
        print("\nSTDERR (last 1000 chars):")
        print(result.stderr[-1000:])

print("\n💡 To run individual cells in Colab mode:")
print("   1. Start Python: python3")
print("   2. Run: import sys; sys.path.insert(0, '/workspace/google_colab_mock')")
print("   3. Run: import google.colab  # Will now work!")
print("   4. Execute notebook cells")
