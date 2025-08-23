#!/usr/bin/env python3
"""
Fallback UI for Cell 2 - Uses ipywidgets for in-notebook interface
Simple model selection without Streamlit or CivitAI browser
"""

import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Get project root
try:
    project_root = Path(__file__).parent.parent
except NameError:
    # When executed from notebook
    if os.path.exists('/content'):
        project_root = Path('/content/SD-DarkMaster-Pro')
    elif os.path.exists('/kaggle'):
        project_root = Path('/kaggle/working/SD-DarkMaster-Pro')
    elif os.path.exists('/workspace'):
        project_root = Path('/workspace/SD-DarkMaster-Pro')
    else:
        project_root = Path.home() / 'SD-DarkMaster-Pro'

# Import model data
sys.path.insert(0, str(project_root))
from scripts._models_data import model_list as sd15_models, vae_list as sd15_vae_list, controlnet_list as sd15_controlnet_list, lora_list as sd15_lora_list
from scripts._xl_models_data import model_list as sdxl_models, vae_list as sdxl_vae_list, controlnet_list as sdxl_controlnet_list, lora_list as sdxl_lora_list

# Style
display(HTML("""
<style>
    .widget-label { font-weight: bold; color: #333; }
    .section-header { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-size: 18px;
        font-weight: bold;
    }
    .info-box {
        background: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-msg {
        color: green;
        font-weight: bold;
        padding: 10px;
        background: #e8f5e9;
        border-radius: 5px;
    }
</style>
"""))

# Configuration storage
config = {
    'selected_models': [],
    'selected_loras': [],
    'selected_vae': None,
    'selected_controlnet': [],
    'webui_type': 'A1111',
    'install_method': 'git',
    'base_model_lock': 'None'
}

# Create UI components
print("🎨 SD-DarkMaster-Pro Configuration (Fallback Mode)")
print("=" * 60)

# WebUI Selection
display(HTML('<div class="section-header">🚀 WebUI Selection</div>'))
webui_dropdown = widgets.Dropdown(
    options=['A1111', 'Forge', 'ComfyUI', 'SD.Next', 'Fooocus', 'InvokeAI', 'Vladmandic'],
    value='A1111',
    description='WebUI Type:',
    style={'description_width': 'initial'}
)
display(webui_dropdown)

# Installation Method
install_radio = widgets.RadioButtons(
    options=['Git Clone (Standard)', 'Package Method (Fast)'],
    value='Git Clone (Standard)',
    description='Install Method:',
    style={'description_width': 'initial'}
)
display(install_radio)

# Model Selection
display(HTML('<div class="section-header">📦 Model Selection</div>'))

# SD1.5 Models
display(HTML('<h4>SD 1.5 Models</h4>'))
sd15_checkboxes = []
for name, info in list(sd15_models.items())[:10]:  # Show first 10
    cb = widgets.Checkbox(value=False, description=name[:50], indent=False)
    sd15_checkboxes.append((f"sd15_{name}", cb))
    display(cb)

# SDXL Models
display(HTML('<h4>SDXL Models</h4>'))
sdxl_checkboxes = []
for name, info in list(sdxl_models.items())[:10]:  # Show first 10
    cb = widgets.Checkbox(value=False, description=name[:50], indent=False)
    sdxl_checkboxes.append((f"sdxl_{name}", cb))
    display(cb)

# LoRA Selection
display(HTML('<div class="section-header">🎨 LoRA Selection</div>'))
lora_checkboxes = []

display(HTML('<h4>SD 1.5 LoRAs</h4>'))
for name, info in list(sd15_lora_list.items())[:5]:  # Show first 5
    cb = widgets.Checkbox(value=False, description=name[:50], indent=False)
    lora_checkboxes.append((f"sd15_lora_{name}", cb))
    display(cb)

display(HTML('<h4>SDXL LoRAs</h4>'))
for name, info in list(sdxl_lora_list.items())[:5]:  # Show first 5
    cb = widgets.Checkbox(value=False, description=name[:50], indent=False)
    lora_checkboxes.append((f"sdxl_lora_{name}", cb))
    display(cb)

