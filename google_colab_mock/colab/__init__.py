"""
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
