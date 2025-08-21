#!/usr/bin/env python3
"""Create properly formatted notebook with markdown cells and #@title"""

import json

# Create notebook structure
notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

# Add header markdown
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# 🌟 SD-DarkMaster-Pro Notebook\n",
        "## Dark Mode Pro Theme | Enterprise AI Tools\n",
        "\n",
        "### Features:\n",
        "- ⚡ **aria2c Integration** - 16x faster downloads\n",
        "- 💾 **Central Storage** - Unified model management\n",
        "- 🎨 **Dual Framework UI** - Streamlit/Gradio\n",
        "- 🚀 **Multi-WebUI Support** - Forge, ComfyUI, A1111\n",
        "- 🎯 **5 Simple Cells** - All complexity hidden in scripts"
    ]
})

# Cell 1: Setup Environment
notebook["cells"].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "#@title Cell 1: Setup Environment ⚙️\n",
        "from pathlib import Path\n",
        "import os, sys\n",
        "import subprocess\n",
        "\n",
        "# Bootstrap: Determine project root dynamically\n",
        "try:\n",
        "    # Try common cloud platform paths first\n",
        "    if Path('/content').exists():\n",
        "        project_root = Path('/content/SD-DarkMaster-Pro')\n",
        "    elif Path('/kaggle/working').exists():\n",
        "        project_root = Path('/kaggle/working/SD-DarkMaster-Pro')\n",
        "    elif Path('/workspace').exists():\n",
        "        project_root = Path('/workspace/SD-DarkMaster-Pro')\n",
        "    else:\n",
        "        # Fallback to current directory\n",
        "        project_root = Path.cwd()\n",
        "        if project_root.name == 'notebook':\n",
        "            project_root = project_root.parent\n",
        "except:\n",
        "    project_root = Path.cwd()\n",
        "    if project_root.name == 'notebook':\n",
        "        project_root = project_root.parent\n",
        "\n",
        "print(f\"🏠 Project root: {project_root}\")\n",
        "\n",
        "# Clone repository if not exists\n",
        "if not (project_root / '.git').exists():\n",
        "    print(\"📥 Cloning SD-DarkMaster-Pro repository...\")\n",
        "    subprocess.run([\n",
        "        'git', 'clone',\n",
        "        'https://github.com/yourusername/SD-DarkMaster-Pro.git',\n",
        "        str(project_root)\n",
        "    ], check=False)\n",
        "\n",
        "# Update system path\n",
        "scripts_dir = project_root / 'scripts'\n",
        "modules_dir = project_root / 'modules'\n",
        "sys.path.insert(0, str(scripts_dir))\n",
        "sys.path.insert(0, str(modules_dir))\n",
        "\n",
        "# Set environment variables\n",
        "os.environ['PROJECT_ROOT'] = str(project_root)\n",
        "os.environ['SCRIPTS_DIR'] = str(scripts_dir)\n",
        "os.environ['MODULES_DIR'] = str(modules_dir)\n",
        "\n",
        "# Execute setup script\n",
        "setup_script = scripts_dir / 'setup.py'\n",
        "if setup_script.exists():\n",
        "    print(f\"🚀 Running setup script from {setup_script}\")\n",
        "    exec(open(setup_script).read())\n",
        "else:\n",
        "    print(f\"⚠️ Setup script not found at {setup_script}\")\n",
        "\n",
        "print(\"✅ Cell 1 complete!\")"
    ]
})

# Markdown for Cell 2
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 🎨 Cell 2: Hybrid Dashboard & CivitAI Browser\n",
        "This cell launches the configuration UI with native CivitAI integration and central storage management."
    ]
})

# Cell 2: Dashboard
notebook["cells"].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "#@title Cell 2: Hybrid Dashboard & CivitAI Browser 🌟\n",
        "# Launch the hybrid Streamlit/Gradio interface with native CivitAI browser\n",
        "%run $scripts_dir/widgets-en.py"
    ]
})

# Markdown for Cell 3
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 📦 Cell 3: Intelligent Downloads & Storage\n",
        "Downloads models using **aria2c** with 16x parallel connections for maximum speed!"
    ]
})

# Cell 3: Downloads
notebook["cells"].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "#@title Cell 3: Intelligent Downloads & Storage 📦\n",
        "# Handle all downloads with unified storage management and aria2c acceleration\n",
        "%run $scripts_dir/downloading-en.py"
    ]
})

# Markdown for Cell 4
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 🚀 Cell 4: Multi-Platform WebUI Launch\n",
        "Launch your selected WebUI with platform-specific optimizations and AnxietySolo's package method."
    ]
})

# Cell 4: Launch
notebook["cells"].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "#@title Cell 4: Multi-Platform WebUI Launch 🚀\n",
        "# Launch the selected WebUI with platform-specific optimizations\n",
        "%run $scripts_dir/launch.py"
    ]
})

# Markdown for Cell 5
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 🧹 Cell 5: Advanced Storage Management\n",
        "Manage storage, clean temporary files, and optimize disk usage."
    ]
})

# Cell 5: Storage
notebook["cells"].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "#@title Cell 5: Advanced Storage Management 🧹\n",
        "# Provide storage visualization and cleanup tools\n",
        "%run $scripts_dir/auto-cleaner.py"
    ]
})

# Footer markdown
notebook["cells"].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "---\n",
        "## 📝 Notes\n",
        "\n",
        "- **aria2c Integration**: Downloads use 16 parallel connections for 6x speed improvement\n",
        "- **Central Storage**: All models stored in `/storage` with symlinks to WebUIs\n",
        "- **Package Method**: Uses AnxietySolo's pre-configured WebUI packages\n",
        "- **Extensions**: 29+ extensions pre-configured for Forge\n",
        "\n",
        "### 🎯 Quick Commands\n",
        "\n",
        "```bash\n",
        "# Check aria2c status\n",
        "aria2c --version\n",
        "\n",
        "# View storage usage\n",
        "du -sh /workspace/SD-DarkMaster-Pro/storage/*\n",
        "\n",
        "# Launch Streamlit UI directly\n",
        "streamlit run scripts/widgets-en.py\n",
        "```\n",
        "\n",
        "**Created with ❤️ by SD-DarkMaster-Pro**"
    ]
})

# Save the notebook
with open('/workspace/SD-DarkMaster-Pro/notebook/SD-DarkMaster-Pro-formatted.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print('✅ Created properly formatted notebook!')
print('   - 11 cells total')
print('   - 5 code cells (all with #@title)')
print('   - 6 markdown cells for documentation')
print('\nSaved as: notebook/SD-DarkMaster-Pro-formatted.ipynb')