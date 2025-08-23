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
        
scripts_dir = project_root / 'scripts'

platform = 'colab' if 'google.colab' in sys.modules else 'local'
if platform == 'colab':
    # Install and setup ngrok
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyngrok', '-q'])
    from pyngrok import ngrok
    
    # Set auth token
    ngrok.set_auth_token("2tjxIXifSaGR3dMhkvhk6sZqbGo_6ZfBZLZHMbtAjfRmfoDW5")
    
    # Kill old streamlit
    subprocess.run(['pkill', '-f', 'streamlit'], capture_output=True)
    time.sleep(2)
    
    # Start streamlit
    cmd = f"streamlit run {scripts_dir}/widgets-en.py --server.port 8501 --server.headless true"
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Wait and create tunnel
    time.sleep(8)
    public_url = ngrok.connect(8501, "http")
    
    print("="*60)
    print(f"✅ Dashboard ready at: {public_url}")
    print("="*60)
    
    # Display clickable link
    from IPython.display import display, HTML
    display(HTML(f'<a href="{public_url}" target="_blank" style="background:#10B981;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;font-weight:bold">Open Dashboard →</a>'))
else:
    # Non-colab: run directly
    exec(open(f'{scripts_dir}/widgets-en.py').read())