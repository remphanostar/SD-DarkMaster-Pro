#@title Cell 2: Hybrid Dashboard & CivitAI Browser 🌟
import os
import sys
import subprocess
import time
from pathlib import Path

# Detect platform
platform = 'colab' if 'google.colab' in sys.modules else 'local'
project_root = Path('/content/SD-DarkMaster-Pro') if platform == 'colab' else Path('/workspace/SD-DarkMaster-Pro')
scripts_dir = project_root / 'scripts'

if platform == 'colab':
    print("🌐 Setting up Streamlit with ngrok tunnel for Colab...")
    
    # Install ngrok if not already installed
    try:
        import pyngrok
    except ImportError:
        print("📦 Installing pyngrok...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyngrok', '-q'], check=True)
        import pyngrok
    
    from pyngrok import ngrok
    
    # Kill any existing Streamlit processes
    subprocess.run(['pkill', '-f', 'streamlit'], capture_output=True)
    time.sleep(2)
    
    # Start Streamlit server in background
    print("🚀 Starting Streamlit server...")
    streamlit_cmd = [
        'streamlit', 'run',
        str(scripts_dir / 'widgets-en.py'),
        '--server.port', '8501',
        '--server.headless', 'true',
        '--server.address', '0.0.0.0',
        '--theme.base', 'dark',
        '--theme.primaryColor', '#10B981',
        '--theme.backgroundColor', '#0a0a0a',
        '--theme.secondaryBackgroundColor', '#1a1a2e'
    ]
    
    # Start the process
    process = subprocess.Popen(
        streamlit_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for Streamlit to start
    print("⏳ Waiting for Streamlit to initialize...")
    time.sleep(8)
    
    # Set up ngrok tunnel
    try:
        # Authenticate ngrok if token is available (optional)
        # ngrok.set_auth_token("YOUR_AUTH_TOKEN")  # Optional: Add your ngrok auth token
        
        # Create tunnel
        public_url = ngrok.connect(8501, "http")
        
        print("\n" + "="*60)
        print("✅ SD-DarkMaster-Pro Dashboard is ready!")
        print("="*60)
        print(f"🌐 Public URL: {public_url}")
        print("="*60)
        print("📱 Click the link above to open the dashboard")
        print("🎨 The UI will open in a new tab with Dark Mode Pro theme")
        print("="*60)
        
        # Also try to display as clickable link in Colab
        from IPython.display import display, HTML
        display(HTML(f'''
        <div style="background: linear-gradient(135deg, #10B981 0%, #059669 100%); 
                    padding: 20px; border-radius: 10px; margin: 10px 0;">
            <h2 style="color: white; margin: 0 0 10px 0;">🎨 SD-DarkMaster-Pro Dashboard</h2>
            <a href="{public_url}" target="_blank" 
               style="background: white; color: #059669; padding: 10px 20px; 
                      border-radius: 5px; text-decoration: none; font-weight: bold;
                      display: inline-block;">
                Open Dashboard →
            </a>
        </div>
        '''))
        
    except Exception as e:
        print(f"❌ Error setting up ngrok tunnel: {e}")
        print("💡 Tip: Make sure you have internet connectivity")
        print("💡 Alternative: Install ngrok manually: !pip install pyngrok")
        
else:
    # For non-Colab environments, try Gradio fallback
    print("🎨 Launching Gradio interface (Streamlit requires ngrok in notebooks)...")
    try:
        exec(open(scripts_dir / 'widgets-en.py').read())
    except Exception as e:
        print(f"⚠️ Could not launch UI: {e}")
        print("💡 For notebooks, Streamlit requires ngrok tunneling")
        print("💡 For local environments, run: streamlit run scripts/widgets-en.py")