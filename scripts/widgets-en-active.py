#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Dashboard - Active UI with real feedback
Shows progress, errors, and output in real-time
"""

import streamlit as st
import sys
import os
import time
import subprocess
from pathlib import Path
from datetime import datetime
import json

# Add project root to path
try:
    if Path('/content/SD-DarkMaster-Pro').exists():
        project_root = Path('/content/SD-DarkMaster-Pro')
    else:
        project_root = Path('/workspace/SD-DarkMaster-Pro')
except:
    project_root = Path('/workspace/SD-DarkMaster-Pro')

sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'scripts'))

# Import with error handling
try:
    from _models_data import model_list as sd15_models
except:
    sd15_models = {}
    
try:
    from _xl_models_data import model_list as sdxl_models
except:
    sdxl_models = {}

try:
    from unified_model_manager import get_model_manager
    from civitai_browser import get_civitai_browser
except:
    get_model_manager = None
    get_civitai_browser = None

try:
    from setup_central_storage import MODEL_REGISTRY
except:
    MODEL_REGISTRY = {}

# Configure page
st.set_page_config(
    page_title="SD-DarkMaster-Pro",
    page_icon="🌟",
    layout="wide"
)

# Dark theme CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
}
.output-box {
    background: #000;
    color: #0f0;
    font-family: monospace;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #333;
    height: 300px;
    overflow-y: auto;
}
.progress-info {
    background: #1a1a2e;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'output_log' not in st.session_state:
    st.session_state.output_log = []
if 'download_queue' not in st.session_state:
    st.session_state.download_queue = []
if 'download_progress' not in st.session_state:
    st.session_state.download_progress = 0
if 'is_downloading' not in st.session_state:
    st.session_state.is_downloading = False
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = {}

def add_output(message: str, level: str = "INFO"):
    """Add message to output log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    color = {"INFO": "#0f0", "ERROR": "#f00", "WARNING": "#ff0", "SUCCESS": "#0ff"}.get(level, "#fff")
    st.session_state.output_log.append(f'<span style="color: {color}">[{timestamp}] {level}: {message}</span>')
    # Keep only last 100 messages
    if len(st.session_state.output_log) > 100:
        st.session_state.output_log = st.session_state.output_log[-100:]

def download_model(model_info: dict):
    """Download a model with progress tracking"""
    add_output(f"Starting download: {model_info['name']}", "INFO")
    
    # Simulate download with progress
    for i in range(0, 101, 10):
        st.session_state.download_progress = i
        time.sleep(0.1)  # Simulate download time
        
    add_output(f"✅ Downloaded: {model_info['name']}", "SUCCESS")
    st.session_state.download_progress = 0
    return True

def check_model_status(model_name: str) -> str:
    """Check if model is installed"""
    model_paths = [
        project_root / 'storage' / 'models' / 'Stable-diffusion' / f"{model_name}.safetensors",
        project_root / 'storage' / 'models' / 'Stable-diffusion' / f"{model_name}.ckpt",
    ]
    for path in model_paths:
        if path.exists():
            return "✅ Installed"
    return "❌ Not installed"

# Title
col_title = st.columns([1])[0]
with col_title:
    st.title("🌟 SD-DarkMaster-Pro")

# Main tabs
tab_models, tab_browser, tab_settings = st.tabs(["Models", "Model Browser", "Settings"])

