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
    print("\n🔧 Installing ngrok (showing all output)...")
    print("-" * 60)
    
    # Install ngrok with full output
    install_result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', 'pyngrok', '-v'],
        capture_output=False,  # Show output directly
        text=True
    )
    
    print("-" * 60)
    print(f"✅ Ngrok installation completed with exit code: {install_result.returncode}")
    
    try:
        from pyngrok import ngrok
        
        # Set auth token
        print("\n🔑 Setting ngrok auth token...")
        ngrok.set_auth_token("2tjxIXifSaGR3dMhkvhk6sZqbGo_6ZfBZLZHMbtAjfRmfoDW5")
        print("✅ Ngrok configured")
        
        # Kill old streamlit
        print("\n🔄 Cleaning up old processes...")
        kill_result = subprocess.run(['pkill', '-f', 'streamlit'], capture_output=True, text=True)
        print(f"Kill command output: {kill_result.stdout}")
        if kill_result.stderr:
            print(f"Kill command errors: {kill_result.stderr}")
        time.sleep(2)
        
        # Start streamlit with full output
        print("\n🚀 Starting Streamlit dashboard (showing all output)...")
        print("-" * 60)
        
        cmd = [
            sys.executable, '-m', 'streamlit', 'run',
            str(scripts_dir / 'widgets-en.py'),
            '--server.port', '8501',
            '--server.headless', 'true',
            '--logger.level', 'info'  # Show all logs
        ]
        
        print(f"Command: {' '.join(cmd)}")
        
        # Start process and show output in real-time
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Read output for a few seconds
        print("\nStreamlit startup output:")
        start_time = time.time()
        while time.time() - start_time < 10:  # Show output for 10 seconds
            line = process.stdout.readline()
            if line:
                print(f"  {line.rstrip()}")
            if process.poll() is not None:
                print(f"❌ Process exited with code: {process.returncode}")
                break
        
        print("-" * 60)
        
        # Check if process is still running
        if process.poll() is not None:
            print(f"❌ Streamlit failed to start! Exit code: {process.returncode}")
            # Get any remaining output
            remaining_output = process.stdout.read()
            if remaining_output:
                print("Remaining output:")
                print(remaining_output)
            sys.exit(1)
        
        # Create tunnel
        print("\n🌐 Creating public URL with ngrok...")
        public_url = ngrok.connect(8501, "http")
        
        print("\n" + "="*60)
        print(f"✅ Dashboard ready at: {public_url}")
        print("="*60)
        
        # Also display as HTML link
        from IPython.display import display, HTML
        display(HTML(f'''
        <div style="background: #10B981; padding: 20px; border-radius: 10px; text-align: center;">
            <a href="{public_url}" target="_blank" style="color: white; font-size: 18px; text-decoration: none;">
                🚀 Click here to open the Dashboard
            </a>
        </div>
        '''))
        
        print("\n📋 Instructions:")
        print("1. Click the link above to open the dashboard")
        print("2. Configure your settings")
        print("3. Click 'Save All Settings' when done")
        print("4. Then run Cell 3 to download models")
        
        # Keep showing Streamlit output
        print("\n📊 Streamlit server output (live):")
        print("-" * 60)
        while True:
            line = process.stdout.readline()
            if line:
                print(f"  {line.rstrip()}")
            else:
                time.sleep(0.1)
            if process.poll() is not None:
                print(f"\n❌ Streamlit process ended with code: {process.returncode}")
                break
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\n💡 Try using Cell 2b (fallback) instead if this doesn't work")
        
else:
    print("\n🖥️ Running Streamlit locally (showing all output)...")
    print("-" * 60)
    
    cmd = [sys.executable, str(scripts_dir / 'widgets-en.py')]
    print(f"Command: {' '.join(cmd)}")
    
    try:
        # Run with full output
        result = subprocess.run(cmd, capture_output=False, text=True)
        print(f"\nStreamlit exited with code: {result.returncode}")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\n💡 Try using Cell 2b (fallback) instead")