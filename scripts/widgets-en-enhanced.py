#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Dashboard - Enhanced with Custom Components
Using streamlit-option-menu, streamlit-card, streamlit-extras for better UI
"""

import streamlit as st
import sys
from pathlib import Path
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

# Try to import custom components (will gracefully fallback if not installed)
try:
    from streamlit_option_menu import option_menu
    HAS_OPTION_MENU = True
except:
    HAS_OPTION_MENU = False
    
try:
    from streamlit_card import card
    HAS_CARD = True
except:
    HAS_CARD = False

try:
    from streamlit_extras.colored_header import colored_header
    from streamlit_extras.add_vertical_space import add_vertical_space
    from streamlit_extras.metric_cards import style_metric_cards
    from streamlit_extras.badges import badge
    HAS_EXTRAS = True
except:
    HAS_EXTRAS = False

try:
    import streamlit_antd_components as sac
    HAS_ANTD = True
except:
    HAS_ANTD = False

# Page config
st.set_page_config(
    page_title="SD-DarkMaster-Pro",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Dark Theme CSS
st.markdown("""
<style>
/* Dark theme base */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
}

.main .block-container {
    padding-top: 2rem;
    max-width: 100%;
}

/* Enhanced model cards */
.model-card {
    background: rgba(26, 26, 46, 0.8);
    border: 1px solid rgba(16, 185, 129, 0.3);
    border-radius: 12px;
    padding: 12px;
    margin: 8px 4px;
    backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.model-card:hover {
    transform: translateY(-2px);
    border-color: #10B981;
    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.2);
}

.model-card.selected {
    background: rgba(16, 185, 129, 0.2);
    border-color: #10B981;
}

/* Glassmorphism effect */
.glass-panel {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 20px;
    margin: 10px 0;
}

