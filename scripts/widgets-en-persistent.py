#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Dashboard - Persistent Toggle Buttons
Buttons that maintain their selected state visually
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

# Initialize session state
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = set()
if 'output_log' not in st.session_state:
    st.session_state.output_log = []
if 'download_progress' not in st.session_state:
    st.session_state.download_progress = 0

# Custom CSS for persistent button states
st.markdown("""
<style>
/* Dark theme base */
.stApp {
    background: #1a1a1a;
}

/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.css-1dp5vir { display: none; }

/* Model button container */
.model-button {
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
    cursor: pointer;
    text-align: center;
    display: block;
}

.model-button:hover {
    background-color: #3d3d40;
    border-color: #ef4444;
}

/* Selected state */
.model-button-selected {
    background-color: #ef4444 !important;
    border-color: #dc2626 !important;
    color: #ffffff !important;
}

.model-button-selected:hover {
    background-color: #dc2626 !important;
    border-color: #b91c1c !important;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
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

/* Download button */
.download-section {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #3c3c3c;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #10b981;
}

/* Output console */
.stCode {
    background-color: #1e1e1e !important;
    border: 1px solid #3c3c3c !important;
}
</style>
""", unsafe_allow_html=True)

def create_model_button(name, model_id, size="Unknown", col_container=None):
    """Create a persistent toggle button for model selection"""
    is_selected = model_id in st.session_state.selected_models
    
    # Create unique key for button
    button_key = f"btn_{model_id}"
    
    # Display button with persistent state
    button_class = "model-button-selected" if is_selected else "model-button"
    button_html = f"""
    <div class="{button_class}" id="{button_key}">
        {name} ({size})
    </div>
    """
    
    # Use container if provided, otherwise use st directly
    container = col_container if col_container else st
    
    # Display the styled button
    container.markdown(button_html, unsafe_allow_html=True)
    
    # Create an actual Streamlit button (invisible) for interaction
    if container.button("", key=button_key, use_container_width=True, help=f"Click to toggle {name}"):
        if model_id in st.session_state.selected_models:
            st.session_state.selected_models.remove(model_id)
            st.session_state.output_log.append(f"[-] Deselected: {name}")
        else:
            st.session_state.selected_models.add(model_id)
            st.session_state.output_log.append(f"[+] Selected: {name}")
        st.rerun()

def render_model_grid(models, prefix, num_cols=2):
    """Render a grid of model buttons"""
    if not models:
        st.info(f"No {prefix} models available")
        return
    
    # Create columns
    cols = st.columns(num_cols)
    
    # Distribute models across columns
    for idx, (name, info) in enumerate(models):
        col_idx = idx % num_cols
        with cols[col_idx]:
            model_id = f"{prefix}_{name}"
            # Create container for the button
            container = st.container()
            with container:
                # Check if selected to apply correct styling
                is_selected = model_id in st.session_state.selected_models
                button_class = "model-button-selected" if is_selected else "model-button"
                
                # Render styled div
                st.markdown(f"""
                <div class="{button_class}">
                    {name[:40]} ({info.get('size', 'Unknown')})
                </div>
                """, unsafe_allow_html=True)
                
                # Invisible button for click handling
                if st.button("", key=f"btn_{model_id}", use_container_width=True):
                    if model_id in st.session_state.selected_models:
                        st.session_state.selected_models.remove(model_id)
                        st.session_state.output_log.append(f"[-] Deselected: {name}")
                    else:
                        st.session_state.selected_models.add(model_id)
                        st.session_state.output_log.append(f"[+] Selected: {name}")
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
                models_list = list(sd15_models.items())
                render_model_grid(models_list, "sd15_model")
            else:
                st.info("No SD 1.5 models available")
        
        with sub_tabs[1]:  # Loras
            st.markdown("#### SD 1.5 LoRAs")
            st.info("LoRA models will appear here")
        
        with sub_tabs[2]:  # VAE
            st.markdown("#### SD 1.5 VAE")
            st.info("VAE models will appear here")
        
        with sub_tabs[3]:  # ControlNet
            st.markdown("#### SD 1.5 ControlNet")
            if MODEL_REGISTRY.get('controlnet'):
                cn_models = [(k, v) for k, v in MODEL_REGISTRY['controlnet'].items() 
                           if 'sd15' in k or 'v11' in k]
                render_model_grid(cn_models, "cn")
            else:
                st.info("No ControlNet models available")
    
    with model_tabs[1]:  # SDXL
        sub_tabs = st.tabs(["Models", "Loras", "Vae", "Controlnet"])
        
        with sub_tabs[0]:
            st.markdown("#### SDXL Checkpoints")
            
            if sdxl_models:
                # Filter non-pony/illustrious
                sdxl_filtered = [(k, v) for k, v in sdxl_models.items() 
                               if 'pony' not in k.lower() and 'illustrious' not in k.lower()]
                render_model_grid(sdxl_filtered, "sdxl_model")
            else:
                st.info("No SDXL models available")
    
    with model_tabs[2]:  # PONY
        sub_tabs = st.tabs(["Models", "Loras"])
        
        with sub_tabs[0]:
            st.markdown("#### Pony Checkpoints")
            
            if sdxl_models:
                pony_models = [(k, v) for k, v in sdxl_models.items() if 'pony' in k.lower()]
                render_model_grid(pony_models, "pony_model")
            else:
                st.info("No Pony models available")
    
    with model_tabs[3]:  # Illustrous
        sub_tabs = st.tabs(["Models", "Loras"])
        
        with sub_tabs[0]:
            st.markdown("#### Illustrious Checkpoints")
            
            if sdxl_models:
                ill_models = [(k, v) for k, v in sdxl_models.items() if 'illustrious' in k.lower()]
                render_model_grid(ill_models, "ill_model")
            else:
                st.info("No Illustrious models available")
    
    with model_tabs[4]:  # Misc
        ext_tabs = st.tabs(["SAM", "ADetailer", "Upscaler", "Reactor", "Future"])
        
        with ext_tabs[0]:
            st.markdown("#### SAM Models")
            if MODEL_REGISTRY.get('sam'):
                sam_models = list(MODEL_REGISTRY['sam'].items())
                render_model_grid(sam_models, "sam")
            else:
                st.info("No SAM models available")
        
        with ext_tabs[1]:
            st.markdown("#### ADetailer Models")
            st.info("ADetailer models will appear here")

