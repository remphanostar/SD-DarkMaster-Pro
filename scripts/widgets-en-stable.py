#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Dashboard - Stable Version with Your Exact Tab Structure
No jumping, consistent layout, comprehensive features
"""

import streamlit as st
import sys
import json
import requests
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

# Import model dictionaries with error handling
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

# CSS for consistent layout and button styling
st.markdown("""
<style>
/* Dark theme */
.stApp {
    background: #0e0e0e;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Consistent tab heights - prevent jumping */
.stTabs {
    min-height: 50px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background-color: transparent;
    align-items: stretch;
    min-height: 45px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #1a1a1a;
    border-radius: 8px 8px 0 0;
    color: #ffffff;
    border: 1px solid #2a2a2a;
    padding: 10px 16px;
    min-height: 42px;
}

.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #2a2a2a;
    border-bottom: 3px solid #ef4444;
}

/* Model buttons */
.model-button {
    width: 100%;
    background-color: #1a1a1a;
    color: #ffffff;
    border: 2px solid #2a2a2a;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 15px;
    font-weight: 500;
    transition: all 0.2s ease;
    margin: 4px 0;
    cursor: pointer;
    text-align: center;
}

.model-button:hover {
    background-color: #2a2a2a;
    border-color: #ef4444;
}

.model-button-selected {
    background-color: #ef4444 !important;
    border-color: #dc2626 !important;
}

