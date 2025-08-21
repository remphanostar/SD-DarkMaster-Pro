#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Dashboard - Compact Design
Smaller buttons, more models visible, full names shown
"""

import streamlit as st
import sys
import os
import time
from pathlib import Path
from datetime import datetime

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
    from setup_central_storage import MODEL_REGISTRY
except:
    MODEL_REGISTRY = {}

# Configure page
st.set_page_config(
    page_title="SD-DarkMaster-Pro",
    page_icon="🌟",
    layout="wide"
)

# Compact Dark Theme CSS
st.markdown("""
<style>
/* Dark theme */
.stApp {
    background: #0a0a0a;
}

/* Make everything more compact */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 100%;
}

/* Smaller tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 1px;
    background: #1a1a2e;
    padding: 0.25rem;
    border-radius: 8px;
}

.stTabs [data-baseweb="tab"] {
    height: 32px;
    padding: 0.25rem 1rem;
    font-size: 13px;
    background: #2a2a3e;
    color: #e0e0e0;
}

.stTabs [aria-selected="true"] {
    background: #10B981 !important;
}

/* Compact model cards */
.model-item {
    background: #1a1a2e;
    border: 1px solid #2a2a3e;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 4px 2px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 36px;
    transition: all 0.2s;
}

.model-item:hover {
    background: #2a2a3e;
    border-color: #10B981;
}

.model-name {
    color: #e0e0e0;
    font-size: 13px;
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-right: 10px;
}

.model-info {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #888;
}

.status-badge {
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
}

.status-installed {
    background: #10B981;
    color: white;
}

.status-not-installed {
    background: #374151;
    color: #9CA3AF;
}

/* Smaller buttons */
.stButton > button {
    height: 28px;
    padding: 0 12px;
    font-size: 12px;
    background: #10B981;
    border: none;
    color: white;
    border-radius: 4px;
}

/* Compact checkboxes */
.stCheckbox {
    margin: 0;
    padding: 0;
}

.stCheckbox > label {
    font-size: 13px;
    margin: 0;
}

/* Output console */
.output-console {
    background: #000;
    color: #0f0;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    padding: 8px;
    border-radius: 4px;
    height: 200px;
    overflow-y: auto;
    border: 1px solid #333;
}

/* Reduce spacing */
.element-container {
    margin: 0;
}

hr {
    margin: 0.5rem 0;
}

/* Compact columns */
[data-testid="column"] {
    padding: 0 4px;
}

/* Small progress bar */
.stProgress > div {
    height: 20px;
}