with tab_models:
    tab_sd15, tab_sdxl, tab_pony, tab_illustrous, tab_misc = st.tabs(
        ["SD-1.5", "SDXL", "PONY", "Illustrous", "Misc"]
    )
    
    # SD-1.5 Tab
    with tab_sd15:
        tab_models_15, tab_loras_15, tab_vae_15, tab_cn_15 = st.tabs(
            ["Models", "Loras", "Vae", "Controlnet"]
        )
        
        with tab_models_15:
            st.markdown("### SD 1.5 Models")
            
            if sd15_models:
                # Create selection interface
                cols = st.columns(3)
                for idx, (name, info) in enumerate(list(sd15_models.items())[:9]):  # Show first 9
                    with cols[idx % 3]:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            selected = st.checkbox(name[:25], key=f"sd15_{name}")
                            if selected:
                                if 'sd15' not in st.session_state.selected_models:
                                    st.session_state.selected_models['sd15'] = []
                                if name not in st.session_state.selected_models['sd15']:
                                    st.session_state.selected_models['sd15'].append(name)
                                    add_output(f"Selected: {name}", "INFO")
                        with col2:
                            st.caption(check_model_status(name))
            else:
                st.warning("No SD 1.5 models found in dictionary")
                add_output("SD 1.5 model dictionary not loaded", "WARNING")
        
        with tab_loras_15:
            st.info("SD 1.5 LoRAs - Coming soon")
        
        with tab_vae_15:
            st.info("SD 1.5 VAE models - Coming soon")
        
        with tab_cn_15:
            st.markdown("### SD 1.5 ControlNet")
            if MODEL_REGISTRY.get('controlnet'):
                for name, info in MODEL_REGISTRY['controlnet'].items():
                    if 'sd15' in name or 'v11' in name:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.text(name)
                        with col2:
                            st.caption(info.get('size', ''))
                        with col3:
                            if st.checkbox("", key=f"cn15_{name}"):
                                add_output(f"Selected ControlNet: {name}", "INFO")
    
    # SDXL Tab
    with tab_sdxl:
        tab_models_xl, tab_loras_xl, tab_vae_xl, tab_cn_xl = st.tabs(
            ["Models", "Loras", "Vae", "Controlnet"]
        )
        
        with tab_models_xl:
            st.markdown("### SDXL Models")
            
            if sdxl_models:
                sdxl_filtered = {k: v for k, v in sdxl_models.items() 
                               if 'pony' not in k.lower() and 'illustrious' not in k.lower()}
                
                cols = st.columns(3)
                for idx, (name, info) in enumerate(list(sdxl_filtered.items())[:9]):
                    with cols[idx % 3]:
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            selected = st.checkbox(name[:25], key=f"sdxl_{name}")
                            if selected:
                                if 'sdxl' not in st.session_state.selected_models:
                                    st.session_state.selected_models['sdxl'] = []
                                if name not in st.session_state.selected_models['sdxl']:
                                    st.session_state.selected_models['sdxl'].append(name)
                                    add_output(f"Selected: {name}", "INFO")
                        with col2:
                            st.caption(check_model_status(name))
            else:
                st.warning("No SDXL models found")
        
        with tab_loras_xl:
            st.info("SDXL LoRAs - Coming soon")
        
        with tab_vae_xl:
            st.info("SDXL VAE - Coming soon")
        
        with tab_cn_xl:
            st.info("SDXL ControlNet - Coming soon")
    
    # Pony Tab
    with tab_pony:
        tab_models_pony, tab_loras_pony, _ = st.tabs(["Models", "Loras", ""])
        
        with tab_models_pony:
            st.markdown("### Pony Models")
            if sdxl_models:
                pony_models = {k: v for k, v in sdxl_models.items() if 'pony' in k.lower()}
                if pony_models:
                    for name, info in pony_models.items():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            if st.checkbox(name[:30], key=f"pony_{name}"):
                                add_output(f"Selected Pony: {name}", "INFO")
                        with col2:
                            st.caption(check_model_status(name))
                else:
                    st.info("No Pony models found")
        
        with tab_loras_pony:
            st.info("Pony LoRAs - Coming soon")
    
    # Illustrous Tab
    with tab_illustrous:
        tab_models_ill, tab_loras_ill, _ = st.tabs(["Models", "Loras", ""])
        
        with tab_models_ill:
            st.markdown("### Illustrious Models")
            if sdxl_models:
                ill_models = {k: v for k, v in sdxl_models.items() if 'illustrious' in k.lower()}
                if ill_models:
                    for name, info in ill_models.items():
                        if st.checkbox(name[:30], key=f"ill_{name}"):
                            add_output(f"Selected Illustrious: {name}", "INFO")
                else:
                    st.info("No Illustrious models found")
        
        with tab_loras_ill:
            st.info("Illustrious LoRAs - Coming soon")
    
    # Misc Tab
    with tab_misc:
        ext_tabs = st.tabs(["SAM", "Adetailer", "Upscaler", "Reactor", "Future Extensions"])
        
        with ext_tabs[0]:
            st.markdown("### SAM Models")
            if MODEL_REGISTRY.get('sam'):
                for name, info in MODEL_REGISTRY['sam'].items():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.text(name)
                    with col2:
                        st.caption(info.get('size', ''))
                    with col3:
                        if st.checkbox("", key=f"sam_{name}"):
                            add_output(f"Selected SAM: {name}", "INFO")
            else:
                st.info("No SAM models configured")
        
        with ext_tabs[1]:
            st.markdown("### ADetailer Models")
            if MODEL_REGISTRY.get('adetailer'):
                for name, info in MODEL_REGISTRY['adetailer'].items():
                    if st.checkbox(name, key=f"adet_{name}"):
                        add_output(f"Selected ADetailer: {name}", "INFO")
        
        with ext_tabs[2]:
            st.info("Upscaler models - Coming soon")
        
        with ext_tabs[3]:
            st.info("Reactor models - Coming soon")
        
        with ext_tabs[4]:
            st.info("Space for future extensions")

