#!/usr/bin/env python3
"""
Launch SD-DarkMaster-Pro Master UI with Ngrok public URL
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from pyngrok import ngrok, conf

# Your ngrok token
NGROK_AUTH_TOKEN = "2tjxIXifSaGR3dMhkvhk6sZqbGo_6ZfBZLZHMbtAjfRmfoDW5"

# Set up ngrok configuration
conf.get_default().auth_token = NGROK_AUTH_TOKEN
conf.get_default().region = "us"  # Can change to 'eu', 'ap', 'au', 'sa', 'jp', 'in'

project_root = Path(__file__).parent

def launch_master_ui_with_ngrok():
    """Launch the Master UI with ngrok tunnel"""
    
    print("\n" + "="*60)
    print("🎨 SD-DarkMaster-Pro Master UI - Public Access")
    print("="*60 + "\n")
    
    # First, kill any existing streamlit instances
    print("🔄 Cleaning up existing instances...")
    subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
    time.sleep(2)
    
    # Start Streamlit in the background
    print("🚀 Starting Streamlit Master UI...")
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(project_root / "streamlit_master_ui.py"),
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--theme.base", "dark",
        "--theme.primaryColor", "#10B981",
        "--theme.backgroundColor", "#111827",
        "--theme.secondaryBackgroundColor", "#1F2937",
        "--theme.textColor", "#6B7280"
    ]
    
    # Start Streamlit process
    streamlit_process = subprocess.Popen(
        streamlit_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for Streamlit to start
    print("⏳ Waiting for Streamlit to initialize...")
    time.sleep(5)
    
    # Start ngrok tunnel
    print("🌐 Creating ngrok tunnel...")
    try:
        # Open tunnel on port 8501
        public_url = ngrok.connect(8501, "http")
        
        print("\n" + "="*60)
        print("✅ SUCCESS! Master UI is now publicly accessible!")
        print("="*60)
        print(f"\n🌍 PUBLIC URL: {public_url}")
        print(f"🏠 LOCAL URL: http://localhost:8501")
        print("\n📱 Share the public URL to access from anywhere!")
        print("🔒 This URL is secure and encrypted (HTTPS)")
        print("\n⚠️  Note: Free ngrok URLs change on restart")
        print("💡 Tip: The URL works on mobile devices too!")
        print("\nPress Ctrl+C to stop the server")
        print("="*60 + "\n")
        
        # Save the URL to a file for reference
        with open(project_root / "public_url.txt", "w") as f:
            f.write(f"Public URL: {public_url}\n")
            f.write(f"Local URL: http://localhost:8501\n")
            f.write(f"Created at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Keep the script running
        try:
            streamlit_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            
    except Exception as e:
        print(f"❌ Error creating ngrok tunnel: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify the auth token is correct")
        print("3. Try again in a few moments")
        
    finally:
        # Cleanup
        ngrok.kill()
        streamlit_process.terminate()
        print("✅ Cleanup complete")

def launch_config_ui_with_ngrok():
    """Launch the Config UI (simpler version) with ngrok"""
    
    print("\n" + "="*60)
    print("🎨 SD-DarkMaster-Pro Config UI - Public Access")
    print("="*60 + "\n")
    
    # Kill existing instances
    subprocess.run(["pkill", "-f", "streamlit"], capture_output=True)
    time.sleep(2)
    
    # Run the config UI launcher
    print("🚀 Starting Config UI...")
    subprocess.run([sys.executable, "scripts/config_ui_launcher.py"], 
                   capture_output=True, timeout=5)
    
    # Start ngrok
    print("🌐 Creating ngrok tunnel...")
    public_url = ngrok.connect(8501, "http")
    
    print(f"\n✅ PUBLIC URL: {public_url}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ngrok.kill()
        print("\n✅ Stopped")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ui",
        choices=["master", "config"],
        default="master",
        help="Which UI to launch (master=full control, config=simple config)"
    )
    
    args = parser.parse_args()
    
    if args.ui == "master":
        launch_master_ui_with_ngrok()
    else:
        launch_config_ui_with_ngrok()