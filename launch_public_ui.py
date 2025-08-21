#!/usr/bin/env python3
"""
Launch SD-DarkMaster-Pro Config UI with public access options
"""

import os
import sys
import subprocess
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def launch_with_tunnel(tunnel_type="localtunnel"):
    """Launch Streamlit with tunnel for public access"""
    
    print("\n" + "="*60)
    print("🎨 SD-DarkMaster-Pro Config UI - Public Access")
    print("="*60 + "\n")
    
    # First ensure the streamlit app exists
    if not (project_root / 'streamlit_config_ui.py').exists():
        print("⚠️ Creating Streamlit app first...")
        subprocess.run([sys.executable, "scripts/config_ui_launcher.py"])
    
    if tunnel_type == "localtunnel":
        print("🚀 Using Localtunnel for public access...")
        print("Installing localtunnel...")
        subprocess.run(["npm", "install", "-g", "localtunnel"], check=False)
        
        # Start Streamlit
        print("\n📱 Starting Streamlit on port 8501...")
        streamlit_cmd = [
            sys.executable, "-m", "streamlit", "run",
            "streamlit_config_ui.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--theme.base", "dark"
        ]
        
        streamlit_process = subprocess.Popen(streamlit_cmd)
        
        # Wait a moment for Streamlit to start
        import time
        time.sleep(5)
        
        # Start localtunnel
        print("\n🌐 Starting Localtunnel...")
        lt_process = subprocess.Popen(
            ["lt", "--port", "8501", "--subdomain", "sd-darkmaster"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Read the URL
        for line in lt_process.stdout:
            if "your url is:" in line.lower():
                url = line.split(":")[-1].strip()
                print(f"\n✅ PUBLIC URL: {url}")
                print("Share this URL to access from anywhere!")
                break
        
        print("\nPress Ctrl+C to stop")
        
        try:
            streamlit_process.wait()
        except KeyboardInterrupt:
            print("\n✅ Stopping services...")
            streamlit_process.terminate()
            lt_process.terminate()
    
    elif tunnel_type == "ngrok":
        print("🚀 Using Ngrok for public access...")
        print("Note: Ngrok requires authentication for persistent URLs")
        
        # Check if ngrok is installed
        try:
            subprocess.run(["ngrok", "version"], check=True, capture_output=True)
        except:
            print("Installing ngrok...")
            subprocess.run(["pip", "install", "pyngrok"])
        
        from pyngrok import ngrok
        
        # Start Streamlit
        streamlit_cmd = [
            sys.executable, "-m", "streamlit", "run",
            "streamlit_config_ui.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ]
        
        streamlit_process = subprocess.Popen(streamlit_cmd)
        
        # Start ngrok tunnel
        public_url = ngrok.connect(8501)
        print(f"\n✅ PUBLIC URL: {public_url}")
        print("Share this URL to access from anywhere!")
        
        try:
            streamlit_process.wait()
        except KeyboardInterrupt:
            print("\n✅ Stopping services...")
            ngrok.disconnect(public_url)
            streamlit_process.terminate()
    
    elif tunnel_type == "cloudflare":
        print("🚀 Using Cloudflare Tunnel (cloudflared)...")
        
        # Install cloudflared if needed
        print("Installing cloudflared...")
        subprocess.run([
            "wget", "-q",
            "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64",
            "-O", "cloudflared"
        ], check=False)
        subprocess.run(["chmod", "+x", "cloudflared"], check=False)
        
        # Start Streamlit
        streamlit_cmd = [
            sys.executable, "-m", "streamlit", "run",
            "streamlit_config_ui.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ]
        
        streamlit_process = subprocess.Popen(streamlit_cmd)
        
        # Start cloudflare tunnel
        print("\n🌐 Starting Cloudflare Tunnel...")
        cf_process = subprocess.Popen(
            ["./cloudflared", "tunnel", "--url", "http://localhost:8501"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Read the URL
        for line in cf_process.stdout:
            if "trycloudflare.com" in line:
                import re
                urls = re.findall(r'https://[^\s]+trycloudflare\.com', line)
                if urls:
                    print(f"\n✅ PUBLIC URL: {urls[0]}")
                    print("Share this URL to access from anywhere!")
                    print("Note: This URL changes each time you restart")
                    break
        
        try:
            streamlit_process.wait()
        except KeyboardInterrupt:
            print("\n✅ Stopping services...")
            streamlit_process.terminate()
            cf_process.terminate()

def launch_with_share():
    """Launch Streamlit with built-in share (requires Streamlit Cloud account)"""
    
    print("\n" + "="*60)
    print("🎨 SD-DarkMaster-Pro Config UI - Streamlit Share")
    print("="*60 + "\n")
    
    # Note: This requires the code to be in a GitHub repo and connected to Streamlit Cloud
    print("📝 To use Streamlit's built-in sharing:")
    print("1. Push your code to GitHub")
    print("2. Go to share.streamlit.io")
    print("3. Connect your GitHub repo")
    print("4. Deploy the app")
    print("\nFor now, let's use a tunnel instead...")
    
    launch_with_tunnel("cloudflare")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Launch Config UI with public access")
    parser.add_argument(
        "--tunnel",
        choices=["localtunnel", "ngrok", "cloudflare", "share"],
        default="cloudflare",
        help="Tunnel service to use"
    )
    
    args = parser.parse_args()
    
    if args.tunnel == "share":
        launch_with_share()
    else:
        launch_with_tunnel(args.tunnel)