/* Compact select boxes */
.stSelectbox > div > div {
    min-height: 30px;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'output_log' not in st.session_state:
    st.session_state.output_log = []
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = set()
if 'download_progress' not in st.session_state:
    st.session_state.download_progress = 0

def add_output(message: str, level: str = "INFO"):
    """Add message to output log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    color = {"INFO": "#0f0", "ERROR": "#f00", "WARNING": "#ff0", "SUCCESS": "#0ff"}.get(level, "#fff")
    st.session_state.output_log.append(f'<span style="color:{color}">[{timestamp}] {message}</span>')
    if len(st.session_state.output_log) > 50:
        st.session_state.output_log = st.session_state.output_log[-50:]

def render_model_grid(models: dict, prefix: str):
    """Render models in a compact grid"""
    if not models:
        st.info("No models found")
        return
    
    # Create 2-column layout for compact display
    cols = st.columns(2)
    
    for idx, (name, info) in enumerate(models.items()):
        with cols[idx % 2]:
            # Create custom HTML for compact model item
            model_key = f"{prefix}_{name}"
            is_selected = model_key in st.session_state.selected_models
            
            # Container with checkbox and info
            container = st.container()
            with container:
                col1, col2, col3 = st.columns([1, 3, 1])
                
                with col1:
                    if st.checkbox("", key=f"cb_{model_key}", value=is_selected):
                        st.session_state.selected_models.add(model_key)
                        add_output(f"Selected: {name[:40]}", "INFO")
                    else:
                        st.session_state.selected_models.discard(model_key)
                
                with col2:
                    # Show full name with tooltip
                    st.markdown(f"""
                    <div class="model-item">
                        <span class="model-name" title="{name}">{name}</span>
                        <span class="model-info">{info.get('size', 'Unknown')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    # Check if installed
                    installed = check_if_installed(name, prefix)
                    if installed:
                        st.markdown('<span class="status-badge status-installed">✓</span>', unsafe_allow_html=True)
                    else:
                        if st.button("↓", key=f"dl_{model_key}", help="Download"):
                            add_output(f"Downloading: {name[:40]}", "INFO")

def check_if_installed(model_name: str, model_type: str) -> bool:
    """Check if model is installed"""
    paths = [
        project_root / 'storage' / 'models' / 'Stable-diffusion' / f"{model_name}.safetensors",
        project_root / 'storage' / 'models' / 'Stable-diffusion' / f"{model_name}.ckpt",
    ]
    return any(p.exists() for p in paths)

# Title - Compact
st.markdown("# 🌟 SD-DarkMaster-Pro Dashboard")
st.markdown("##### Unified Model Management System")

# Main tabs
tab_models, tab_browser, tab_settings = st.tabs(["Models", "Model Browser", "Settings"])

with tab_models:
    # Model type tabs
    tab_sd15, tab_sdxl, tab_pony, tab_illustrous, tab_misc = st.tabs(
        ["SD-1.5", "SDXL", "🦄PONY", "Illustrous", "Misc"]
    )
    
    with tab_sd15:
        # Sub-tabs for SD 1.5
        sub_tabs = st.tabs(["Models", "Loras", "Vae", "Controlnet"])
        
        with sub_tabs[0]:
            st.markdown("##### SD 1.5 Checkpoints")
            
            # Show all models in compact grid
            if sd15_models:
                render_model_grid(sd15_models, "sd15")
            else:
                st.warning("No SD 1.5 models in dictionary")
        
        with sub_tabs[1]:
            st.markdown("##### SD 1.5 LoRAs")
            lora_path = project_root / 'storage' / 'models' / 'Lora'
            if lora_path.exists():
                loras = list(lora_path.glob('*.safetensors'))
                if loras:
                    cols = st.columns(3)
                    for idx, lora in enumerate(loras):
                        with cols[idx % 3]:
                            st.checkbox(lora.stem[:30], key=f"lora_{lora.name}")
                else:
                    st.info("No LoRAs found")
        
        with sub_tabs[2]:
            st.markdown("##### SD 1.5 VAE")
            st.info("VAE models will appear here")
        
        with sub_tabs[3]:
            st.markdown("##### SD 1.5 ControlNet")
            if MODEL_REGISTRY.get('controlnet'):
                cn_models = {k: v for k, v in MODEL_REGISTRY['controlnet'].items() 
                           if 'sd15' in k or 'v11' in k}
                render_model_grid(cn_models, "cn15")
    
    with tab_sdxl:
        sub_tabs = st.tabs(["Models", "Loras", "Vae", "Controlnet"])
        
        with sub_tabs[0]:
            st.markdown("##### SDXL Checkpoints")
            
            if sdxl_models:
                # Filter out Pony and Illustrious
                sdxl_filtered = {k: v for k, v in sdxl_models.items() 
                               if 'pony' not in k.lower() and 'illustrious' not in k.lower()}
                render_model_grid(sdxl_filtered, "sdxl")
            else:
                st.warning("No SDXL models found")
        
        with sub_tabs[1]:
            st.info("SDXL LoRAs")
        
        with sub_tabs[2]:
            st.info("SDXL VAE")
        
        with sub_tabs[3]:
            st.info("SDXL ControlNet")
    
    with tab_pony:
        sub_tabs = st.tabs(["Models", "Loras", ""])
        
        with sub_tabs[0]:
            st.markdown("##### Pony Checkpoints")
            
            if sdxl_models:
                pony_models = {k: v for k, v in sdxl_models.items() 
                             if 'pony' in k.lower()}
                if pony_models:
                    render_model_grid(pony_models, "pony")
                else:
                    st.info("No Pony models found")
        
        with sub_tabs[1]:
            st.info("Pony LoRAs")
    
    with tab_illustrous:
        sub_tabs = st.tabs(["Models", "Loras", ""])
        
        with sub_tabs[0]:
            st.markdown("##### Illustrious Checkpoints")
            
            if sdxl_models:
                ill_models = {k: v for k, v in sdxl_models.items() 
                            if 'illustrious' in k.lower()}
                if ill_models:
                    render_model_grid(ill_models, "illustrious")
                else:
                    st.info("No Illustrious models found")
        
        with sub_tabs[1]:
            st.info("Illustrious LoRAs")
    
    with tab_misc:
        ext_tabs = st.tabs(["SAM", "ADetailer", "Upscaler", "Reactor", "Future"])
        
        with ext_tabs[0]:
            st.markdown("##### SAM Models")
            if MODEL_REGISTRY.get('sam'):
                render_model_grid(MODEL_REGISTRY['sam'], "sam")
        
        with ext_tabs[1]:
            st.markdown("##### ADetailer Models")
            if MODEL_REGISTRY.get('adetailer'):
                render_model_grid(MODEL_REGISTRY['adetailer'], "adet")
        
        with ext_tabs[2]:
            st.markdown("##### Upscaler Models")
            if MODEL_REGISTRY.get('upscalers'):
                render_model_grid(MODEL_REGISTRY['upscalers'], "upscale")
        
        with ext_tabs[3]:
            st.markdown("##### Reactor Models")
            if MODEL_REGISTRY.get('reactor'):
                render_model_grid(MODEL_REGISTRY['reactor'], "reactor")
        
        with ext_tabs[4]:
            st.info("Future extensions")

with tab_browser:
    st.markdown("##### CivitAI Browser")
    
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    with col1:
        search = st.text_input("", placeholder="Search models...")
    with col2:
        model_type = st.selectbox("", ["All", "Checkpoint", "LORA"])
    with col3:
        sort_by = st.selectbox("", ["Most Downloaded", "Newest"])
    with col4:
        if st.button("🔍 Search"):
            add_output(f"Searching: {search}", "INFO")

with tab_settings:
    st.markdown("##### Settings")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox("WebUI", ["Forge", "ComfyUI", "A1111"])
    with col2:
        st.number_input("Port", value=7860, min_value=1000, max_value=65535)
    with col3:
        st.checkbox("Auto-launch")

# Download bar and output
st.markdown("---")

# Download section - compact
col1, col2 = st.columns([1, 6])
with col1:
    selected_count = len(st.session_state.selected_models)
    if st.button(f"📥 Download ({selected_count})"):
        if selected_count > 0:
            add_output(f"Downloading {selected_count} models...", "INFO")
            st.session_state.download_progress = 50
        else:
            add_output("No models selected", "WARNING")

with col2:
    st.progress(st.session_state.download_progress / 100)

# Output console - compact
st.markdown("##### Output")
output_html = '<div class="output-console">'
for line in st.session_state.output_log[-15:]:  # Show last 15 lines
    output_html += f"{line}<br>"
output_html += '</div>'
st.markdown(output_html, unsafe_allow_html=True)

# Quick actions bar
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🚀 Launch"):
        add_output("Launching WebUI...", "SUCCESS")
with col2:
    if st.button("🔄 Refresh"):
        st.rerun()
with col3:
    if st.button("🧹 Clear"):
        st.session_state.output_log = []
        st.rerun()
with col4:
    if st.button("📊 Stats"):
        add_output(f"Models: {selected_count} selected", "INFO")
with col5:
    if st.button("❌ Stop"):
        add_output("Stopped", "WARNING")