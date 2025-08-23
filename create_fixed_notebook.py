import nbformat as nbf
import json

# Create a new notebook
nb = nbf.v4.new_notebook()

# Cell 1: Setup Environment
cell1_code = """#@title Cell 1: Setup Environment ⚙️
from pathlib import Path
import os, sys
import subprocess

def detect_current_platform():
    if os.path.exists('/content'): return 'colab'
    elif os.path.exists('/kaggle'): return 'kaggle'
    elif os.path.exists('/workspace'): return 'workspace'
    else: return 'local'

def get_platform_root():
    platform = detect_current_platform()
    if platform == 'colab': return Path('/content')
    elif platform == 'kaggle': return Path('/kaggle/working')
    elif platform == 'workspace': return Path('/workspace')
    else: return Path.home()

platform_detected = detect_current_platform()
project_root = get_platform_root()

# For cloud platforms, clone into subdirectory
if platform_detected in ['colab', 'kaggle']:
    sd_dir = project_root / 'SD-DarkMaster-Pro'
    if not sd_dir.exists():
        print(f"🚀 Initializing SD-DarkMaster-Pro on {platform_detected} platform...")
        repo_url = "https://github.com/remphanostar/SD-DarkMaster-Pro.git"
        subprocess.run(['git', 'clone', repo_url, str(sd_dir)], check=True)
        print("✅ Repository cloned successfully!")
    project_root = sd_dir
    scripts_dir = project_root / 'scripts'
else:
    # Workspace already has the files
    print(f"✅ Running in {platform_detected} environment")
    scripts_dir = project_root / 'scripts'
    
sys.path.insert(0, str(project_root))

setup_script = scripts_dir / 'setup.py'
if setup_script.exists():
    print(f"🔧 Running setup for {platform_detected} platform...")
    exec(open(setup_script).read())
else:
    print(f"❌ Setup script not found at {setup_script}")"""

# Cell 2: Hybrid Dashboard
cell2_code = """#@title Cell 2: Hybrid Dashboard with Ngrok 🌟
import os
os.environ['NGROK_AUTH_TOKEN'] = '2tjxIXifSaGR3dMhkvhk6sZqbGo_6ZfBZLZHMbtAjfRmfoDW5'
exec(open(f'{scripts_dir}/cell2_ngrok_launcher.py').read())"""

# Cell 3: Downloads
cell3_code = """#@title Cell 3: Downloads 📦
%run $scripts_dir/downloading-en.py"""

# Cell 4: WebUI Launch
cell4_code = """#@title Cell 4: WebUI Launch 🚀
%run $scripts_dir/launch.py"""

# Cell 5: Storage Management
cell5_code = """#@title Cell 5: Storage Management 🧹
%run $scripts_dir/auto-cleaner.py"""

# Add cells to notebook
nb.cells = [
    nbf.v4.new_code_cell(cell1_code),
    nbf.v4.new_code_cell(cell2_code),
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
        "codemirror_mode": {
            "name": "ipython",
            "version": 3
        },
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.10.0"
    }
}

# Save the notebook
with open('/workspace/notebook/SD-DarkMaster-Pro-Fixed.ipynb', 'w') as f:
    nbf.write(nb, f)
    
print("✅ Created fixed notebook at /workspace/notebook/SD-DarkMaster-Pro-Fixed.ipynb")