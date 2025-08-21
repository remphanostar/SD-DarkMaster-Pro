#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Config UI - Gradio Version
Simple, reliable interface for configuration
"""

import os
import sys
import json
from pathlib import Path
import gradio as gr

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import model data
try:
    from scripts._models_data import model_list as sd15_models
    from scripts._xl_models_data import model_list as sdxl_models
except:
    sd15_models = {}
    sdxl_models = {}

# Load extensions
extensions_file = project_root / 'scripts' / '_extensions.txt'
extensions = []
if extensions_file.exists():
    with open(extensions_file, 'r') as f:
        extensions = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Storage for selections
selections = {
    'models': [],
    'loras': [],
    'extensions': [],
    'settings': {}
}

def update_model_list(model_type):
    """Update model list based on type selection"""
    if model_type == "SD 1.5":
        return gr.update(choices=list(sd15_models.keys()) if sd15_models else ["No models found"])
    else:
        return gr.update(choices=list(sdxl_models.keys()) if sdxl_models else ["No models found"])

def save_selections(models, loras, exts):
    """Save current selections"""
    selections['models'] = models or []
    selections['loras'] = loras or []
    selections['extensions'] = exts or []
    
    # Save to file
    config_file = project_root / 'configs' / 'ui_selections.json'
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_file, 'w') as f:
        json.dump(selections, f, indent=2)
    
    return f"✅ Saved: {len(selections['models'])} models, {len(selections['loras'])} LoRAs, {len(selections['extensions'])} extensions"

def get_storage_info():
    """Get storage information"""
    storage_path = project_root / 'storage'
    
    if not storage_path.exists():
        return "Storage not initialized"
    
    total_size = 0
    file_count = 0
    
    for path in storage_path.rglob('*'):
        if path.is_file():
            file_count += 1
            total_size += path.stat().st_size
    
    size_gb = total_size / (1024**3)
    
    return f"""📊 Storage Status:
• Total Size: {size_gb:.2f} GB
• Total Files: {file_count}
• Storage Path: {storage_path}

📁 Directories:
• Models: {storage_path / 'models' / 'Stable-diffusion'}
• LoRA: {storage_path / 'models' / 'Lora'}
• VAE: {storage_path / 'models' / 'VAE'}
• Outputs: {storage_path / 'outputs'}
"""

def launch_webui(webui_type, port, share, api):
    """Launch WebUI configuration"""
    config = {
        'webui_type': webui_type,
        'port': port,
        'share': share,
        'api': api
    }
    
    selections['settings'] = config
    
    return f"""🚀 WebUI Configuration Ready:
• Type: {webui_type}
• Port: {port}
• Share: {'Enabled' if share else 'Disabled'}
• API: {'Enabled' if api else 'Disabled'}

