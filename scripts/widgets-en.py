#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Dashboard - Stable Version with Your Exact Tab Structure
No jumping, consistent layout, comprehensive features
"""

import streamlit as st
import os
import sys
import json
import platform
import subprocess
from datetime import datetime
import time

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try to import model data
try:
    from scripts._models_data import model_list as sd15_models
except ImportError:
    sd15_models = {}
    
try:
    from scripts._xl_models_data import model_list as sdxl_models
except ImportError:
    sdxl_models = {}

# Page config
st.set_page_config(
    page_title="SD-DarkMaster-Pro Dashboard",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the sophisticated dark theme
st.markdown("""
<style>
    /* Dark theme base */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, rgba(139, 0, 0, 0.1) 0%, rgba(0, 0, 0, 0.3) 100%);
        border: 2px solid rgba(139, 0, 0, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Title with star */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    
    /* Info panels */
    .info-panel {
        background: rgba(139, 0, 0, 0.1);
        border: 1px solid rgba(139, 0, 0, 0.3);
        border-radius: 10px;
        padding: 15px;
        height: 100%;
    }
    
    /* Console styling */
    .console-output {
        background: #0a0a0a;
        border: 1px solid #333;
        border-radius: 5px;
        padding: 10px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        color: #0f0;
        height: 150px;
        overflow-y: auto;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(139, 0, 0, 0.05);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #888;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(139, 0, 0, 0.3) !important;
        color: white !important;
        border: 1px solid rgba(139, 0, 0, 0.5);
    }
    
    /* Model button styling */
    .model-button {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        border: 2px solid #333;
        border-radius: 8px;
        padding: 12px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #888;
        text-align: center;
        width: 100%;
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .model-button:hover {
        border-color: rgba(139, 0, 0, 0.5);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(139, 0, 0, 0.3);
    }
    
    .model-button-selected {
        background: linear-gradient(135deg, rgba(139, 0, 0, 0.3) 0%, rgba(139, 0, 0, 0.1) 100%);
        border: 2px solid #8B0000;
        color: white !important;
    }
    
    /* Download button styling */
    .download-button {
        background: linear-gradient(135deg, #8B0000 0%, #660000 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .download-button:hover {
        background: linear-gradient(135deg, #A00000 0%, #8B0000 100%);
        transform: scale(1.05);
    }
    
    /* Queue section */
    .queue-section {
        background: rgba(139, 0, 0, 0.05);
        border: 1px solid rgba(139, 0, 0, 0.2);
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #8B0000, #FF0000);
    }
    
    /* Selections panel */
    .selections-panel {
        background: rgba(139, 0, 0, 0.1);
        border: 1px solid rgba(139, 0, 0, 0.3);
        border-radius: 10px;
        padding: 15px;
        height: 100%;
    }
    
    .selections-panel h4 {
        color: #FFD700;
        margin-bottom: 10px;
    }
    
    .selection-item {
        background: rgba(0, 0, 0, 0.3);
        padding: 5px 10px;
        border-radius: 5px;
        margin: 5px 0;
        color: #888;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = set()
if 'console_output' not in st.session_state:
    st.session_state.console_output = []
if 'download_queue' not in st.session_state:
    st.session_state.download_queue = []
if 'environment_info' not in st.session_state:
    st.session_state.environment_info = {
        'platform': 'Unknown',
        'gpu': False,
        'hardware': 'Unknown'
    }

# Function to detect environment
def detect_environment():
    """Detect the current running environment"""
    env_info = {
        'platform': 'Local',
        'gpu': False,
        'hardware': platform.machine()
    }
    
    # Check for various cloud platforms
    if os.path.exists('/content'):
        env_info['platform'] = 'Google Colab'
    elif os.path.exists('/kaggle'):
        env_info['platform'] = 'Kaggle'
    elif 'PAPERSPACE' in os.environ:
        env_info['platform'] = 'Paperspace'
    elif 'RUNPOD' in os.environ:
        env_info['platform'] = 'Runpod'
    elif 'VAST' in os.environ:
        env_info['platform'] = 'Vast.ai'
    
    # Check for GPU
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            env_info['gpu'] = True
    except:
        pass
    
    return env_info

# Update environment info
if st.session_state.environment_info['platform'] == 'Unknown':
    st.session_state.environment_info = detect_environment()

# Add to console
def add_console_output(message):
    """Add message to console output"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.console_output.append(f"[{timestamp}] {message}")
    # Keep only last 100 messages
    if len(st.session_state.console_output) > 100:
        st.session_state.console_output = st.session_state.console_output[-100:]

# Toggle model selection
def toggle_model(model_id):
    """Toggle model selection"""
    if model_id in st.session_state.selected_models:
        st.session_state.selected_models.remove(model_id)
        add_console_output(f"Deselected: {model_id}")
    else:
        st.session_state.selected_models.add(model_id)
        add_console_output(f"Selected: {model_id}")

# Main header
st.markdown('<h1 class="main-title">⭐ SD-DarkMaster-Pro Dashboard</h1>', unsafe_allow_html=True)

# Header section with controls
header_col1, header_col2, header_col3 = st.columns([1, 3, 1])

with header_col1:
    st.markdown('<div class="info-panel">', unsafe_allow_html=True)
    st.markdown("### Environment Info")
    st.write(f"**Platform:** {st.session_state.environment_info['platform']}")
    st.write(f"**Hardware:** {st.session_state.environment_info['hardware']}")
    st.write(f"**GPU:** {'✅ Yes' if st.session_state.environment_info['gpu'] else '❌ No'}")
    st.markdown('</div>', unsafe_allow_html=True)

with header_col2:
    # WebUI selector and Launch button row
    selector_col, launch_col = st.columns([2, 1])
    
    with selector_col:
        webui_choice = st.selectbox(
            "WebUI Selector",
            ["Automatic1111", "ComfyUI", "Forge", "ReForge"],
            key="webui_selector"
        )
    
    with launch_col:
        if st.button("🚀 Launch WebUI", key="launch_webui", use_container_width=True, type="primary"):
            add_console_output(f"Launching {webui_choice}...")
            st.balloons()
    
    # Console output
    st.markdown("### Output Console")
    console_placeholder = st.empty()
    with console_placeholder.container():
        console_text = "\n".join(st.session_state.console_output[-10:]) if st.session_state.console_output else "System ready..."
        st.code(console_text, language="bash")

with header_col3:
    st.markdown('<div class="selections-panel">', unsafe_allow_html=True)
    st.markdown("### Selections")
    st.markdown("**Pre-installed:** 5")
    st.markdown("**CivitAI:** " + str(len(st.session_state.selected_models)))
    st.markdown("**Queue:** " + str(len(st.session_state.download_queue)))
    st.markdown('</div>', unsafe_allow_html=True)

# Main content tabs
tab_models, tab_browser, tab_settings = st.tabs(["📦 Models", "🔍 Model Search", "⚙️ Settings"])

with tab_models:
    # Model type tabs (using the names you specified)
    model_tabs = st.tabs(["SD1.5", "SDXL", "Pony", "Illustrious", "Misc"])
    
    # SD1.5 Tab
    with model_tabs[0]:
        sd15_subtabs = st.tabs(["Models", "LoRAs", "VAE", "ControlNet"])
        
        with sd15_subtabs[0]:  # Models
            st.markdown("### SD 1.5 Models")
            
            # Create model grid
            cols = st.columns(3)
            for idx, (model_name, model_info) in enumerate(list(sd15_models.items())[:9]):
                with cols[idx % 3]:
                    model_id = f"sd15_{model_name}"
                    is_selected = model_id in st.session_state.selected_models
                    
                    # Create custom button with HTML
                    button_class = "model-button-selected" if is_selected else "model-button"
                    st.markdown(f"""
                        <div class="{button_class}" onclick="console.log('clicked')">
                            {model_name[:30]}...
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Actual button (invisible)
                    if st.button("", key=f"btn_{model_id}", use_container_width=True):
                        toggle_model(model_id)
                        st.rerun()
        
        with sd15_subtabs[1]:  # LoRAs
            st.info("SD 1.5 LoRAs will be displayed here")
        
        with sd15_subtabs[2]:  # VAE
            st.info("SD 1.5 VAEs will be displayed here")
        
        with sd15_subtabs[3]:  # ControlNet
            st.info("SD 1.5 ControlNet models will be displayed here")
    
    # SDXL Tab
    with model_tabs[1]:
        sdxl_subtabs = st.tabs(["Models", "LoRAs", "VAE", "ControlNet"])
        
        with sdxl_subtabs[0]:  # Models
            st.markdown("### SDXL Models")
            
            # Create model grid
            cols = st.columns(3)
            for idx, (model_name, model_info) in enumerate(list(sdxl_models.items())[:9]):
                with cols[idx % 3]:
                    model_id = f"sdxl_{model_name}"
                    is_selected = model_id in st.session_state.selected_models
                    
                    # Create custom button with HTML
                    button_class = "model-button-selected" if is_selected else "model-button"
                    st.markdown(f"""
                        <div class="{button_class}">
                            {model_name[:30]}...
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Actual button (invisible)
                    if st.button("", key=f"btn_{model_id}", use_container_width=True):
                        toggle_model(model_id)
                        st.rerun()
        
        with sdxl_subtabs[1]:  # LoRAs
            st.info("SDXL LoRAs will be displayed here")
        
        with sdxl_subtabs[2]:  # VAE
            st.info("SDXL VAEs will be displayed here")
        
        with sdxl_subtabs[3]:  # ControlNet
            st.info("SDXL ControlNet models will be displayed here")
    
    # Pony Tab
    with model_tabs[2]:
        pony_subtabs = st.tabs(["Models", "LoRAs", "VAE"])
        
        with pony_subtabs[0]:
            st.info("Pony models will be displayed here")
        
        with pony_subtabs[1]:
            st.info("Pony LoRAs will be displayed here")
        
        with pony_subtabs[2]:
            st.info("Pony VAEs will be displayed here")
    
    # Illustrious Tab
    with model_tabs[3]:
        illustrious_subtabs = st.tabs(["Models", "LoRAs", "VAE"])
        
        with illustrious_subtabs[0]:
            st.info("Illustrious models will be displayed here")
        
        with illustrious_subtabs[1]:
            st.info("Illustrious LoRAs will be displayed here")
        
        with illustrious_subtabs[2]:
            st.info("Illustrious VAEs will be displayed here")
    
    # Misc Tab
    with model_tabs[4]:
        misc_tabs = st.tabs(["SAM", "ADetailer", "Upscaler", "Reactor", "Other Extensions"])
        
        with misc_tabs[0]:
            st.info("SAM models will be displayed here")
        
        with misc_tabs[1]:
            st.info("ADetailer models will be displayed here")
        
        with misc_tabs[2]:
            st.info("Upscaler models will be displayed here")
        
        with misc_tabs[3]:
            st.info("Reactor models will be displayed here")
        
        with misc_tabs[4]:
            st.info("Other extension models will be displayed here")

with tab_browser:
    st.markdown("### 🔍 CivitAI Model Browser")
    
    # Search bar
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_query = st.text_input("Search models...", placeholder="Enter model name or tag")
    with search_col2:
        search_button = st.button("Search", use_container_width=True, type="primary")
    
    # Filters
    filter_cols = st.columns(4)
    with filter_cols[0]:
        model_type = st.selectbox("Type", ["All", "Checkpoint", "LoRA", "VAE", "ControlNet"])
    with filter_cols[1]:
        base_model = st.selectbox("Base Model", ["All", "SD 1.5", "SDXL", "Pony", "Illustrious"])
    with filter_cols[2]:
        sort_by = st.selectbox("Sort By", ["Most Downloaded", "Highest Rated", "Newest"])
    with filter_cols[3]:
        nsfw_filter = st.checkbox("Include NSFW", value=False)
    
    # Results area
    st.markdown("### Search Results")
    st.info("Enter a search query to find models on CivitAI")

with tab_settings:
    st.markdown("### ⚙️ Settings")
    
    settings_tabs = st.tabs(["Paths", "Download", "Advanced", "About"])
    
    with settings_tabs[0]:
        st.markdown("### Storage Paths")
        st.text_input("Models Path", value="/storage/models", key="models_path")
        st.text_input("LoRA Path", value="/storage/loras", key="lora_path")
        st.text_input("VAE Path", value="/storage/vae", key="vae_path")
        st.text_input("ControlNet Path", value="/storage/controlnet", key="controlnet_path")
    
    with settings_tabs[1]:
        st.markdown("### Download Settings")
        st.slider("Parallel Downloads", 1, 16, 4, key="parallel_downloads")
        st.checkbox("Use Aria2c", value=True, key="use_aria2c")
        st.checkbox("Auto-extract ZIP files", value=True, key="auto_extract")
    
    with settings_tabs[2]:
        st.markdown("### Advanced Settings")
        st.checkbox("Enable Debug Mode", value=False, key="debug_mode")
        st.checkbox("Auto-detect Extensions", value=True, key="auto_detect")
        st.number_input("Cache Size (GB)", min_value=1, max_value=100, value=10, key="cache_size")
    
    with settings_tabs[3]:
        st.markdown("### About SD-DarkMaster-Pro")
        st.info("""
        **Version:** 2.0.0  
        **Author:** DarkMaster  
        **License:** MIT  
        
        SD-DarkMaster-Pro is an advanced Stable Diffusion WebUI manager with integrated model management,
        CivitAI browser, and multi-platform support.
        """)

# Download Queue Section (Bottom)
st.markdown("---")
st.markdown("### 📥 Download Queue")

queue_col1, queue_col2 = st.columns([4, 1])

with queue_col1:
    if st.session_state.selected_models:
        # Show progress bar
        progress = st.progress(0, text="Ready to download...")
        
        # Show selected models
        st.markdown(f"**Selected Models:** {len(st.session_state.selected_models)}")
        
        # Sample queue display
        with st.expander("View Queue", expanded=False):
            for model in list(st.session_state.selected_models)[:5]:
                st.markdown(f"- {model}")
    else:
        st.info("No models selected for download")

with queue_col2:
    if st.button("⬇️ Download All", key="download_all", use_container_width=True, type="primary", 
                 disabled=len(st.session_state.selected_models) == 0):
        add_console_output(f"Starting download of {len(st.session_state.selected_models)} models...")
        with st.spinner("Downloading..."):
            time.sleep(2)  # Simulate download
        st.success("Download started!")

# Add initialization message
if len(st.session_state.console_output) == 0:
    add_console_output("SD-DarkMaster-Pro initialized successfully")
    add_console_output(f"Platform detected: {st.session_state.environment_info['platform']}")
    add_console_output("Ready for model selection...")