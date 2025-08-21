import nbformat as nbf

# Read the current notebook
with open('notebook/SD-DarkMaster-Pro.ipynb', 'r') as f:
    nb = nbf.read(f, 4)

# Update Cell 2 with ngrok tunneling
cell2_code = '''#@title Cell 2: Hybrid Dashboard & CivitAI Browser 🌟
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
    
    # Install ngrok
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyngrok', '-q'], check=True)
    from pyngrok import ngrok
    
    # Kill any existing Streamlit
    subprocess.run(['pkill', '-f', 'streamlit'], capture_output=True)
    time.sleep(2)
    
    # Start Streamlit server
    print("🚀 Starting Streamlit server...")
    streamlit_cmd = [
        'streamlit', 'run',
        str(scripts_dir / 'widgets-en.py'),
        '--server.port', '8501',
        '--server.headless', 'true'
    ]
    
    process = subprocess.Popen(streamlit_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for startup
    print("⏳ Waiting for Streamlit to initialize...")
    time.sleep(8)
    
    # Create tunnel
    try:
        public_url = ngrok.connect(8501, "http")
        print("\\n" + "="*60)
        print("✅ SD-DarkMaster-Pro Dashboard is ready!")
        print(f"🌐 Public URL: {public_url}")
        print("📱 Click the link to open the dashboard")
        print("="*60)
        
        # Display clickable link
        from IPython.display import display, HTML
        display(HTML(f'<a href="{public_url}" target="_blank" style="background: #10B981; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; font-weight: bold;">Open Dashboard →</a>'))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Try: !pip install pyngrok")
        
else:
    # Non-Colab: run the script directly
    %run $scripts_dir/widgets-en.py'''

# Update Cell 2
if len(nb.cells) > 1:
    nb.cells[1] = nbf.v4.new_code_cell(cell2_code)

# Save updated notebook
with open('notebook/SD-DarkMaster-Pro-with-ngrok.ipynb', 'w') as f:
    nbf.write(nb, f)

print("✅ Created SD-DarkMaster-Pro-with-ngrok.ipynb with proper ngrok tunneling!")
