import nbformat as nbf

# Create a new notebook
nb = nbf.v4.new_notebook()

# Cell 1: Setup
cell1_code = """#@title Cell 1: Setup Environment ⚙️
from pathlib import Path
import os, sys
import subprocess

def detect_current_platform():
    if 'google.colab' in sys.modules: 
        return 'colab'
    elif os.path.exists('/kaggle'): 
        return 'kaggle'
    elif os.path.exists('/workspace'): 
        return 'workspace'
    else: 
        return 'local'

def get_platform_root():
    platform = detect_current_platform()
    if platform == 'colab': 
        return Path('/content')
    elif platform == 'kaggle': 
        return Path('/kaggle/working')
    elif platform == 'workspace': 
        return Path('/workspace')
    else: 
        return Path.home()

platform_detected = detect_current_platform()
platform_root = get_platform_root()

# Always use subdirectory for consistent structure
project_name = 'SD-DarkMaster-Pro'
project_root = platform_root / project_name

if not project_root.exists():
    print(f"🚀 Cloning SD-DarkMaster-Pro on {platform_detected} platform...")
    repo_url = "https://github.com/remphanostar/SD-DarkMaster-Pro.git"
    subprocess.run(['git', 'clone', repo_url, str(project_root)], check=True)
    print("✅ Repository cloned successfully!")
else:
    print(f"✅ SD-DarkMaster-Pro already exists at {project_root}")
    # For existing installations, pull latest changes
    try:
        subprocess.run(['git', '-C', str(project_root), 'pull'], check=True)
        print("✅ Updated to latest version")
    except:
        print("⚠️ Could not update (may have local changes)")

scripts_dir = project_root / 'scripts'
sys.path.insert(0, str(project_root))

# Run setup
setup_script = scripts_dir / 'setup.py'
if setup_script.exists():
    print(f"🔧 Running setup for {platform_detected} platform...")
    exec(open(setup_script).read())
else:
    print(f"❌ Setup script not found at {setup_script}")
    print(f"Current directory contents: {list(project_root.iterdir())}")"""

# Cell 2: Streamlit UI with ngrok
cell2_code = """#@title Cell 2: Hybrid Dashboard with Ngrok 🌟
import os
os.environ['NGROK_AUTH_TOKEN'] = '2tjxIXifSaGR3dMhkvhk6sZqbGo_6ZfBZLZHMbtAjfRmfoDW5'
exec(open(f'{scripts_dir}/cell2_ngrok_launcher.py').read())"""

# Cell 2b: Fallback UI
cell2b_code = """#@title Cell 2b: Simple Configuration UI (Fallback) 🎯
# Use this cell if Cell 2 doesn't work or if you prefer a simpler in-notebook interface
exec(open(f'{scripts_dir}/cell2_fallback.py').read())"""

# Cell 3: Downloads
cell3_code = """#@title Cell 3: Downloads 📦
exec(open(f'{scripts_dir}/downloading-en.py').read())"""

# Cell 4: WebUI Launch
cell4_code = """#@title Cell 4: WebUI Launch 🚀
exec(open(f'{scripts_dir}/launch.py').read())"""

# Cell 5: Storage Management
cell5_code = """#@title Cell 5: Storage Management 🧹
exec(open(f'{scripts_dir}/auto-cleaner.py').read())"""

# Add cells to notebook
nb.cells = [
    nbf.v4.new_code_cell(cell1_code),
    nbf.v4.new_code_cell(cell2_code),
    nbf.v4.new_code_cell(cell2b_code),
    nbf.v4.new_code_cell(cell3_code),
    nbf.v4.new_code_cell(cell4_code),
    nbf.v4.new_code_cell(cell5_code)
]

# Add metadata
nb.metadata = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "name": "python",
        "version": "3.9.0"
    }
}

# Save the notebook
with open('/workspace/notebook/SD-DarkMaster-Pro.ipynb', 'w') as f:
    nbf.write(nb, f)

print("✅ Fixed notebook created successfully!")