# VAE Selection
display(HTML('<div class="section-header">🎭 VAE Selection</div>'))
vae_radio = widgets.RadioButtons(
    options=['None (Use Model VAE)'] + list(sd15_vae_list.keys()) + list(sdxl_vae_list.keys()),
    value='None (Use Model VAE)',
    description='Select VAE:',
    style={'description_width': 'initial'}
)
display(vae_radio)

# ControlNet Selection
display(HTML('<div class="section-header">🎮 ControlNet Selection</div>'))
controlnet_checkboxes = []

display(HTML('<h4>SD 1.5 ControlNets</h4>'))
for name, info in list(sd15_controlnet_list.items())[:5]:  # Show first 5
    cb = widgets.Checkbox(value=False, description=name[:50], indent=False)
    controlnet_checkboxes.append((f"sd15_cn_{name}", cb))
    display(cb)

# Base Model Lock
display(HTML('<div class="section-header">🔒 Base Model Lock</div>'))
lock_dropdown = widgets.Dropdown(
    options=['None (Load All)', 'SD 1.5 Only', 'SDXL Only', 'Pony Only'],
    value='None (Load All)',
    description='Model Filter:',
    style={'description_width': 'initial'}
)
display(lock_dropdown)

# Output area for messages
output = widgets.Output()
display(output)

# Save button
save_button = widgets.Button(
    description='💾 Save Configuration',
    button_style='success',
    tooltip='Save all settings to session.json',
    layout=widgets.Layout(width='300px', height='50px')
)

def save_config(b):
    """Save configuration when button is clicked"""
    with output:
        clear_output()
        
        # Collect selected models
        config['selected_models'] = [id for id, cb in sd15_checkboxes + sdxl_checkboxes if cb.value]
        config['selected_loras'] = [id for id, cb in lora_checkboxes if cb.value]
        config['selected_vae'] = None if vae_radio.value == 'None (Use Model VAE)' else vae_radio.value
        config['selected_controlnet'] = [id for id, cb in controlnet_checkboxes if cb.value]
        config['webui_type'] = webui_dropdown.value
        config['install_method'] = 'package' if 'Package' in install_radio.value else 'git'
        config['base_model_lock'] = lock_dropdown.value
        
        # Add metadata
        config['timestamp'] = datetime.now().isoformat()
        config['platform'] = 'colab' if os.path.exists('/content') else 'unknown'
        
        # Save to file
        config_dir = project_root / 'configs'
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / 'session.json'
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            display(HTML(f'''
            <div class="success-msg">
                ✅ Configuration saved successfully!<br>
                📦 Models: {len(config['selected_models'])}<br>
                🎨 LoRAs: {len(config['selected_loras'])}<br>
                🎭 VAE: {'Selected' if config['selected_vae'] else 'None'}<br>
                🎮 ControlNets: {len(config['selected_controlnet'])}<br>
                🚀 WebUI: {config['webui_type']}<br>
                ⚡ Method: {config['install_method']}<br>
            </div>
            '''))
            
            print("\n📋 Configuration saved to:", config_file)
            print("\n✅ You can now run Cell 3 to download models!")
            
        except Exception as e:
            print(f"❌ Error saving configuration: {str(e)}")

save_button.on_click(save_config)
display(save_button)

# Info box
display(HTML('''
<div class="info-box">
    <h4>ℹ️ Instructions:</h4>
    <ol>
        <li>Select your preferred WebUI and installation method</li>
        <li>Choose models, LoRAs, VAE, and ControlNets</li>
        <li>Click "Save Configuration" to save your selections</li>
        <li>Run Cell 3 to download selected models</li>
        <li>Run Cell 4 to launch the WebUI</li>
    </ol>
    <p><strong>Note:</strong> This is a simplified fallback UI. For full features including CivitAI browser, use Cell 2 instead.</p>
</div>
'''))