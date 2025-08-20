#!/usr/bin/env python3
"""Create the SD-DarkMaster-Pro notebook with exactly 5 cells"""

import nbformat as nbf
from pathlib import Path

# Create a new notebook
nb = nbf.v4.new_notebook()

# Cell 1: Setup Environment
cell1_code = '''#@title Cell 1: Setup Environment ⚙️
from pathlib import Path
import os, sys
import subprocess

# Detect current platform
def detect_current_platform():
    """Detect the current cloud GPU platform"""
    if os.path.exists('/content'):
        return 'colab'
    elif os.path.exists('/kaggle'):
        return 'kaggle'
    elif os.path.exists('/workspace'):
        return 'workspace'
    elif 'LIGHTNING_CLOUD_PROJECT_ID' in os.environ:
        return 'lightning'
    elif 'PAPERSPACE_GRADIENT_ID' in os.environ:
        return 'paperspace'
    elif 'RUNPOD_POD_ID' in os.environ:
        return 'runpod'
    elif 'VAST_CONTAINERLABEL' in os.environ:
        return 'vast'
    elif 'SAGEMAKER_INTERNAL_IMAGE_URI' in os.environ:
        return 'sagemaker'
    else:
        return 'local'

def get_platform_root():
    """Get the appropriate root directory for the platform"""
    platform = detect_current_platform()
    if platform == 'colab':
        return Path('/content')
    elif platform == 'kaggle':
        return Path('/kaggle/working')
    elif platform == 'workspace':
        return Path('/workspace')
    elif platform == 'lightning':
        return Path.home() / 'work'
    elif platform == 'paperspace':
        return Path('/notebooks')
    elif platform == 'runpod':
        return Path('/workspace')
    elif platform == 'vast':
        return Path('/workspace')
    elif platform == 'sagemaker':
        return Path('/opt/ml/code')
    else:
        return Path.home()

# Hybrid dual-framework bootstrap with Dark Mode Pro theming
platform_detected = detect_current_platform()
project_root = get_platform_root() / 'SD-DarkMaster-Pro'
scripts_dir = project_root / 'scripts'

# Self-cloning bootstrap sequence
if not project_root.exists():
    print(f"🚀 Initializing SD-DarkMaster-Pro on {platform_detected} platform...")
    print(f"📁 Project root: {project_root}")
    
    # Clone the repository
    repo_url = "https://github.com/anxietysolo/SD-DarkMaster-Pro.git"
    subprocess.run(['git', 'clone', repo_url, str(project_root)], check=True)
    print("✅ Repository cloned successfully!")
else:
    print(f"✅ SD-DarkMaster-Pro already exists at {project_root}")
    
# Add project to path
sys.path.insert(0, str(project_root))

# Run setup script with platform-specific optimizations
setup_script = scripts_dir / 'setup.py'
if setup_script.exists():
    print(f"🔧 Running setup for {platform_detected} platform with Dark Mode Pro theme...")
    exec(open(setup_script).read())
else:
    print("⚠️ Setup script not found. Please ensure the repository is properly cloned.")'''

# Cell 2: Hybrid Dashboard & CivitAI Browser
cell2_code = '''#@title Cell 2: Hybrid Dashboard & CivitAI Browser 🌟
# This cell launches the hybrid Streamlit/Gradio interface with native CivitAI browser
%run $scripts_dir/widgets-en.py'''

# Cell 3: Intelligent Downloads & Storage
cell3_code = '''#@title Cell 3: Intelligent Downloads & Storage 📦
# This cell handles all downloads with unified storage management
%run $scripts_dir/downloading-en.py'''

# Cell 4: Multi-Platform WebUI Launch
cell4_code = '''#@title Cell 4: Multi-Platform WebUI Launch 🚀
# This cell launches the selected WebUI with platform-specific optimizations
%run $scripts_dir/launch.py'''

# Cell 5: Advanced Storage Management
cell5_code = '''#@title Cell 5: Advanced Storage Management 🧹
# This cell provides storage visualization and cleanup tools
%run $scripts_dir/auto-cleaner.py'''

# Add cells to notebook
nb.cells = [
    nbf.v4.new_code_cell(cell1_code),
    nbf.v4.new_code_cell(cell2_code),
    nbf.v4.new_code_cell(cell3_code),
    nbf.v4.new_code_cell(cell4_code),
    nbf.v4.new_code_cell(cell5_code)
]

# Save the notebook
notebook_path = Path('/workspace/SD-DarkMaster-Pro/notebook/SD-DarkMaster-Pro.ipynb')
notebook_path.parent.mkdir(parents=True, exist_ok=True)

with open(notebook_path, 'w') as f:
    nbf.write(nb, f)

print(f"✅ Notebook created successfully at {notebook_path}")
print(f"📝 Total cells: {len(nb.cells)} (all code cells with #@title)")