#!/usr/bin/env python3
"""
Proof of Concept: Cell 1 that launches complete Streamlit UI
This would replace the traditional 5-cell approach
"""

from pathlib import Path
import os, sys
import subprocess
import threading
import time
import webbrowser

def detect_current_platform():
    """Detect the current cloud GPU platform"""
    if os.path.exists('/content'):
        return 'colab'
    elif os.path.exists('/kaggle'):
        return 'kaggle'
    elif os.path.exists('/workspace'):
        return 'workspace'
    else:
        return 'local'

def get_platform_root():
    """Get the appropriate root directory for the platform"""
    platform = detect_current_platform()
    platform_roots = {
        'colab': Path('/content'),
        'kaggle': Path('/kaggle/working'),
        'workspace': Path('/workspace'),
        'local': Path.home()
    }
    return platform_roots.get(platform, Path.home())

def setup_and_launch():
    """Complete setup and launch Streamlit UI"""
    
    # Platform detection
    platform = detect_current_platform()
    project_root = get_platform_root() / 'SD-DarkMaster-Pro'
    
    print("="*60)
    print("🎨 SD-DarkMaster-Pro - One Cell Setup")
    print("="*60)
    print(f"📍 Platform: {platform}")
    print(f"📁 Project: {project_root}")
    
    # Add to path
    sys.path.insert(0, str(project_root))
    
    # Run setup.py
    setup_script = project_root / 'scripts' / 'setup.py'
    if setup_script.exists():
        print("🔧 Running setup...")
        exec(open(setup_script).read())
        print("✅ Setup complete!")
    
    # Prepare Streamlit launch command
    streamlit_script = project_root / 'streamlit_master_ui.py'
    
    # Check if we need ngrok (for cloud platforms)
    needs_tunnel = platform in ['colab', 'kaggle', 'paperspace']
    
    if needs_tunnel:
        print("\n🌐 Cloud platform detected - setting up public access...")
        
        # Install pyngrok if needed
        try:
            import pyngrok
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyngrok", "-q"])
            import pyngrok
        
        from pyngrok import ngrok
        
        # Set ngrok token if available
        ngrok_token = os.environ.get('NGROK_AUTH_TOKEN')
        if ngrok_token:
            ngrok.set_auth_token(ngrok_token)
    
    # Launch Streamlit in background
    def run_streamlit():
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            str(streamlit_script),
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--theme.base", "dark"
        ]
        subprocess.run(cmd)
    
    # Start Streamlit thread
    print("\n🚀 Launching Streamlit UI...")
    ui_thread = threading.Thread(target=run_streamlit, daemon=True)
    ui_thread.start()
    
    # Wait for Streamlit to start
    time.sleep(5)
    
    # Get access URL
    if needs_tunnel:
        # Create ngrok tunnel
        from pyngrok import ngrok
        public_url = ngrok.connect(8501, "http")
        access_url = str(public_url)
        print(f"\n✅ Public URL: {access_url}")
    else:
        access_url = "http://localhost:8501"
        print(f"\n✅ Local URL: {access_url}")
    
    # Display access information
    print("\n" + "="*60)
    print("🎉 SD-DarkMaster-Pro Interface Ready!")
    print("="*60)
    print(f"\n📱 Access URL: {access_url}")
    print("\nThe interface includes:")
    print("  • Complete notebook control (all cells)")
    print("  • Model selection & downloads")
    print("  • Native CivitAI browser")
    print("  • WebUI launcher")
    print("  • Storage management")
    print("\n✨ No need to run other cells - everything is in the UI!")
    print("="*60)
    
    # For notebook environments, display HTML
    try:
        from IPython.display import display, HTML
        
        html_content = f'''
        <div style="background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #0f4c3a 50%, #1a1a2e 75%, #10B981 100%);
                    padding: 2rem; border-radius: 16px; color: white; font-family: 'Segoe UI', sans-serif;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.5); animation: glow 3s ease-in-out infinite;">
            <style>
                @keyframes glow {{
                    0%, 100% {{ box-shadow: 0 10px 40px rgba(16, 185, 129, 0.3); }}
                    50% {{ box-shadow: 0 10px 60px rgba(16, 185, 129, 0.6); }}
                }}
            </style>
            
            <h1 style="background: linear-gradient(135deg, #10B981 0%, #059669 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       font-size: 2.5rem; margin-bottom: 1rem;">
                🎨 SD-DarkMaster-Pro Ready!
            </h1>
            
            <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                <h2 style="color: #10B981; margin-bottom: 0.5rem;">Access Your Interface:</h2>
                <a href="{access_url}" target="_blank" 
                   style="color: #10B981; font-size: 1.5rem; text-decoration: none;
                          display: inline-block; padding: 0.5rem 1rem;
                          background: rgba(16, 185, 129, 0.2); border-radius: 8px;
                          border: 2px solid #10B981; transition: all 0.3s;">
                    🌐 {access_url}
                </a>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1.5rem;">
                <div style="background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 8px;">
                    <h3 style="color: #10B981;">✅ Included Features:</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li>📦 Model Management</li>
                        <li>🎨 LoRA Selection</li>
                        <li>🔍 CivitAI Browser</li>
                        <li>🚀 WebUI Launcher</li>
                    </ul>
                </div>
                <div style="background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 8px;">
                    <h3 style="color: #10B981;">🎮 Control Panel:</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li>📊 System Monitor</li>
                        <li>💾 Storage Manager</li>
                        <li>⚙️ Settings Config</li>
                        <li>📥 Download Queue</li>
                    </ul>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 2rem; padding: 1rem;
                        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
                        border-radius: 8px;">
                <p style="font-size: 1.2rem; font-weight: bold; margin: 0;">
                    🚀 No need to run other cells - everything is in the UI!
                </p>
            </div>
        </div>
        '''
        
        display(HTML(html_content))
        
    except ImportError:
        # Not in a notebook environment
        pass
    
    return access_url

# This would be the ONLY code in Cell 1:
if __name__ == "__main__":
    url = setup_and_launch()
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n✅ Shutting down SD-DarkMaster-Pro...")