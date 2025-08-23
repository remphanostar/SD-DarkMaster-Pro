#!/usr/bin/env python3
"""Streamlit launcher with ngrok for Colab - Cell 2"""
import os, sys, subprocess, time
from pathlib import Path

# Get the correct scripts directory
try:
    project_root = Path(__file__).parent.parent
except NameError:
    # When executed from notebook - detect platform
    if os.path.exists('/content'):
        # Google Colab
        project_root = Path('/content/SD-DarkMaster-Pro')
    elif os.path.exists('/kaggle'):
        # Kaggle
        project_root = Path('/kaggle/working/SD-DarkMaster-Pro')
    elif os.path.exists('/workspace'):
        # Lightning.ai or similar
        project_root = Path('/workspace/SD-DarkMaster-Pro')
    else:
        # Local or other
        project_root = Path.home() / 'SD-DarkMaster-Pro'

print(f"📂 Project root: {project_root}")
print(f"📂 Project exists: {project_root.exists()}")
        
scripts_dir = project_root / 'scripts'
print(f"📂 Scripts dir: {scripts_dir}")
print(f"📂 Scripts exists: {scripts_dir.exists()}")

# Check if widgets-en.py exists
widgets_script = scripts_dir / 'widgets-en.py'
if not widgets_script.exists():
    print(f"❌ ERROR: {widgets_script} not found!")
    print(f"Directory contents: {list(scripts_dir.iterdir()) if scripts_dir.exists() else 'Directory does not exist'}")
    sys.exit(1)

platform = 'colab' if 'google.colab' in sys.modules else 'local'
print(f"🖥️ Platform detected: {platform}")

if platform == 'colab':
    print("🔧 Setting up ngrok for Colab...")
    try:
        # Install and setup ngrok
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyngrok', '-q'], check=True)
        from pyngrok import ngrok
        
        # Set auth token
        ngrok.set_auth_token("2tjxIXifSaGR3dMhkvhk6sZqbGo_6ZfBZLZHMbtAjfRmfoDW5")
        print("✅ Ngrok configured")
        
        # Kill old streamlit
        print("🔄 Cleaning up old processes...")
        subprocess.run(['pkill', '-f', 'streamlit'], capture_output=True)
        time.sleep(2)
        
        # Start streamlit
        print("🚀 Starting Streamlit dashboard...")
        cmd = f"streamlit run {scripts_dir}/widgets-en.py --server.port 8501 --server.headless true"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give it time to start
        print("⏳ Waiting for server to start...")
        time.sleep(8)
        
        # Check if process is still running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"❌ Streamlit failed to start!")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            sys.exit(1)
        
        # Create tunnel
        print("🌐 Creating public URL...")
        public_url = ngrok.connect(8501, "http")
        
        print("\n" + "="*60)
        print(f"✅ Dashboard ready at: {public_url}")
        print("="*60)
        print("\n📋 Next steps:")
        print("1. Click the link above to open the dashboard")
        print("2. Configure your settings")
        print("3. Click 'Save All Settings' when done")
        print("4. Then run Cell 3 to download models")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Try using Cell 2b (fallback) instead if this doesn't work")
        
else:
    print("🖥️ Running locally...")
    try:
        # For local, just run directly
        subprocess.run([sys.executable, str(scripts_dir / 'widgets-en.py')], check=True)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n💡 Try using Cell 2b (fallback) instead")