To launch, run: python scripts/launch.py
"""

# Create Gradio interface
with gr.Blocks(title="SD-DarkMaster-Pro Config UI", theme=gr.themes.Soft(
    primary_hue="emerald",
    neutral_hue="slate",
    font=["Inter", "sans-serif"]
)) as interface:
    
    # Custom CSS for Dark Mode Pro
    gr.HTML("""
    <style>
        .gradio-container {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%) !important;
        }
        
        h1, h2, h3 {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        
        .gr-button-primary {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
            border: none !important;
        }
        
        .gr-button-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
        }
        
        .gr-box {
            background: rgba(26, 26, 46, 0.5) !important;
            border: 1px solid rgba(16, 185, 129, 0.2) !important;
        }
        
        .gr-input {
            background: rgba(26, 26, 46, 0.7) !important;
            border: 1px solid rgba(16, 185, 129, 0.3) !important;
            color: #E5E7EB !important;
        }
        
        .gr-check-radio {
            background: rgba(26, 26, 46, 0.5) !important;
        }
    </style>
    """)
    
    gr.Markdown("# 🎨 SD-DarkMaster-Pro Config UI")
    gr.Markdown("### Unified Control Center for AI Art Generation")
    
    with gr.Tabs():
        with gr.TabItem("🏠 Dashboard"):
            gr.Markdown("## System Status")
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("""
                    ### Platform Information
                    • **Platform**: Workspace/RunPod
                    • **Project**: SD-DarkMaster-Pro
                    • **Status**: ✅ Ready
                    """)
                
                with gr.Column(scale=1):
                    storage_info = gr.Textbox(
                        label="Storage Information",
                        value=get_storage_info(),
                        lines=10,
                        interactive=False
                    )
                    
                    refresh_btn = gr.Button("🔄 Refresh Storage Info")
                    refresh_btn.click(get_storage_info, outputs=storage_info)
        
        with gr.TabItem("📦 Models"):
            gr.Markdown("## Model Selection")
            
            model_type = gr.Radio(
                ["SD 1.5", "SDXL"],
                label="Model Type",
                value="SD 1.5"
            )
            
            model_choices = list(sd15_models.keys()) if sd15_models else ["No models found"]
            
            selected_models = gr.CheckboxGroup(
                choices=model_choices,
                label="Available Models",
                value=[]
            )
            
            model_type.change(update_model_list, inputs=model_type, outputs=selected_models)
        
        with gr.TabItem("🎨 LoRA"):
            gr.Markdown("## LoRA Selection")
            
            # Example LoRAs (in real implementation, these would be loaded from a source)
            example_loras = [
                "Character LoRA 1",
                "Style LoRA 1", 
                "Concept LoRA 1",
                "Pose LoRA 1",
                "Clothing LoRA 1",
                "Background LoRA 1"
            ]
            
            selected_loras = gr.CheckboxGroup(
                choices=example_loras,
                label="Available LoRAs",
                value=[]
            )
        
        with gr.TabItem("🔧 Extensions"):
            gr.Markdown("## Extension Management")
            
            ext_choices = [ext.split('/')[-1].replace('.git', '') for ext in extensions]
            
            selected_extensions = gr.CheckboxGroup(
                choices=ext_choices if ext_choices else ["No extensions found"],
                label="Available Extensions",
                value=[]
            )
            
            gr.Markdown(f"*Found {len(extensions)} extensions in _extensions.txt*")
        
        with gr.TabItem("⚙️ Settings"):
            gr.Markdown("## WebUI Settings")
            
            with gr.Row():
                webui_type = gr.Dropdown(
                    ["Automatic1111", "ComfyUI", "Forge", "Vladmandic"],
                    label="WebUI Type",
                    value="Automatic1111"
                )
                
                port = gr.Number(
                    value=7860,
                    label="Port",
                    precision=0
                )
            
            with gr.Row():
                share = gr.Checkbox(
                    label="Enable Gradio Share",
                    value=False
                )
                
                api = gr.Checkbox(
                    label="Enable API",
                    value=True
                )
            
            launch_output = gr.Textbox(
                label="Launch Configuration",
                lines=8,
                interactive=False
            )
            
            launch_config_btn = gr.Button("🚀 Generate Launch Config", variant="primary")
            launch_config_btn.click(
                launch_webui,
                inputs=[webui_type, port, share, api],
                outputs=launch_output
            )
    
    # Save button at the bottom
    gr.Markdown("---")
    
    with gr.Row():
        save_output = gr.Textbox(
            label="Save Status",
            interactive=False
        )
        
        save_btn = gr.Button("💾 Save All Selections", variant="primary", scale=2)
    
    # Connect save button to all selections
    def save_all():
        return save_selections(
            selected_models.value if 'selected_models' in locals() else [],
            selected_loras.value if 'selected_loras' in locals() else [],
            selected_extensions.value if 'selected_extensions' in locals() else []
        )
    
    save_btn.click(
        lambda m, l, e: save_selections(m, l, e),
        inputs=[selected_models, selected_loras, selected_extensions],
        outputs=save_output
    )
    
    gr.Markdown("### 🎨 SD-DarkMaster-Pro | Unified AI Art Generation Platform")

# Launch the interface
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎨 SD-DarkMaster-Pro Config UI")
    print("="*60)
    print("\n🚀 Launching Gradio interface...")
    print("📍 Access at: http://localhost:7860")
    print("Press Ctrl+C to stop\n")
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=False,
        quiet=False
    )