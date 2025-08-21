"""
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
