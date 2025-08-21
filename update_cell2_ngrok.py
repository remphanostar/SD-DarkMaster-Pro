#!/usr/bin/env python3
import json

# Read notebook
with open('/workspace/notebook/SD-DarkMaster-Pro.ipynb', 'r') as f:
    nb = json.load(f)

# Update Cell 2 (index 1) with small ngrok implementation
new_cell2_code = """#@title Cell 2: Hybrid Dashboard with Ngrok 🌟
import os
os.environ['NGROK_AUTH_TOKEN'] = '2tjxIXifSaGR3dMhkvhk6sZqbGo_6ZfBZLZHMbtAjfRmfoDW5'
exec(open(f'{scripts_dir}/cell2_ngrok_launcher.py').read())"""

nb['cells'][1] = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": new_cell2_code
}

# Save updated notebook
with open('/workspace/notebook/SD-DarkMaster-Pro.ipynb', 'w') as f:
    json.dump(nb, f, indent=2)

print("✅ Updated Cell 2 with ngrok tunneling (kept small - 4 lines!)")