/* Hide the actual button but keep it clickable */
.stButton > button {
    opacity: 0;
    height: 0px;
    padding: 0;
    margin: -20px 0 0 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = set()
if 'output_log' not in st.session_state:
    st.session_state.output_log = []
if 'download_queue' not in st.session_state:
    st.session_state.download_queue = []
if 'civitai_cache' not in st.session_state:
    st.session_state.civitai_cache = {}

def safe_render_button(name, model_id, size="Unknown"):
    """Safely render a model button without problematic parameters"""
    is_selected = model_id in st.session_state.selected_models
    button_class = "model-button-selected" if is_selected else "model-button"
    
    # Display the styled div
    st.markdown(f"""
    <div class="{button_class}">
        {name[:40]} ({size})
    </div>
    """, unsafe_allow_html=True)
    
    # Create invisible button for interaction (no label_visibility parameter)
    if st.button("", key=f"btn_{model_id}"):
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

# YOUR EXACT TAB STRUCTURE
col1 = st.columns([1])[0]

with col1:
    # Level 1: Main tabs
    tab2, tab3 = st.tabs(["Models", "Model search"])
    
    with tab2:  # Models tab
        # Level 2: Model types
        tab4, tab5 = st.tabs(["Sdxl", "etc"])
        
        with tab4:  # Sdxl
            # Level 3: Sub-categories
            tab6, tab7, tab8 = st.tabs(["Model", "Lora", "Etc"])
            
            with tab6:  # SDXL Models
                st.markdown("#### SDXL Checkpoints")
                if sdxl_models:
                    # Filter out pony/illustrious for main SDXL
                    sdxl_filtered = [(k, v) for k, v in sdxl_models.items() 
                                   if 'pony' not in k.lower() and 'illustrious' not in k.lower()]
                    
                    cols = st.columns(2)
                    for idx, (name, info) in enumerate(sdxl_filtered):
                        with cols[idx % 2]:
                            safe_render_button(name, f"sdxl_{name}", info.get('size', 'Unknown'))
                else:
                    st.info("No SDXL models available")
            
            with tab7:  # SDXL Loras
                st.markdown("#### SDXL LoRAs")
                st.info("SDXL LoRAs will appear here")
            
            with tab8:  # SDXL Etc (VAE, ControlNet, etc)
                st.markdown("#### SDXL Additional Models")
                sub_tabs = st.tabs(["VAE", "ControlNet", "Embeddings"])
                
                with sub_tabs[0]:
                    st.info("SDXL VAE models will appear here")
                
                with sub_tabs[1]:
                    st.info("SDXL ControlNet models will appear here")
                
                with sub_tabs[2]:
                    st.info("SDXL Embeddings will appear here")
        
        with tab5:  # etc (SD1.5, Pony, Illustrious, Misc)
            # Additional model types
            model_tabs = st.tabs(["SD-1.5", "Pony", "Illustrious", "Misc"])
            
            with model_tabs[0]:  # SD-1.5
                sub = st.tabs(["Models", "Loras", "VAE", "ControlNet"])
                
                with sub[0]:
                    st.markdown("#### SD 1.5 Checkpoints")
                    if sd15_models:
                        cols = st.columns(2)
                        for idx, (name, info) in enumerate(list(sd15_models.items())):
                            with cols[idx % 2]:
                                safe_render_button(name, f"sd15_{name}", info.get('size', 'Unknown'))
                    else:
                        st.info("No SD 1.5 models available")
                
                with sub[1]:
                    st.info("SD 1.5 LoRAs will appear here")
                
                with sub[2]:
                    st.info("SD 1.5 VAE models will appear here")
                
                with sub[3]:
                    st.info("SD 1.5 ControlNet models will appear here")
            
            with model_tabs[1]:  # Pony
                st.markdown("#### Pony Models")
                if sdxl_models:
                    pony_models = [(k, v) for k, v in sdxl_models.items() if 'pony' in k.lower()]
                    if pony_models:
                        cols = st.columns(2)
                        for idx, (name, info) in enumerate(pony_models):
                            with cols[idx % 2]:
                                safe_render_button(name, f"pony_{name}", info.get('size', 'Unknown'))
                    else:
                        st.info("No Pony models found")
            
            with model_tabs[2]:  # Illustrious
                st.markdown("#### Illustrious Models")
                if sdxl_models:
                    ill_models = [(k, v) for k, v in sdxl_models.items() if 'illustrious' in k.lower()]
                    if ill_models:
                        cols = st.columns(2)
                        for idx, (name, info) in enumerate(ill_models):
                            with cols[idx % 2]:
                                safe_render_button(name, f"ill_{name}", info.get('size', 'Unknown'))
                    else:
                        st.info("No Illustrious models found")
            
            with model_tabs[3]:  # Misc
                ext_tabs = st.tabs(["SAM", "ADetailer", "Upscaler", "Reactor"])
                
                with ext_tabs[0]:
                    st.info("SAM models will appear here")
                with ext_tabs[1]:
                    st.info("ADetailer models will appear here")
                with ext_tabs[2]:
                    st.info("Upscaler models will appear here")
                with ext_tabs[3]:
                    st.info("Reactor models will appear here")
    
    with tab3:  # Model search tab
        # Level 2: Search sources
        tab9, tab10, tab11, tab12 = st.tabs([
            "Civtai search",
            "HF search", 
            "Browse local PC (not colab instance actual PC)",
            "Queue"
        ])
        
        with tab9:  # CivitAI search
            # Level 3: View types
            tab13, tab14, tab15 = st.tabs([
                "Model page basic + pic basic",
                "Verbose every detail",
                "Download Queue"
            ])
            
            with tab13:  # Basic view
                st.markdown("#### 🔍 CivitAI Basic Search")
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    search = st.text_input("Search", placeholder="anime, realistic, etc...")
                with col2:
                    model_type = st.selectbox("Type", ["All", "Checkpoint", "LORA", "VAE"])
                with col3:
                    if st.button("🔍 Search"):
                        st.session_state.output_log.append(f"Searching: {search}")
                        st.rerun()
                
                st.markdown("---")
                st.info("Search results with preview images will appear here")
            
            with tab14:  # Verbose view
                st.markdown("#### 📊 Verbose Model Information")
                st.markdown("*Everything available from the CivitAI API*")
                
                model_id = st.text_input("Enter Model ID", placeholder="e.g., 4384")
                if st.button("Load Full Details"):
                    st.session_state.output_log.append(f"Loading model {model_id} details...")
                
                # Example verbose info structure
                with st.expander("Model Stats", expanded=True):
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Downloads", "0")
                    with col2:
                        st.metric("Likes", "0")
                    with col3:
                        st.metric("Rating", "0.0⭐")
                    with col4:
                        st.metric("Reviews", "0")
                
                with st.expander("Tags & Metadata"):
                    st.info("Tags, trigger words, training details will appear here")
                
                with st.expander("Sample Images & Prompts"):
                    st.info("Image gallery with full prompt data will appear here")
                
                with st.expander("Version History"):
                    st.info("All model versions and files will appear here")
                
                with st.expander("Creator Info"):
                    st.info("Creator details and other models will appear here")
            
            with tab15:  # Download Queue (CivitAI specific)
                st.markdown("#### CivitAI Download Queue")
                if st.session_state.download_queue:
                    for item in st.session_state.download_queue:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.write(f"📎 {item.get('name', 'Unknown')}")
                        with col2:
                            if st.button("Remove", key=f"rm_{item.get('name', '')}"):
                                st.session_state.download_queue.remove(item)
                                st.rerun()
                else:
                    st.info("No items in CivitAI queue")
        
        with tab10:  # HF search
            st.markdown("#### 🤗 HuggingFace Search")
            hf_query = st.text_input("Search HuggingFace", placeholder="stabilityai/stable-diffusion...")
            if st.button("Search HF"):
                st.session_state.output_log.append(f"Searching HF: {hf_query}")
                st.rerun()
        
        with tab11:  # Browse local PC
            st.markdown("#### 💻 Browse Local PC")
            st.info("This browses YOUR computer, not the Colab/cloud instance")
            
            uploaded = st.file_uploader(
                "Select models from your computer",
                type=['safetensors', 'ckpt', 'pt', 'bin'],
                accept_multiple_files=True
            )
            
            if uploaded:
                for file in uploaded:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"📎 {file.name} ({file.size / 1024 / 1024:.1f} MB)")
                    with col2:
                        if st.button(f"Upload", key=f"up_{file.name}"):
                            st.session_state.output_log.append(f"Uploading {file.name}...")
                            st.rerun()
        
        with tab12:  # Main Queue (everything)
            st.markdown("#### 📥 Master Download Queue")
            st.info("All selected models from all sources")
            
            # Summary
            selected_count = len(st.session_state.selected_models)
            queue_count = len(st.session_state.download_queue)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Selected Models", selected_count)
            with col2:
                st.metric("Queued Downloads", queue_count)
            with col3:
                st.metric("Total Items", selected_count + queue_count)
            
            st.markdown("---")
            
            # Selected models
            if st.session_state.selected_models:
                st.markdown("##### Selected Models")
                for model_id in st.session_state.selected_models:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"✅ {model_id}")
                    with col2:
                        if st.button("Remove", key=f"rm_sel_{model_id}"):
                            st.session_state.selected_models.remove(model_id)
                            st.rerun()
            
            # Download queue
            if st.session_state.download_queue:
                st.markdown("##### Queued Downloads")
                for item in st.session_state.download_queue:
                    st.write(f"📥 {item}")

# Download section
st.markdown("---")
col1, col2, col3 = st.columns([2, 6, 2])

with col1:
    total = len(st.session_state.selected_models) + len(st.session_state.download_queue)
    if st.button(f"📥 Download All ({total})", type="primary"):
        if total > 0:
            st.session_state.output_log.append(f"Downloading {total} items...")
        else:
            st.session_state.output_log.append("Nothing to download")
        st.rerun()

with col2:
    st.progress(0)
    st.caption(f"Ready to download {total} items" if total else "Select models to download")

with col3:
    if st.button("🧹 Clear All"):
        st.session_state.selected_models = set()
        st.session_state.download_queue = []
        st.session_state.output_log.append("Cleared all selections")
        st.rerun()

# Output console
st.markdown("---")
st.markdown("#### 📋 Output Console")
output = "\n".join(st.session_state.output_log[-10:]) if st.session_state.output_log else "System ready..."
st.code(output, language='bash')