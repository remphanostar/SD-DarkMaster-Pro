#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Dashboard - Final Design with Verbose Model Info
Consistent layout with comprehensive CivitAI data display
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

# Enhanced CSS for consistent layout
st.markdown("""
<style>
/* Dark theme */
.stApp {
    background: #0e0e0e;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Consistent tab heights */
.stTabs {
    min-height: 50px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background-color: transparent;
    align-items: stretch;
}

.stTabs [data-baseweb="tab"] {
    background-color: #1a1a1a;
    border-radius: 8px 8px 0 0;
    color: #ffffff;
    border: 1px solid #2a2a2a;
    padding: 8px 16px;
    min-height: 40px;
    display: flex;
    align-items: center;
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

/* Info cards */
.info-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}

.info-card h4 {
    color: #ef4444;
    margin-bottom: 8px;
}

/* Model preview grid */
.preview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
    margin: 16px 0;
}

.preview-item {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s;
}

.preview-item:hover {
    transform: scale(1.05);
    border-color: #ef4444;
}

/* Tags */
.tag {
    display: inline-block;
    background: #2a2a2a;
    color: #ffffff;
    padding: 4px 12px;
    border-radius: 16px;
    margin: 4px;
    font-size: 12px;
}

.tag:hover {
    background: #ef4444;
}

/* Stats grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
    margin: 16px 0;
}

.stat-item {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
}

.stat-value {
    font-size: 24px;
    font-weight: bold;
    color: #ef4444;
}

.stat-label {
    font-size: 12px;
    color: #888;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = set()
if 'output_log' not in st.session_state:
    st.session_state.output_log = []
if 'civitai_cache' not in st.session_state:
    st.session_state.civitai_cache = {}
if 'download_queue' not in st.session_state:
    st.session_state.download_queue = []
if 'current_model_data' not in st.session_state:
    st.session_state.current_model_data = None

def fetch_civitai_model_details(model_id):
    """Fetch comprehensive model details from CivitAI API"""
    try:
        # Check cache first
        if model_id in st.session_state.civitai_cache:
            return st.session_state.civitai_cache[model_id]
        
        # Fetch from API
        response = requests.get(f"https://civitai.com/api/v1/models/{model_id}")
        if response.status_code == 200:
            data = response.json()
            st.session_state.civitai_cache[model_id] = data
            return data
    except Exception as e:
        st.error(f"Error fetching model details: {e}")
    return None

def render_model_button(name, model_id, size="Unknown"):
    """Render a model selection button with persistent state"""
    is_selected = model_id in st.session_state.selected_models
    button_class = "model-button-selected" if is_selected else "model-button"
    
    st.markdown(f"""
    <div class="{button_class}">
        {name[:40]} ({size})
    </div>
    """, unsafe_allow_html=True)
    
    # Use empty label to make button invisible but clickable
    if st.button("", key=f"btn_{model_id}", use_container_width=True):
        if model_id in st.session_state.selected_models:
            st.session_state.selected_models.remove(model_id)
            st.session_state.output_log.append(f"[-] Deselected: {name}")
        else:
            st.session_state.selected_models.add(model_id)
            st.session_state.output_log.append(f"[+] Selected: {name}")
        st.rerun()

def render_verbose_model_info(model_data):
    """Render EVERYTHING from CivitAI API"""
    if not model_data:
        st.info("Select a model to view detailed information")
        return
    
    # Model header with stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Downloads", f"{model_data.get('stats', {}).get('downloadCount', 0):,}")
    with col2:
        st.metric("Likes", f"{model_data.get('stats', {}).get('favoriteCount', 0):,}")
    with col3:
        st.metric("Rating", f"{model_data.get('stats', {}).get('rating', 0):.2f}⭐")
    with col4:
        st.metric("Reviews", model_data.get('stats', {}).get('commentCount', 0))
    
    st.markdown("---")
    
    # Main info columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Description
        st.markdown("### 📝 Description")
        st.markdown(model_data.get('description', 'No description available'))
        
        # Tags
        if model_data.get('tags'):
            st.markdown("### 🏷️ Tags")
            tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in model_data.get('tags', [])])
            st.markdown(tags_html, unsafe_allow_html=True)
        
        # Model Versions
        st.markdown("### 📦 Versions")
        for version in model_data.get('modelVersions', [])[:5]:
            with st.expander(f"v{version.get('name', 'Unknown')} - {version.get('baseModel', 'Unknown')}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**Created:** {version.get('createdAt', 'Unknown')[:10]}")
                    st.write(f"**Downloads:** {version.get('stats', {}).get('downloadCount', 0):,}")
                    st.write(f"**Base Model:** {version.get('baseModel', 'Unknown')}")
                with col_b:
                    st.write(f"**Size:** {version.get('files', [{}])[0].get('sizeKB', 0) / 1024:.1f} MB")
                    st.write(f"**Format:** {version.get('files', [{}])[0].get('format', 'Unknown')}")
                    st.write(f"**FP:** {version.get('files', [{}])[0].get('fp', 'Unknown')}")
                
                # Training details
                if version.get('trainedWords'):
                    st.write(f"**Trigger Words:** {', '.join(version.get('trainedWords', []))}")
                
                # Download files
                st.markdown("**Files:**")
                for file in version.get('files', []):
                    file_info = f"📎 {file.get('name', 'Unknown')} ({file.get('sizeKB', 0) / 1024:.1f} MB)"
                    if st.button(f"Add to Queue: {file_info}", key=f"dl_{file.get('id')}"):
                        st.session_state.download_queue.append({
                            'name': file.get('name'),
                            'url': file.get('downloadUrl'),
                            'size': file.get('sizeKB', 0) / 1024
                        })
                        st.success(f"Added to download queue!")
    
    with col2:
        # Creator info
        st.markdown("### 👤 Creator")
        creator = model_data.get('creator', {})
        if creator.get('image'):
            st.image(creator.get('image'), width=100)
        st.write(f"**Username:** {creator.get('username', 'Unknown')}")
        
        # Model metadata
        st.markdown("### 🔧 Metadata")
        st.write(f"**Type:** {model_data.get('type', 'Unknown')}")
        st.write(f"**NSFW:** {'🔞 Yes' if model_data.get('nsfw') else '✅ No'}")
        st.write(f"**POI:** {'⚠️ Yes' if model_data.get('poi') else '✅ No'}")
        st.write(f"**Allow Commercial:** {'✅' if model_data.get('allowCommercialUse') else '❌'}")
        st.write(f"**Allow Derivatives:** {'✅' if model_data.get('allowDerivatives') else '❌'}")
        
        # Stats breakdown
        st.markdown("### 📊 Detailed Stats")
        stats = model_data.get('stats', {})
        for key, value in stats.items():
            if isinstance(value, (int, float)):
                st.write(f"**{key}:** {value:,}")
    
    # Sample images with prompts
    st.markdown("---")
    st.markdown("### 🖼️ Sample Images & Prompts")
    
    versions = model_data.get('modelVersions', [])
    if versions and versions[0].get('images'):
        images = versions[0].get('images', [])[:6]
        
        cols = st.columns(3)
        for idx, img in enumerate(images):
            with cols[idx % 3]:
                if img.get('url'):
                    st.image(img.get('url'), use_column_width=True)
                    
                    # Image metadata
                    with st.expander("Prompt & Settings"):
                        meta = img.get('meta', {})
                        if meta.get('prompt'):
                            st.text_area("Prompt", meta.get('prompt'), height=100, key=f"prompt_{idx}")
                        if meta.get('negativePrompt'):
                            st.text_area("Negative", meta.get('negativePrompt'), height=50, key=f"neg_{idx}")
                        
                        # Generation settings
                        col_s1, col_s2 = st.columns(2)
                        with col_s1:
                            st.write(f"**Steps:** {meta.get('steps', 'N/A')}")
                            st.write(f"**Sampler:** {meta.get('sampler', 'N/A')}")
                            st.write(f"**CFG:** {meta.get('cfgScale', 'N/A')}")
                        with col_s2:
                            st.write(f"**Seed:** {meta.get('seed', 'N/A')}")
                            st.write(f"**Size:** {meta.get('Size', 'N/A')}")
                            st.write(f"**Model:** {meta.get('Model', 'N/A')}")

# Title
st.title("🌟 SD-DarkMaster-Pro Dashboard")
st.caption("Unified Model Management System")

# Main structure matching your code
col1 = st.columns([1])[0]

with col1:
    main_tabs = st.tabs(["Models", "Model Search"])
    
    with main_tabs[0]:  # Models tab
        model_type_tabs = st.tabs(["SD-1.5", "SDXL", "PONY", "Illustrous", "Misc"])
        
        with model_type_tabs[0]:  # SD-1.5
            sub_tabs = st.tabs(["Models", "Loras", "Vae"])
            
            with sub_tabs[0]:  # Models
                st.markdown("#### SD 1.5 Checkpoints")
                if sd15_models:
                    cols = st.columns(2)
                    for idx, (name, info) in enumerate(list(sd15_models.items())):
                        with cols[idx % 2]:
                            render_model_button(name, f"sd15_{name}", info.get('size', 'Unknown'))
                else:
                    st.info("No SD 1.5 models available")
            
            with sub_tabs[1]:  # Loras
                st.info("SD 1.5 LoRAs will appear here")
            
            with sub_tabs[2]:  # Vae
                st.info("SD 1.5 VAE models will appear here")
        
        with model_type_tabs[1]:  # SDXL
            sub_tabs = st.tabs(["Models", "Loras", "Vae"])
            
            with sub_tabs[0]:
                st.markdown("#### SDXL Checkpoints")
                if sdxl_models:
                    sdxl_filtered = [(k, v) for k, v in sdxl_models.items() 
                                   if 'pony' not in k.lower() and 'illustrious' not in k.lower()]
                    cols = st.columns(2)
                    for idx, (name, info) in enumerate(sdxl_filtered):
                        with cols[idx % 2]:
                            render_model_button(name, f"sdxl_{name}", info.get('size', 'Unknown'))
        
        with model_type_tabs[2]:  # PONY
            st.markdown("#### Pony Models")
            if sdxl_models:
                pony_models = [(k, v) for k, v in sdxl_models.items() if 'pony' in k.lower()]
                if pony_models:
                    cols = st.columns(2)
                    for idx, (name, info) in enumerate(pony_models):
                        with cols[idx % 2]:
                            render_model_button(name, f"pony_{name}", info.get('size', 'Unknown'))
    
    with main_tabs[1]:  # Model Search tab
        search_tabs = st.tabs([
            "CivitAI Search", 
            "HuggingFace Search", 
            "Browse Local PC", 
            "Recent Downloads"
        ])
        
        with search_tabs[0]:  # CivitAI Search
            # Sub-tabs for different views
            civitai_tabs = st.tabs([
                "Basic View + Preview", 
                "📊 Verbose (Every Detail)", 
                "📥 Download Queue"
            ])
            
            with civitai_tabs[0]:  # Basic View
                st.markdown("#### 🔍 CivitAI Model Search")
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    search_query = st.text_input("Search", placeholder="anime, realistic, landscape...")
                with col2:
                    search_type = st.selectbox("Type", ["All", "Checkpoint", "LORA", "TextualInversion", "VAE"])
                with col3:
                    if st.button("🔍 Search", use_container_width=True):
                        st.session_state.output_log.append(f"Searching CivitAI: {search_query}")
                        # Here you would implement actual search
                
                # Results area
                st.markdown("---")
                st.info("Search results will appear here with preview images")
            
            with civitai_tabs[1]:  # Verbose View
                st.markdown("#### 📊 Comprehensive Model Information")
                
                # Model selector
                model_id = st.text_input("Enter CivitAI Model ID", placeholder="e.g., 4384")
                if st.button("Load Model Details"):
                    with st.spinner("Fetching comprehensive data..."):
                        model_data = fetch_civitai_model_details(model_id)
                        if model_data:
                            st.session_state.current_model_data = model_data
                            st.success(f"Loaded: {model_data.get('name', 'Unknown')}")
                
                # Display verbose info
                if st.session_state.current_model_data:
                    render_verbose_model_info(st.session_state.current_model_data)
            
            with civitai_tabs[2]:  # Download Queue
                st.markdown("#### 📥 Download Queue")
                
                if st.session_state.download_queue:
                    total_size = sum(item['size'] for item in st.session_state.download_queue)
                    st.info(f"**Queue:** {len(st.session_state.download_queue)} files | **Total Size:** {total_size:.1f} MB")
                    
                    for idx, item in enumerate(st.session_state.download_queue):
                        col1, col2, col3 = st.columns([4, 1, 1])
                        with col1:
                            st.write(f"📎 {item['name']}")
                        with col2:
                            st.write(f"{item['size']:.1f} MB")
                        with col3:
                            if st.button("Remove", key=f"rm_{idx}"):
                                st.session_state.download_queue.pop(idx)
                                st.rerun()
                    
                    st.markdown("---")
                    if st.button("🚀 Start Download All", use_container_width=True, type="primary"):
                        st.session_state.output_log.append(f"Starting download of {len(st.session_state.download_queue)} files...")
                        # Implement actual download here
                else:
                    st.info("Download queue is empty. Add models from the verbose view.")
        
        with search_tabs[1]:  # HuggingFace
            st.markdown("#### 🤗 HuggingFace Model Search")
            hf_search = st.text_input("Search HuggingFace", placeholder="stabilityai/stable-diffusion...")
            if st.button("Search HF", use_container_width=True):
                st.session_state.output_log.append(f"Searching HuggingFace: {hf_search}")
        
        with search_tabs[2]:  # Browse Local PC
            st.markdown("#### 💻 Browse Local PC Files")
            st.info("This will browse your LOCAL computer, not the Colab/cloud instance")
            
            # File uploader for local files
            uploaded_file = st.file_uploader(
                "Select model from your computer",
                type=['safetensors', 'ckpt', 'pt', 'bin'],
                accept_multiple_files=True
            )
            
            if uploaded_file:
                for file in uploaded_file:
                    st.write(f"📎 {file.name} ({file.size / 1024 / 1024:.1f} MB)")
                    if st.button(f"Upload {file.name}", key=f"up_{file.name}"):
                        st.session_state.output_log.append(f"Uploading: {file.name}")
        
        with search_tabs[3]:  # Recent Downloads
            st.markdown("#### 🕐 Recent Downloads")
            st.info("Recently downloaded models will appear here")

# Download section
st.markdown("---")
col1, col2, col3 = st.columns([2, 6, 2])

with col1:
    count = len(st.session_state.selected_models)
    queue_count = len(st.session_state.download_queue)
    if st.button(f"📥 Download ({count} + {queue_count} queued)", use_container_width=True, type="primary"):
        if count > 0 or queue_count > 0:
            st.session_state.output_log.append(f"Downloading {count} selected + {queue_count} queued models...")
        else:
            st.session_state.output_log.append("Nothing to download")
        st.rerun()

with col2:
    st.progress(0)
    st.caption(f"Ready: {count} selected, {queue_count} in queue")

with col3:
    if st.button("🧹 Clear All", use_container_width=True):
        st.session_state.selected_models = set()
        st.session_state.download_queue = []
        st.session_state.output_log.append("Cleared all selections")
        st.rerun()

# Output console
st.markdown("---")
st.markdown("#### 📋 Output Console")
output_text = "\n".join(st.session_state.output_log[-10:]) if st.session_state.output_log else "System ready..."
st.code(output_text, language='bash')

# Stats
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Selected", len(st.session_state.selected_models))
with col2:
    st.metric("Queued", len(st.session_state.download_queue))
with col3:
    st.metric("Cached", len(st.session_state.civitai_cache))
with col4:
    st.metric("Storage", "0 GB")