/* Animated gradient border */
.gradient-border {
    position: relative;
    background: linear-gradient(90deg, #10B981, #3B82F6, #8B5CF6);
    padding: 2px;
    border-radius: 12px;
}

.gradient-border::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 12px;
    background: linear-gradient(90deg, #10B981, #3B82F6, #8B5CF6);
    animation: gradient-animation 3s ease infinite;
}

@keyframes gradient-animation {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Enhanced toggles */
.stToggle > label {
    background: rgba(26, 26, 46, 0.9) !important;
    border: 1px solid rgba(42, 42, 62, 0.8) !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}

.stToggle > label:hover {
    background: rgba(42, 42, 62, 0.9) !important;
    border-color: #10B981 !important;
}

/* Progress indicator */
.progress-ring {
    animation: spin 2s linear infinite;
}

@keyframes spin {
    100% { transform: rotate(360deg); }
}

/* Smooth transitions */
* {
    transition: color 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.viewerBadge_container__1QSob {display: none;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = set()
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Models"
if 'output_log' not in st.session_state:
    st.session_state.output_log = []

# Enhanced Header with gradient
if HAS_EXTRAS:
    colored_header(
        label="🌟 SD-DarkMaster-Pro Dashboard",
        description="Unified Model Management System",
        color_name="green-70"
    )
else:
    st.title("🌟 SD-DarkMaster-Pro Dashboard")
    st.caption("Unified Model Management System")

# Enhanced navigation with option menu
if HAS_OPTION_MENU:
    selected = option_menu(
        menu_title=None,
        options=["Models", "Model Browser", "Settings", "Extensions"],
        icons=["collection", "search", "gear", "puzzle"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#10B981", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "background-color": "rgba(26, 26, 46, 0.8)",
                "border-radius": "10px",
            },
            "nav-link-selected": {"background-color": "#10B981"},
        }
    )
    st.session_state.current_tab = selected
else:
    # Fallback to regular tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Models", "Model Browser", "Settings", "Extensions"])
    selected = "Models"

# Use Ant Design components if available
if HAS_ANTD and selected == "Models":
    # Create segmented control for model types
    model_type = sac.segmented(
        items=[
            sac.SegmentedItem(label='SD-1.5', icon='image'),
            sac.SegmentedItem(label='SDXL', icon='rocket'),
            sac.SegmentedItem(label='PONY', icon='star'),
            sac.SegmentedItem(label='Illustrous', icon='palette'),
            sac.SegmentedItem(label='Misc', icon='grid'),
        ],
        label='Model Type',
        align='center',
        size='lg',
        color='green'
    )
    
    # Create tabs for sub-categories
    sub_category = sac.tabs([
        sac.TabsItem(label='Models', icon='collection'),
        sac.TabsItem(label='Loras', icon='layers'),
        sac.TabsItem(label='Vae', icon='box'),
        sac.TabsItem(label='Controlnet', icon='sliders'),
    ], align='center', size='md')

# Main content area
if selected == "Models" or (not HAS_OPTION_MENU and tab1):
    
    # If we don't have Ant Design, use regular tabs
    if not HAS_ANTD:
        model_tabs = st.tabs(["SD-1.5", "SDXL", "🦄 PONY", "Illustrous", "Misc"])
        
        with model_tabs[0]:
            sub_tabs = st.tabs(["Models", "Loras", "Vae", "Controlnet"])
            
            with sub_tabs[0]:
                st.markdown("#### SD 1.5 Checkpoints")
                
                if sd15_models:
                    # Use cards if available
                    if HAS_CARD:
                        cols = st.columns(3)
                        for idx, (name, info) in enumerate(list(sd15_models.items())[:9]):
                            with cols[idx % 3]:
                                hasClicked = card(
                                    title=name[:30],
                                    text=info.get('size', 'Unknown'),
                                    key=f"card_sd15_{name}",
                                    on_click=lambda: st.session_state.selected_models.add(name)
                                )
                                if hasClicked:
                                    st.session_state.selected_models.add(name)
                    else:
                        # Fallback to toggles with enhanced styling
                        cols = st.columns(2)
                        for idx, (name, info) in enumerate(sd15_models.items()):
                            with cols[idx % 2]:
                                # Create glass panel effect
                                st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
                                
                                col1, col2 = st.columns([4, 1])
                                with col1:
                                    selected = st.toggle(name[:40], key=f"sd15_{name}")
                                    if selected:
                                        st.session_state.selected_models.add(f"sd15/{name}")
                                    else:
                                        st.session_state.selected_models.discard(f"sd15/{name}")
                                    
                                    # Add badge if available
                                    if HAS_EXTRAS:
                                        badge(info.get('size', 'Unknown'), "secondary")
                                    else:
                                        st.caption(info.get('size', 'Unknown'))
                                
                                with col2:
                                    if f"sd15/{name}" not in st.session_state.selected_models:
                                        st.markdown("⬇️")
                                    else:
                                        st.markdown("✅")
                                
                                st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Model Browser" or (not HAS_OPTION_MENU and tab2):
    st.markdown("#### 🔍 CivitAI Browser")
    
    # Enhanced search with Ant Design if available
    if HAS_ANTD:
        col1, col2 = st.columns([3, 1])
        with col1:
            search = sac.input('Search models', placeholder='anime, realistic, etc.', size='lg')
        with col2:
            model_type = sac.select(
                'Type',
                items=['All', 'Checkpoint', 'LORA', 'VAE'],
                size='lg'
            )
        
        if sac.buttons(['Search', 'Trending', 'Latest'], align='center', size='lg', color='green'):
            st.session_state.output_log.append(f"Searching: {search}")
    else:
        # Regular search interface
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            search = st.text_input("Search", placeholder="Search CivitAI...")
        with col2:
            model_type = st.selectbox("Type", ["All", "Checkpoint", "LORA", "VAE"])
        with col3:
            if st.button("🔍 Search"):
                st.session_state.output_log.append(f"Searching: {search}")

elif selected == "Settings" or (not HAS_OPTION_MENU and tab3):
    st.markdown("#### ⚙️ Settings")
    
    if HAS_ANTD:
        # Use Ant Design components for settings
        col1, col2 = st.columns(2)
        
        with col1:
            webui = sac.radio(
                'WebUI Type',
                items=['Forge', 'ComfyUI', 'A1111'],
                direction='horizontal',
                size='lg'
            )
            
            port = sac.number('Port', min=1000, max=65535, value=7860, step=1)
        
        with col2:
            sac.switch('Enable API', value=False, size='lg')
            sac.switch('Auto-launch', value=True, size='lg')
            sac.switch('Share', value=False, size='lg')
    else:
        # Regular settings
        col1, col2 = st.columns(2)
        with col1:
            webui = st.selectbox("WebUI Type", ["Forge", "ComfyUI", "A1111"])
            port = st.number_input("Port", value=7860)
        with col2:
            st.toggle("Enable API", value=False)
            st.toggle("Auto-launch", value=True)
            st.toggle("Share", value=False)

elif selected == "Extensions" or (not HAS_OPTION_MENU and tab4):
    st.markdown("#### 🧩 Extension Models")
    
    ext_tabs = st.tabs(["SAM", "ADetailer", "Upscaler", "Reactor", "Future"])
    
    with ext_tabs[0]:
        if MODEL_REGISTRY.get('sam'):
            for name, info in MODEL_REGISTRY['sam'].items():
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.toggle(name, key=f"sam_{name}")
                with col2:
                    st.caption(info.get('size', ''))

# Enhanced metrics display
if HAS_EXTRAS:
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Selected Models", len(st.session_state.selected_models))
    with col2:
        st.metric("Total Available", len(sd15_models) + len(sdxl_models))
    with col3:
        st.metric("Storage Used", "0 GB")
    with col4:
        st.metric("Downloads", "0")
    
    style_metric_cards()

# Download section with animation
st.markdown("---")
col1, col2 = st.columns([1, 10])

with col1:
    count = len(st.session_state.selected_models)
    
    if HAS_ANTD:
        if sac.buttons([f'📥 Download ({count})'], size='lg', color='green'):
            if count > 0:
                st.session_state.output_log.append(f"Downloading {count} models...")
            else:
                st.session_state.output_log.append("No models selected")
    else:
        if st.button(f"📥 Download ({count})"):
            if count > 0:
                st.session_state.output_log.append(f"Downloading {count} models...")

with col2:
    # Animated progress bar
    progress = st.progress(0)
    if count > 0:
        st.markdown('<div class="progress-ring">⚙️ Ready to download...</div>', unsafe_allow_html=True)

# Enhanced output console
st.markdown("---")
st.markdown("#### 📋 Output Console")

# Glass panel effect for output
st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
output_text = "\n".join(st.session_state.output_log[-10:]) if st.session_state.output_log else "System ready..."
st.code(output_text, language='bash')
st.markdown('</div>', unsafe_allow_html=True)

# Quick actions with enhanced buttons
if HAS_ANTD:
    actions = sac.buttons([
        sac.ButtonsItem(label='Launch WebUI', icon='rocket'),
        sac.ButtonsItem(label='Refresh', icon='arrow-clockwise'),
        sac.ButtonsItem(label='Clear Output', icon='trash'),
        sac.ButtonsItem(label='System Info', icon='info-circle'),
    ], align='center', size='md', color='green')
else:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🚀 Launch"):
            st.session_state.output_log.append("Launching WebUI...")
    with col2:
        if st.button("🔄 Refresh"):
            st.rerun()
    with col3:
        if st.button("🧹 Clear"):
            st.session_state.output_log = []
    with col4:
        if st.button("📊 Info"):
            st.session_state.output_log.append("System info...")