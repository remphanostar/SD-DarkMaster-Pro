import nbformat as nbf

nb = nbf.v4.new_notebook()

cell1 = '''#@title Cell 1: Setup Environment ⚙️
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
project_root = get_platform_root() / 'SD-DarkMaster-Pro'
scripts_dir = project_root / 'scripts'

if not project_root.exists():
    print(f"🚀 Initializing SD-DarkMaster-Pro on {platform_detected} platform...")
    repo_url = "https://github.com/remphanostar/SD-DarkMaster-Pro.git"
    subprocess.run(['git', 'clone', repo_url, str(project_root)], check=True)
    print("✅ Repository cloned successfully!")
else:
    print(f"✅ SD-DarkMaster-Pro already exists at {project_root}")
    
sys.path.insert(0, str(project_root))

setup_script = scripts_dir / 'setup.py'
if setup_script.exists():
    print(f"🔧 Running setup for {platform_detected} platform...")
    exec(open(setup_script).read())'''

nb.cells = [
    nbf.v4.new_code_cell(cell1),
    nbf.v4.new_code_cell('#@title Cell 2: Hybrid Dashboard 🌟\n%run $scripts_dir/widgets-en.py'),
    nbf.v4.new_code_cell('#@title Cell 3: Downloads 📦\n%run $scripts_dir/downloading-en.py'),
    nbf.v4.new_code_cell('#@title Cell 4: WebUI Launch 🚀\n%run $scripts_dir/launch.py'),
    nbf.v4.new_code_cell('#@title Cell 5: Storage Management 🧹\n%run $scripts_dir/auto-cleaner.py')
]

with open('notebook/SD-DarkMaster-Pro.ipynb', 'w') as f:
    nbf.write(nb, f)
print("✅ Created notebook with correct GitHub URL!")