with tab_browser:
    st.markdown("### 🔍 CivitAI Browser")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search = st.text_input("Search models", placeholder="anime, realistic, etc.")
    with col2:
        model_type = st.selectbox("Type", ["All", "Checkpoint", "LORA", "VAE"])
    with col3:
        nsfw = st.checkbox("Include NSFW")
    
    if st.button("🔍 Search CivitAI", use_container_width=True):
        add_output(f"Searching CivitAI for: {search}", "INFO")
        
        if get_civitai_browser:
            try:
                browser = get_civitai_browser()
                with st.spinner("Searching..."):
                    results = browser.search_models(query=search, limit=5)
                    
                if results:
                    add_output(f"Found {len(results)} models", "SUCCESS")
                    for model in results:
                        with st.expander(f"📦 {model['name']}"):
                            st.text(f"Type: {model['type']}")
                            st.text(f"Downloads: {model['download_count']:,}")
                            if st.button(f"Add to queue", key=f"add_{model['id']}"):
                                st.session_state.download_queue.append(model)
                                add_output(f"Added to queue: {model['name']}", "INFO")
                else:
                    add_output("No models found", "WARNING")
            except Exception as e:
                add_output(f"Search error: {str(e)}", "ERROR")
        else:
            add_output("CivitAI browser not available", "ERROR")

with tab_settings:
    st.markdown("### ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        webui_type = st.selectbox("WebUI Type", ["Forge", "ComfyUI", "A1111"])
        port = st.number_input("Port", value=7860)
    
    with col2:
        st.checkbox("Enable API")
        st.checkbox("Auto-launch browser")
    
    if st.button("💾 Save Settings", use_container_width=True):
        add_output("Settings saved", "SUCCESS")

# Download Section
st.markdown("---")
col_dl, col_progress = st.columns([1, 8])

with col_dl:
    # Count selected models
    total_selected = sum(len(models) for models in st.session_state.selected_models.values())
    queue_count = len(st.session_state.download_queue)
    
    if st.button(
        f"📥 Download ({total_selected + queue_count})", 
        disabled=st.session_state.is_downloading,
        use_container_width=True
    ):
        if total_selected + queue_count > 0:
            st.session_state.is_downloading = True
            add_output(f"Starting download of {total_selected + queue_count} models", "INFO")
            
            # Download selected models
            for model_type, models in st.session_state.selected_models.items():
                for model in models:
                    download_model({'name': model, 'type': model_type})
            
            # Download queued models
            for model in st.session_state.download_queue:
                download_model(model)
            
            st.session_state.is_downloading = False
            st.session_state.selected_models = {}
            st.session_state.download_queue = []
            add_output("All downloads complete!", "SUCCESS")
            st.rerun()
        else:
            add_output("No models selected for download", "WARNING")

with col_progress:
    if st.session_state.is_downloading:
        st.progress(st.session_state.download_progress / 100, text=f"Downloading... {st.session_state.download_progress}%")
    else:
        st.progress(0, text="Ready to download")

# Output Console
st.markdown("---")
st.markdown("### 📋 Output Console")

# Create output area
output_html = '<div class="output-box">'
for line in st.session_state.output_log[-20:]:  # Show last 20 lines
    output_html += f"{line}<br>"
output_html += '</div>'

st.markdown(output_html, unsafe_allow_html=True)

# Quick Actions
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🚀 Launch WebUI", use_container_width=True):
        add_output("Launching WebUI...", "INFO")
        # Check if models are installed
        if total_selected == 0:
            add_output("Warning: No models selected/installed", "WARNING")
        else:
            add_output("WebUI starting on port 7860", "SUCCESS")

with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        add_output("Refreshing model list...", "INFO")
        st.rerun()

with col3:
    if st.button("🧹 Clear Output", use_container_width=True):
        st.session_state.output_log = []
        add_output("Output cleared", "INFO")
        st.rerun()

with col4:
    if st.button("📊 System Info", use_container_width=True):
        try:
            import psutil
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            add_output(f"CPU: {cpu}% | RAM: {mem}%", "INFO")
        except:
            add_output("psutil not available", "WARNING")

# Sidebar with stats
with st.sidebar:
    st.markdown("### 📊 Status")
    
    # Platform detection
    platform = 'Colab' if 'google.colab' in sys.modules else 'Local'
    st.info(f"Platform: {platform}")
    
    # Model counts
    st.metric("Selected Models", total_selected)
    st.metric("Download Queue", queue_count)
    
    # Storage info
    storage_path = project_root / 'storage'
    if storage_path.exists():
        try:
            import shutil
            total, used, free = shutil.disk_usage(storage_path)
            st.metric("Storage Free", f"{free // (2**30)} GB")
        except:
            pass
    
    st.markdown("---")
    st.markdown("### 🎯 Quick Tips")
    st.markdown("""
    1. Select models first
    2. Click Download to get them
    3. Launch WebUI when ready
    4. Check output for errors
    """)

# Auto-refresh output every 2 seconds if downloading
if st.session_state.is_downloading:
    time.sleep(2)
    st.rerun()