with tab2:
    st.markdown("#### 🔍 Model Browser")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search = st.text_input("Search", placeholder="Search CivitAI for models...")
    with col2:
        model_type = st.selectbox("Type", ["All", "Checkpoint", "LORA", "VAE", "ControlNet"])
    with col3:
        if st.button("🔍 Search", use_container_width=True):
            st.session_state.output_log.append(f"Searching CivitAI for: {search} (Type: {model_type})")
            st.rerun()
    
    # Results area
    st.markdown("---")
    st.info("Search results will appear here")

with tab3:
    st.markdown("#### ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("WebUI Configuration")
        webui = st.selectbox("WebUI Type", ["Forge", "ComfyUI", "A1111", "ReForge"])
        port = st.number_input("Port", value=7860, min_value=1000, max_value=65535)
        theme = st.selectbox("Theme", ["Dark", "Light", "Auto"])
    
    with col2:
        st.subheader("Options")
        enable_api = st.checkbox("Enable API", value=False)
        auto_launch = st.checkbox("Auto-launch WebUI", value=True)
        share = st.checkbox("Create public link", value=False)
        xformers = st.checkbox("Enable xFormers", value=True)

# Download section
st.markdown('<div class="download-section"></div>', unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns([2, 6, 2])

with col1:
    count = len(st.session_state.selected_models)
    # Download button with count
    if st.button(f"📥 Download ({count} models)", use_container_width=True, type="primary"):
        if count > 0:
            st.session_state.output_log.append(f"🚀 Starting download of {count} models...")
            st.session_state.download_progress = 0.1
            # Here you would trigger actual download
        else:
            st.session_state.output_log.append("⚠️ No models selected for download")
        st.rerun()

with col2:
    # Progress bar
    if st.session_state.download_progress > 0:
        st.progress(st.session_state.download_progress)
        st.caption(f"Downloading... {int(st.session_state.download_progress * 100)}%")
    else:
        st.progress(0)
        if count > 0:
            st.caption(f"Ready to download {count} models")
        else:
            st.caption("Select models to download")

with col3:
    if st.button("🧹 Clear All", use_container_width=True):
        st.session_state.selected_models = set()
        st.session_state.output_log.append("✨ Selection cleared")
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
    st.metric("Selected", len(st.session_state.selected_models), delta=None)
with col2:
    total_models = len(sd15_models) + len(sdxl_models) if sd15_models and sdxl_models else 0
    st.metric("Available", total_models)
with col3:
    st.metric("Downloaded", "0")
with col4:
    st.metric("Storage", "0 GB")

# Debug info (can be removed in production)
with st.expander("Debug Info"):
    st.write("Selected Models:", st.session_state.selected_models)