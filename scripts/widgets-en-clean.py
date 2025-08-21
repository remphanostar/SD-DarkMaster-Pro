#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Dashboard - Clean Toggle Button Design
Full-width toggle buttons with color state changes
"""

import streamlit as st
import sys
from pathlib import Path

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

# Import model dictionaries
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

# Page config
st.set_page_config(
    page_title="SD-DarkMaster-Pro",
    page_icon="🌟",
    layout="wide"
)

# Custom CSS for button styling
st.markdown("""
<style>
/* Dark theme base */
.stApp {
    background: #1a1a1a;
}

/* Hide default Streamlit elements */
.css-1dp5vir { display: none; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Custom button styling */
.stButton > button {
    width: 100%;
    background-color: #2d2d30;
    color: #ffffff;
    border: 2px solid #3c3c3c;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 16px;
    font-weight: 500;
    transition: all 0.2s ease;
    margin: 4px 0;
}

.stButton > button:hover {
    background-color: #3d3d40;
    border-color: #ef4444;
}

/* Selected state (we'll use session state to apply this) */
.selected-model {
    background-color: #ef4444 !important;
    border-color: #ef4444 !important;
}

/* Download button special styling */
.download-button > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    border: none;
    font-weight: bold;
    padding: 14px 28px;
}

.download-button > button:hover {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
}

/* Progress bar styling */
.stProgress > div > div > div > div {
    background-color: #10b981;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #2d2d30;
    border-radius: 8px 8px 0 0;
    color: white;
    border: 1px solid #3c3c3c;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #3d3d40;
    border-bottom: 2px solid #ef4444;
}

