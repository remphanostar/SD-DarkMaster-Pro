#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Dashboard - Clean Toggle Design
Using st.toggle for model selection
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

# Dark theme CSS
st.markdown("""
<style>
.stApp { background: #0a0a0a; }
.main .block-container { padding-top: 1rem; max-width: 100%; }

/* Style for toggles */
.stToggle {
    background: #1a1a2e;
    border-radius: 6px;
    padding: 4px;
    margin: 2px 0;
}

/* Compact tabs */
.stTabs [data-baseweb="tab"] {
    height: 36px;
    padding: 6px 16px;
    font-size: 14px;
}

/* Hide link icon */
.css-1dp5vir { display: none; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_count' not in st.session_state:
    st.session_state.selected_count = 0
if 'output_log' not in st.session_state:
    st.session_state.output_log = []

# Title
st.title("🌟 SD-DarkMaster-Pro Dashboard")
st.caption("Unified Model Management System")

# Main tabs
tab1, tab2, tab3 = st.tabs(["Models", "Model Browser", "Settings"])

with tab1:
    # Model type tabs
    tab_sd15, tab_sdxl, tab_pony, tab_illustrous, tab_misc = st.tabs(
        ["SD-1.5", "SDXL", "🦄 PONY", "Illustrous", "Misc"]
    )
    
    with tab_sd15:
        # Sub tabs
        sub1, sub2, sub3, sub4 = st.tabs(["Models", "Loras", "Vae", "Controlnet"])
        
        with sub1:
            st.markdown("#### SD 1.5 Checkpoints")
            st.markdown('<a href="#" id="link-icon">🔗</a>', unsafe_allow_html=True)
            
            if sd15_models:
                # Create 2 columns for model display
                col1, col2 = st.columns(2)
                
                model_list = list(sd15_models.items())
                for idx, (name, info) in enumerate(model_list):
                    with col1 if idx % 2 == 0 else col2:
                        # Create container for each model
                        with st.container():
                            c1, c2, c3 = st.columns([1, 4, 1])
                            
                            with c1:
                                # Toggle for selection
                                selected = st.toggle("", value=False, key=f"sd15_{name}")
                                if selected:
                                    st.session_state.selected_count += 1
                            
                            with c2:
                                # Model name and size
                                st.markdown(f"**{name}**")
                                st.caption(info.get('size', 'Unknown'))
                            
                            with c3:
                                # Download arrow
                                st.markdown("↓")
            else:
                st.info("No SD 1.5 models found")
        
        with sub2:
            st.markdown("#### SD 1.5 LoRAs")
            st.info("LoRA models will appear here")
        
        with sub3:
            st.markdown("#### SD 1.5 VAE")
            st.info("VAE models will appear here")
        
        with sub4:
            st.markdown("#### SD 1.5 ControlNet")
            if MODEL_REGISTRY.get('controlnet'):
                col1, col2 = st.columns(2)
                cn_models = [(k, v) for k, v in MODEL_REGISTRY['controlnet'].items() 
                           if 'sd15' in k or 'v11' in k]
                
                for idx, (name, info) in enumerate(cn_models):
                    with col1 if idx % 2 == 0 else col2:
                        with st.container():
                            c1, c2, c3 = st.columns([1, 4, 1])
                            with c1:
                                st.toggle("", value=False, key=f"cn_{name}")
                            with c2:
                                st.markdown(f"**{name}**")
                                st.caption(info.get('size', 'Unknown'))
                            with c3:
                                st.markdown("↓")
    
    with tab_sdxl:
        sub1, sub2, sub3, sub4 = st.tabs(["Models", "Loras", "Vae", "Controlnet"])
        
        with sub1:
            st.markdown("#### SDXL Checkpoints")
            
            if sdxl_models:
                # Filter non-pony/illustrious
                sdxl_filtered = [(k, v) for k, v in sdxl_models.items() 
                               if 'pony' not in k.lower() and 'illustrious' not in k.lower()]
                
                col1, col2 = st.columns(2)
                for idx, (name, info) in enumerate(sdxl_filtered):
                    with col1 if idx % 2 == 0 else col2:
                        with st.container():
                            c1, c2, c3 = st.columns([1, 4, 1])
                            with c1:
                                st.toggle("", value=False, key=f"sdxl_{name}")
                            with c2:
                                st.markdown(f"**{name}**")
                                st.caption(info.get('size', 'Unknown'))
                            with c3:
                                st.markdown("↓")
            else:
                st.info("No SDXL models found")
    
    with tab_pony:
        sub1, sub2 = st.tabs(["Models", "Loras"])
        
        with sub1:
            st.markdown("#### Pony Checkpoints")
            
            if sdxl_models:
                pony_models = [(k, v) for k, v in sdxl_models.items() if 'pony' in k.lower()]
                
                if pony_models:
                    for name, info in pony_models:
                        with st.container():
                            c1, c2, c3 = st.columns([1, 4, 1])
                            with c1:
                                st.toggle("", value=False, key=f"pony_{name}")
                            with c2:
                                st.markdown(f"**{name}**")
                                st.caption(info.get('size', 'Unknown'))
                            with c3:
                                st.markdown("↓")
                else:
                    st.info("No Pony models found")
    
    with tab_illustrous:
        sub1, sub2 = st.tabs(["Models", "Loras"])
        
        with sub1:
            st.markdown("#### Illustrious Checkpoints")
            
            if sdxl_models:
                ill_models = [(k, v) for k, v in sdxl_models.items() if 'illustrious' in k.lower()]
                
                if ill_models:
                    for name, info in ill_models:
                        with st.container():
                            c1, c2, c3 = st.columns([1, 4, 1])
                            with c1:
                                st.toggle("", value=False, key=f"ill_{name}")
                            with c2:
                                st.markdown(f"**{name}**")
                                st.caption(info.get('size', 'Unknown'))
                            with c3:
                                st.markdown("↓")
                else:
                    st.info("No Illustrious models found")
    
    with tab_misc:
        ext1, ext2, ext3, ext4, ext5 = st.tabs(["SAM", "ADetailer", "Upscaler", "Reactor", "Future"])
        
        with ext1:
            st.markdown("#### SAM Models")
            if MODEL_REGISTRY.get('sam'):
                for name, info in MODEL_REGISTRY['sam'].items():
                    with st.container():
                        c1, c2, c3 = st.columns([1, 4, 1])
                        with c1:
                            st.toggle("", value=False, key=f"sam_{name}")
                        with c2:
                            st.markdown(f"**{name}**")
                            st.caption(info.get('size', 'Unknown'))
                        with c3:
                            st.markdown("↓")

with tab2:
    st.markdown("#### Model Browser")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search = st.text_input("Search", placeholder="Search CivitAI...")
    with col2:
        model_type = st.selectbox("Type", ["All", "Checkpoint", "LORA", "VAE"])
    with col3:
        if st.button("🔍 Search"):
            st.session_state.output_log.append(f"Searching for: {search}")

with tab3:
    st.markdown("#### Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        webui = st.selectbox("WebUI Type", ["Forge", "ComfyUI", "A1111"])
        port = st.number_input("Port", value=7860)
    
    with col2:
        st.toggle("Enable API", value=False)
        st.toggle("Auto-launch", value=True)

# Download section
st.markdown("---")
col1, col2 = st.columns([1, 10])

with col1:
    # Count selected toggles
    count = sum(1 for key in st.session_state if key.startswith(('sd15_', 'sdxl_', 'pony_', 'ill_', 'sam_', 'cn_')) and st.session_state[key])
    
    if st.button(f"📥 Download ({count})"):
        if count > 0:
            st.session_state.output_log.append(f"Downloading {count} models...")
        else:
            st.session_state.output_log.append("No models selected")

with col2:
    st.progress(0)

# Output
st.markdown("#### Output")
output_text = "\n".join(st.session_state.output_log[-10:]) if st.session_state.output_log else "Ready..."
st.text_area("", value=output_text, height=100, disabled=True)