#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Dashboard - Final Nested Tab Design
All models under Models tab, including Misc for extensions
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path('/workspace/SD-DarkMaster-Pro')
sys.path.insert(0, str(project_root))

# Import model dictionaries
from scripts._models_data import model_list as sd15_models
from scripts._xl_models_data import model_list as sdxl_models
from scripts.setup_central_storage import MODEL_REGISTRY

# Configure page
st.set_page_config(
    page_title="SD-DarkMaster-Pro",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Centered Dark Mode Pro CSS
CENTERED_CSS = """
<style>
/* Dark Mode Pro Theme */
:root {
    --darkpro-bg: #0a0a0a;
    --darkpro-surface: #1a1a2e;
    --darkpro-accent: #10B981;
    --darkpro-text: #e0e0e0;
    --darkpro-border: #2a2a3e;
}

/* Center the main content */
.main > div {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
}

/* Dark background */
.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    color: var(--darkpro-text);
}

/* Style tabs */
.stTabs [data-baseweb="tab-list"] {
    justify-content: center;
    gap: 2px;
    background: var(--darkpro-surface);
    border-radius: 10px;
    padding: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--darkpro-text);
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(16, 185, 129, 0.1);
}

.stTabs [aria-selected="true"] {
    background: var(--darkpro-accent) !important;
    color: white !important;
}

/* Center headers */
h1, h2, h3 {
    text-align: center;
    color: var(--darkpro-text);
}

/* Model cards */
.model-card {
    background: var(--darkpro-surface);
    border: 1px solid var(--darkpro-border);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem;
    transition: all 0.3s ease;
}

.model-card:hover {
    border-color: var(--darkpro-accent);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

/* Center content in columns */
.stColumn > div {
    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--darkpro-accent) 0%, #059669 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    margin: 0 auto;
    display: block;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
}

/* Checkboxes */
.stCheckbox {
    display: flex;
    justify-content: center;
}

/* Info boxes */
.stAlert {
    background: var(--darkpro-surface);
    border: 1px solid var(--darkpro-border);
    border-radius: 8px;
}
</style>
"""

# Apply CSS
st.markdown(CENTERED_CSS, unsafe_allow_html=True)

# Title
st.markdown("# 🌟 SD-DarkMaster-Pro Dashboard")
st.markdown("### Unified Model Management System")
st.markdown("---")

# Main tabs
tab1, tab2, tab3 = st.tabs(["Models", "Model Browser", "Settings"])

with tab1:
    # Model type tabs - Added Misc tab
    tab_sd15, tab_sdxl, tab_pony, tab_illustrous, tab_misc = st.tabs([
        "SD-1.5", "SDXL", "PONY", "Illustrous", "Misc"
    ])
    
    # SD-1.5 Section
    with tab_sd15:
        tab_models, tab_loras, tab_vae, tab_controlnet = st.tabs([
            "Models", "Loras", "Vae", "Controlnet"
        ])
        
        with tab_models:
            st.markdown("#### SD 1.5 Checkpoints")
            
            # Filter SD1.5 models
            if sd15_models:
                # Create 3-column grid
                cols = st.columns(3)
                for idx, (name, info) in enumerate(sd15_models.items()):
                    with cols[idx % 3]:
                        with st.container():
                            st.markdown(f"""
                            <div class="model-card">
                                <h5>{name[:30]}...</h5>
                                <p>Size: {info.get('size', 'Unknown')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.checkbox("Select", key=f"sd15_model_{name}")
                            with col2:
                                # Check if downloaded
                                model_path = Path('/workspace/SD-DarkMaster-Pro/storage/models/Stable-diffusion') / name
                                if model_path.exists():
                                    st.success("✅")
                                else:
                                    st.button("⬇️", key=f"dl_sd15_{name}")
            else:
                st.info("No SD 1.5 models found")
        
        with tab_loras:
            st.markdown("#### SD 1.5 LoRAs")
            st.info("Drop SD 1.5 LoRAs here")
        
        with tab_vae:
            st.markdown("#### SD 1.5 VAE")
            st.info("Drop SD 1.5 VAE models here")
        
        with tab_controlnet:
            st.markdown("#### SD 1.5 ControlNet")
            
            # Show ControlNet models for SD1.5
            controlnet_models = MODEL_REGISTRY.get('controlnet', {})
            if controlnet_models:
                for name, info in controlnet_models.items():
                    if 'sd15' in name or 'v11' in name:  # Filter SD1.5 ControlNet
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.text(name)
                            st.caption(info.get('description', ''))
                        with col2:
                            st.text(info.get('size', ''))
                        with col3:
                            if st.checkbox("", key=f"cn_sd15_{name}"):
                                st.success("✓")
            else:
                st.info("Drop in ControlNet models")
    
    # SDXL Section
    with tab_sdxl:
        tab_models, tab_loras, tab_vae, tab_controlnet = st.tabs([
            "Models", "Loras", "Vae", "Controlnet"
        ])
        
        with tab_models:
            st.markdown("#### SDXL Checkpoints")
            
            # Filter SDXL models (non-Pony)
            if sdxl_models:
                sdxl_filtered = {k: v for k, v in sdxl_models.items() 
                                if 'pony' not in k.lower() and 'illustrious' not in k.lower()}
                
                cols = st.columns(3)
                for idx, (name, info) in enumerate(sdxl_filtered.items()):
                    with cols[idx % 3]:
                        with st.container():
                            st.markdown(f"""
                            <div class="model-card">
                                <h5>{name[:30]}...</h5>
                                <p>Size: {info.get('size', 'Unknown')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.checkbox("Select", key=f"sdxl_model_{name}")
                            with col2:
                                model_path = Path('/workspace/SD-DarkMaster-Pro/storage/models/Stable-diffusion') / name
                                if model_path.exists():
                                    st.success("✅")
                                else:
                                    st.button("⬇️", key=f"dl_sdxl_{name}")
            else:
                st.info("No SDXL models found")
        
        with tab_loras:
            st.markdown("#### SDXL LoRAs")
            st.info("Drop SDXL LoRAs here")
        
        with tab_vae:
            st.markdown("#### SDXL VAE")
            st.info("Drop SDXL VAE models here")
        
        with tab_controlnet:
            st.markdown("#### SDXL ControlNet")
            st.info("Drop SDXL ControlNet models here")
    
    # PONY Section
    with tab_pony:
        tab_models, tab_loras, tab_empty = st.tabs(["Models", "Loras", ""])
        
        with tab_models:
            st.markdown("#### Pony Checkpoints")
            
            # Filter Pony models
            if sdxl_models:
                pony_models = {k: v for k, v in sdxl_models.items() 
                             if 'pony' in k.lower()}
                
                if pony_models:
                    cols = st.columns(3)
                    for idx, (name, info) in enumerate(pony_models.items()):
                        with cols[idx % 3]:
                            with st.container():
                                st.markdown(f"""
                                <div class="model-card">
                                    <h5>{name[:30]}...</h5>
                                    <p>Size: {info.get('size', 'Unknown')}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.checkbox("Select", key=f"pony_model_{name}")
                                with col2:
                                    model_path = Path('/workspace/SD-DarkMaster-Pro/storage/models/Stable-diffusion') / name
                                    if model_path.exists():
                                        st.success("✅")
                                    else:
                                        st.button("⬇️", key=f"dl_pony_{name}")
                else:
                    st.info("No Pony models found")
            else:
                st.info("No Pony models available")
        
        with tab_loras:
            st.markdown("#### Pony LoRAs")
            st.info("Drop Pony LoRAs here")
        
        with tab_empty:
            pass  # Empty tab placeholder
    
    # Illustrous Section
    with tab_illustrous:
        tab_models, tab_loras, tab_empty = st.tabs(["Models", "Loras", ""])
        
        with tab_models:
            st.markdown("#### Illustrious Checkpoints")
            
            # Filter Illustrious models
            if sdxl_models:
                illustrious_models = {k: v for k, v in sdxl_models.items() 
                                    if 'illustrious' in k.lower()}
                
                if illustrious_models:
                    cols = st.columns(3)
                    for idx, (name, info) in enumerate(illustrious_models.items()):
                        with cols[idx % 3]:
                            with st.container():
                                st.markdown(f"""
                                <div class="model-card">
                                    <h5>{name[:30]}...</h5>
                                    <p>Size: {info.get('size', 'Unknown')}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.checkbox("Select", key=f"illust_model_{name}")
                                with col2:
                                    model_path = Path('/workspace/SD-DarkMaster-Pro/storage/models/Stable-diffusion') / name
                                    if model_path.exists():
                                        st.success("✅")
                                    else:
                                        st.button("⬇️", key=f"dl_illust_{name}")
                else:
                    st.info("No Illustrious models found")
            else:
                st.info("No Illustrious models available")
        
        with tab_loras:
            st.markdown("#### Illustrious LoRAs")
            st.info("Drop Illustrious LoRAs here")
        
        with tab_empty:
            pass  # Empty tab placeholder
    
    # MISC Section - Extension Models
    with tab_misc:
        ext_tabs = st.tabs([
            "SAM", 
            "Adetailer", 
            "Upscaler", 
            "Reactor", 
            "Expandable for future extensions"
        ])
        
        with ext_tabs[0]:
            st.markdown("#### SAM Models")
            sam_models = MODEL_REGISTRY.get('sam', {})
            
            if sam_models:
                for name, info in sam_models.items():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.text(name)
                        st.caption(info.get('description', ''))
                    with col2:
                        st.text(info.get('size', ''))
                    with col3:
                        model_path = Path('/workspace/SD-DarkMaster-Pro/storage/sam') / name
                        if model_path.exists():
                            st.success("✅")
                        else:
                            st.text("❌")
                    with col4:
                        st.checkbox("Select", key=f"sam_{name}")
            else:
                st.info("No SAM models configured")
        
        with ext_tabs[1]:
            st.markdown("#### ADetailer Models")
            adetailer_models = MODEL_REGISTRY.get('adetailer', {})
            
            if adetailer_models:
                for name, info in adetailer_models.items():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.text(name)
                        st.caption(info.get('description', ''))
                    with col2:
                        st.text(info.get('size', ''))
                    with col3:
                        model_path = Path('/workspace/SD-DarkMaster-Pro/storage/adetailer') / name
                        if model_path.exists():
                            st.success("✅")
                        else:
                            st.text("❌")
                    with col4:
                        st.checkbox("Select", key=f"adet_{name}")
            else:
                st.info("No ADetailer models configured")
        
        with ext_tabs[2]:
            st.markdown("#### Upscaler Models")
            upscaler_models = MODEL_REGISTRY.get('upscalers', {})
            
            if upscaler_models:
                for name, info in upscaler_models.items():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.text(name)
                        st.caption(info.get('description', ''))
                    with col2:
                        st.text(info.get('size', ''))
                    with col3:
                        model_path = Path('/workspace/SD-DarkMaster-Pro/storage/upscalers') / name
                        if model_path.exists():
                            st.success("✅")
                        else:
                            st.text("❌")
                    with col4:
                        st.checkbox("Select", key=f"upscale_{name}")
            else:
                st.info("No Upscaler models configured")
        
        with ext_tabs[3]:
            st.markdown("#### Reactor Models")
            reactor_models = MODEL_REGISTRY.get('reactor', {})
            
            if reactor_models:
                for name, info in reactor_models.items():
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.text(name)
                        st.caption(info.get('description', ''))
                    with col2:
                        st.text(info.get('size', ''))
                    with col3:
                        model_path = Path('/workspace/SD-DarkMaster-Pro/storage/reactor') / name
                        if model_path.exists():
                            st.success("✅")
                        else:
                            st.text("❌")
                    with col4:
                        st.checkbox("Select", key=f"reactor_{name}")
            else:
                st.info("No Reactor models configured")
        
        with ext_tabs[4]:
            st.markdown("#### Future Extensions")
            st.info("This tab is expandable for future extension models")
            st.markdown("""
            Potential future extensions:
            - AnimateDiff models
            - IP-Adapter models
            - InstantID models
            - FaceID models
            - Custom trained models
            """)

with tab2:
    st.markdown("### 🔍 Model Browser")
    
    # Browser tabs
    browser_tabs = st.tabs(["CivitAI", "HuggingFace", "Local Files"])
    
    with browser_tabs[0]:
        st.markdown("#### CivitAI Browser")
        
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            search = st.text_input("Search models", placeholder="e.g., anime, realistic, cartoon")
        with col2:
            model_type = st.selectbox("Type", ["All", "Checkpoint", "LoRA", "VAE", "TextualInversion"])
        with col3:
            st.checkbox("Include NSFW")
        
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("Sort by", ["Most Downloaded", "Highest Rated", "Most Recent"])
        with col2:
            period = st.selectbox("Period", ["All Time", "Year", "Month", "Week", "Day"])
        
        if st.button("🔍 Search CivitAI", use_container_width=True):
            with st.spinner("Searching CivitAI..."):
                st.info(f"Searching for: {search}")
                # Results would go here
    
    with browser_tabs[1]:
        st.markdown("#### HuggingFace Hub")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            hf_search = st.text_input("Search HuggingFace", placeholder="e.g., stable-diffusion, controlnet")
        with col2:
            hf_type = st.selectbox("Type", ["All", "Models", "Datasets"])
        
        if st.button("🔍 Search HuggingFace", use_container_width=True):
            st.info(f"Searching HuggingFace for: {hf_search}")
    
    with browser_tabs[2]:
        st.markdown("#### Local File Browser")
        
        path = st.text_input("Path", value="/workspace/SD-DarkMaster-Pro/storage")
        
        if st.button("📂 Browse", use_container_width=True):
            st.info(f"Browsing: {path}")

with tab3:
    st.markdown("### ⚙️ Settings")
    
    setting_tabs = st.tabs(["WebUI", "Paths", "Performance", "Download", "Theme"])
    
    with setting_tabs[0]:
        st.markdown("#### WebUI Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            webui_type = st.selectbox("WebUI Type", ["Forge", "ComfyUI", "A1111", "ReForge"])
            port = st.number_input("Port", value=7860, min_value=1000, max_value=65535)
            st.checkbox("Auto-launch browser")
        
        with col2:
            st.checkbox("Enable Gradio Share")
            st.checkbox("Enable API")
            st.checkbox("Listen on all interfaces (0.0.0.0)")
        
        st.markdown("##### Command Line Arguments")
        extra_args = st.text_area("Additional arguments", placeholder="--xformers --no-half-vae")
        
        if st.button("💾 Save WebUI Settings", use_container_width=True):
            st.success("Settings saved!")
    
    with setting_tabs[1]:
        st.markdown("#### Storage Paths")
        
        st.text_input("Models Path", value="/workspace/SD-DarkMaster-Pro/storage/models")
        st.text_input("LoRA Path", value="/workspace/SD-DarkMaster-Pro/storage/models/Lora")
        st.text_input("VAE Path", value="/workspace/SD-DarkMaster-Pro/storage/models/VAE")
        st.text_input("ControlNet Path", value="/workspace/SD-DarkMaster-Pro/storage/models/ControlNet")
        st.text_input("Output Path", value="/workspace/SD-DarkMaster-Pro/outputs")
        st.text_input("Temp Path", value="/tmp/sd-temp")
        
        if st.button("💾 Save Path Settings", use_container_width=True):
            st.success("Paths updated!")
    
    with setting_tabs[2]:
        st.markdown("#### Performance Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.slider("Batch Size", 1, 8, 1)
            st.slider("Clip Skip", 1, 12, 2)
            st.checkbox("xFormers Optimization")
            st.checkbox("CPU Offload")
            st.checkbox("Sequential CPU Offload")
        
        with col2:
            st.selectbox("Precision", ["fp16", "fp32", "bf16"])
            st.selectbox("VAE Precision", ["fp16", "fp32", "auto"])
            st.checkbox("Attention Slicing")
            st.checkbox("Tiled VAE")
            st.checkbox("Token Merging")
        
        if st.button("💾 Save Performance Settings", use_container_width=True):
            st.success("Performance settings saved!")
    
    with setting_tabs[3]:
        st.markdown("#### Download Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Max concurrent downloads", value=3, min_value=1, max_value=10)
            st.number_input("Retry attempts", value=3, min_value=1, max_value=10)
            st.checkbox("Use aria2c for downloads")
        
        with col2:
            st.number_input("Connection timeout (seconds)", value=30, min_value=10, max_value=300)
            st.number_input("Download timeout (seconds)", value=3600, min_value=60, max_value=86400)
            st.checkbox("Verify checksums")
        
        st.markdown("##### Proxy Settings")
        proxy_url = st.text_input("HTTP Proxy", placeholder="http://proxy.example.com:8080")
        
        if st.button("💾 Save Download Settings", use_container_width=True):
            st.success("Download settings saved!")
    
    with setting_tabs[4]:
        st.markdown("#### Theme Settings")
        
        theme = st.selectbox("Theme", ["Dark Mode Pro", "Light", "Auto", "Custom"])
        
        if theme == "Custom":
            col1, col2 = st.columns(2)
            with col1:
                st.color_picker("Primary Color", value="#10B981")
                st.color_picker("Background Color", value="#0a0a0a")
                st.color_picker("Surface Color", value="#1a1a2e")
            
            with col2:
                st.color_picker("Text Color", value="#e0e0e0")
                st.color_picker("Border Color", value="#2a2a3e")
                st.slider("Border Radius", 0, 20, 8)
        
        st.slider("UI Scale", 0.8, 1.5, 1.0, 0.1)
        st.checkbox("Enable animations")
        st.checkbox("Show tooltips")
        
        if st.button("💾 Save Theme Settings", use_container_width=True):
            st.success("Theme settings saved!")

# Sidebar for quick actions
with st.sidebar:
    st.markdown("### 🚀 Quick Actions")
    
    if st.button("🎯 Launch WebUI", use_container_width=True):
        st.success("Launching...")
    
    if st.button("📥 Download Selected", use_container_width=True):
        selected_count = 0  # Would count actual selections
        st.info(f"Downloading {selected_count} models...")
    
    if st.button("🧹 Clean Cache", use_container_width=True):
        st.warning("Cleaning cache...")
    
    if st.button("🔄 Refresh Models", use_container_width=True):
        st.info("Refreshing model list...")
    
    st.markdown("---")
    
    # Platform info
    import sys
    platform = 'Colab' if 'google.colab' in sys.modules else 'Local'
    st.info(f"📍 Platform: {platform}")
    
    # System stats
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        st.metric("CPU", f"{cpu}%")
        st.metric("RAM", f"{mem}%")
        st.metric("Disk", f"{disk}%")
    except:
        st.info("System stats unavailable")
    
    st.markdown("---")
    st.markdown("#### 📊 Model Stats")
    st.metric("Total Models", "0")
    st.metric("Downloaded", "0")
    st.metric("Storage Used", "0 GB")