/* Output console */
.output-console {
    background-color: #1e1e1e;
    border: 1px solid #3c3c3c;
    border-radius: 8px;
    padding: 12px;
    font-family: 'Courier New', monospace;
    color: #10b981;
    min-height: 100px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = set()
if 'output_log' not in st.session_state:
    st.session_state.output_log = []
if 'download_progress' not in st.session_state:
    st.session_state.download_progress = 0

def toggle_model(model_id):
    """Toggle model selection"""
    if model_id in st.session_state.selected_models:
        st.session_state.selected_models.remove(model_id)
        st.session_state.output_log.append(f"[-] Deselected: {model_id}")
    else:
        st.session_state.selected_models.add(model_id)
        st.session_state.output_log.append(f"[+] Selected: {model_id}")

def create_model_button(name, model_id, size="Unknown"):
    """Create a toggle button for model selection"""
    is_selected = model_id in st.session_state.selected_models
    
    # Button label with size info
    label = f"{name} ({size})"
    
    # Create button with dynamic styling
    if st.button(
        label,
        key=f"btn_{model_id}",
        use_container_width=True,
        type="primary" if is_selected else "secondary"
    ):
        toggle_model(model_id)
        st.rerun()

# Title
st.title("🌟 SD-DarkMaster-Pro Dashboard")
st.caption("Unified Model Management System")

# Main tabs
tab1, tab2, tab3 = st.tabs(["Models", "Model Browser", "Settings"])

with tab1:
    # Model type tabs
    model_tabs = st.tabs(["SD-1.5", "SDXL", "🦄 PONY", "Illustrous", "Misc"])
    
    with model_tabs[0]:  # SD-1.5
        sub_tabs = st.tabs(["Models", "Loras", "Vae", "Controlnet"])
        
        with sub_tabs[0]:  # Models
            st.markdown("#### SD 1.5 Checkpoints")
            
            if sd15_models:
                # Create columns for better layout (2 columns)
                col1, col2 = st.columns(2)
                
                for idx, (name, info) in enumerate(sd15_models.items()):
                    with col1 if idx % 2 == 0 else col2:
                        model_id = f"sd15_model_{name}"
                        create_model_button(name[:40], model_id, info.get('size', 'Unknown'))
            else:
                st.info("No SD 1.5 models available")
        
        with sub_tabs[1]:  # Loras
            st.markdown("#### SD 1.5 LoRAs")
            # Add LoRA models here
            st.info("LoRA models will appear here")
        
        with sub_tabs[2]:  # VAE
            st.markdown("#### SD 1.5 VAE")
            st.info("VAE models will appear here")
        
        with sub_tabs[3]:  # ControlNet
            st.markdown("#### SD 1.5 ControlNet")
            if MODEL_REGISTRY.get('controlnet'):
                col1, col2 = st.columns(2)
                cn_models = [(k, v) for k, v in MODEL_REGISTRY['controlnet'].items() 
                           if 'sd15' in k or 'v11' in k]
                
                for idx, (name, info) in enumerate(cn_models):
                    with col1 if idx % 2 == 0 else col2:
                        model_id = f"cn_{name}"
                        create_model_button(name[:40], model_id, info.get('size', 'Unknown'))
    
    with model_tabs[1]:  # SDXL
        sub_tabs = st.tabs(["Models", "Loras", "Vae", "Controlnet"])
        
        with sub_tabs[0]:
            st.markdown("#### SDXL Checkpoints")
            
            if sdxl_models:
                # Filter non-pony/illustrious
                sdxl_filtered = [(k, v) for k, v in sdxl_models.items() 
                               if 'pony' not in k.lower() and 'illustrious' not in k.lower()]
                
                col1, col2 = st.columns(2)
                for idx, (name, info) in enumerate(sdxl_filtered):
                    with col1 if idx % 2 == 0 else col2:
                        model_id = f"sdxl_model_{name}"
                        create_model_button(name[:40], model_id, info.get('size', 'Unknown'))
            else:
                st.info("No SDXL models available")
    
    with model_tabs[2]:  # PONY
        sub_tabs = st.tabs(["Models", "Loras"])
        
        with sub_tabs[0]:
            st.markdown("#### Pony Checkpoints")
            
            if sdxl_models:
                pony_models = [(k, v) for k, v in sdxl_models.items() if 'pony' in k.lower()]
                
                if pony_models:
                    col1, col2 = st.columns(2)
                    for idx, (name, info) in enumerate(pony_models):
                        with col1 if idx % 2 == 0 else col2:
                            model_id = f"pony_model_{name}"
                            create_model_button(name[:40], model_id, info.get('size', 'Unknown'))
                else:
                    st.info("No Pony models available")
    
    with model_tabs[3]:  # Illustrous
        sub_tabs = st.tabs(["Models", "Loras"])
        
        with sub_tabs[0]:
            st.markdown("#### Illustrious Checkpoints")
            
            if sdxl_models:
                ill_models = [(k, v) for k, v in sdxl_models.items() if 'illustrious' in k.lower()]
                
                if ill_models:
                    col1, col2 = st.columns(2)
                    for idx, (name, info) in enumerate(ill_models):
                        with col1 if idx % 2 == 0 else col2:
                            model_id = f"ill_model_{name}"
                            create_model_button(name[:40], model_id, info.get('size', 'Unknown'))
                else:
                    st.info("No Illustrious models available")
    
    with model_tabs[4]:  # Misc
        ext_tabs = st.tabs(["SAM", "ADetailer", "Upscaler", "Reactor", "Future"])
        
        with ext_tabs[0]:
            st.markdown("#### SAM Models")
            if MODEL_REGISTRY.get('sam'):
                col1, col2 = st.columns(2)
                for idx, (name, info) in enumerate(MODEL_REGISTRY['sam'].items()):
                    with col1 if idx % 2 == 0 else col2:
                        model_id = f"sam_{name}"
                        create_model_button(name, model_id, info.get('size', 'Unknown'))

with tab2:
    st.markdown("#### Model Browser")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search = st.text_input("Search", placeholder="Search CivitAI...")
    with col2:
        model_type = st.selectbox("Type", ["All", "Checkpoint", "LORA", "VAE"])
    with col3:
        if st.button("🔍 Search", use_container_width=True):
            st.session_state.output_log.append(f"Searching for: {search}")
            st.rerun()

with tab3:
    st.markdown("#### Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        webui = st.selectbox("WebUI Type", ["Forge", "ComfyUI", "A1111"])
        port = st.number_input("Port", value=7860, min_value=1000, max_value=65535)
    
    with col2:
        enable_api = st.checkbox("Enable API", value=False)
        auto_launch = st.checkbox("Auto-launch", value=True)
        share = st.checkbox("Share", value=False)

# Separator
st.markdown("---")

# Download section - single button
col1, col2, col3 = st.columns([2, 6, 2])

with col1:
    count = len(st.session_state.selected_models)
    # Special styling for download button
    st.markdown('<div class="download-button">', unsafe_allow_html=True)
    if st.button(f"📥 Download ({count} models)", use_container_width=True):
        if count > 0:
            st.session_state.output_log.append(f"Starting download of {count} models...")
            st.session_state.download_progress = 0.1
        else:
            st.session_state.output_log.append("No models selected for download")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Progress bar
    if st.session_state.download_progress > 0:
        st.progress(st.session_state.download_progress)
        st.caption(f"Downloading... {int(st.session_state.download_progress * 100)}%")
    else:
        st.progress(0)
        st.caption("Ready to download")

with col3:
    if st.button("🧹 Clear Selection", use_container_width=True):
        st.session_state.selected_models = set()
        st.session_state.output_log.append("Selection cleared")
        st.rerun()

# Output console
st.markdown("---")
st.markdown("#### 📋 Output Console")

# Display last 10 log entries
output_text = "\n".join(st.session_state.output_log[-10:]) if st.session_state.output_log else "System ready..."
st.code(output_text, language='bash')

# Quick stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Selected", len(st.session_state.selected_models))
with col2:
    st.metric("Available", len(sd15_models) + len(sdxl_models))
with col3:
    st.metric("Downloaded", "0")
with col4:
    st.metric("Storage", "0 GB")