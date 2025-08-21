#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Config UI Launcher
Implements the dual-framework approach: Streamlit primary, Gradio fallback
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_streamlit_available():
    """Check if Streamlit is available and working"""
    try:
        import streamlit as st
        # Check if we can import without context errors
        return True
    except ImportError:
        return False
    except Exception:
        return False

def check_gradio_available():
    """Check if Gradio is available"""
    try:
        import gradio as gr
        return True
    except ImportError:
        return False

def launch_streamlit_primary():
    """Launch the primary Streamlit interface"""
    print("🚀 Launching PRIMARY Streamlit Config UI...")
    print("="*60)
    
    # Create the Streamlit app file
    streamlit_app = project_root / 'streamlit_config_ui.py'
    
    with open(streamlit_app, 'w') as f:
        f.write('''
import streamlit as st
import sys
import json
from pathlib import Path
import os

# Suppress Streamlit warnings when run from notebook
import warnings
warnings.filterwarnings('ignore')

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure page
st.set_page_config(
    page_title="SD-DarkMaster-Pro Config UI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Dark Mode Pro theme via CSS
st.markdown("""
<style>
    /* Dark Mode Pro Theme Implementation */
    .stApp {
        background: linear-gradient(135deg, #111827 0%, #1F2937 50%, #10B981 100%);
    }
    
    /* Headers with gradient */
    h1, h2, h3 {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Primary buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
    }
    
    /* Tabs with Dark Mode Pro styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(31, 41, 55, 0.5);
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #6B7280;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white !important;
        border-radius: 6px;
    }
    
    /* Metrics with dark theme */
    [data-testid="metric-container"] {
        background: rgba(31, 41, 55, 0.5);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 8px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div > div {
        background: rgba(31, 41, 55, 0.7);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #E5E7EB;
    }
    
    /* Checkboxes with accent color */
    .stCheckbox > label > span {
        color: #E5E7EB;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(31, 41, 55, 0.5);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 8px;
    }
    
    /* Success/Info/Warning boxes */
    .stAlert {
        background: rgba(31, 41, 55, 0.7);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Load data sources
try:
    from scripts._models_data import model_list as sd15_models
    from scripts._xl_models_data import model_list as sdxl_models
except:
    sd15_models = {}
    sdxl_models = {}

# Load extensions
extensions_file = project_root / 'scripts' / '_extensions.txt'
extensions = []
if extensions_file.exists():
    with open(extensions_file, 'r') as f:
        extensions = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Initialize session state
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = []
if 'selected_loras' not in st.session_state:
    st.session_state.selected_loras = []
if 'selected_extensions' not in st.session_state:
    st.session_state.selected_extensions = []

# Title with Dark Mode Pro branding
st.markdown("# 🎨 SD-DarkMaster-Pro Config UI")
st.markdown("### Unified Control Center with Native CivitAI Browser")
st.markdown("---")

# Create main tabs - following the design spec
tabs = st.tabs([
    "🏠 Dashboard",
    "📦 Models",
    "🎨 LoRA",
    "🔍 CivitAI Browser",
    "🔧 Extensions",
    "⚙️ Settings",
    "📥 Downloads",
    "📊 Storage"
])

# Dashboard Tab
with tabs[0]:
    st.markdown("## System Dashboard")
    
    # Platform metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Platform", "Workspace/RunPod", delta="Active")
    
    with col2:
        models_count = len(st.session_state.selected_models)
        st.metric("Selected Models", models_count, delta=f"+{models_count}")
    
    with col3:
        loras_count = len(st.session_state.selected_loras)
        st.metric("Selected LoRAs", loras_count, delta=f"+{loras_count}")
    
    with col4:
        storage_path = project_root / 'storage'
        if storage_path.exists():
            size_mb = sum(f.stat().st_size for f in storage_path.rglob('*') if f.is_file()) / (1024*1024)
            st.metric("Storage Used", f"{size_mb:.1f} MB")
        else:
            st.metric("Storage Used", "0 MB")
    
    st.markdown("### Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Launch WebUI", type="primary", use_container_width=True):
            st.success("WebUI launch configuration ready. Run: python scripts/launch.py")
    
    with col2:
        if st.button("📥 Download Selected", use_container_width=True):
            st.info(f"Ready to download {models_count} models and {loras_count} LoRAs")
    
    with col3:
        if st.button("🧹 Clean Storage", use_container_width=True):
            st.info("Run: python scripts/auto-cleaner.py")
    
    # System status
    with st.expander("📊 System Status", expanded=True):
        status_col1, status_col2 = st.columns(2)
        
        with status_col1:
            st.markdown("""
            **Environment:**
            - Python: 3.13
            - Platform: Workspace
            - GPU: Not detected (CPU mode)
            - Framework: Streamlit (Primary)
            """)
        
        with status_col2:
            st.markdown("""
            **Storage Paths:**
            - Models: `/storage/models/Stable-diffusion`
            - LoRA: `/storage/models/Lora`
            - VAE: `/storage/models/VAE`
            - Outputs: `/storage/outputs`
            """)

# Models Tab - Multi-select with checkboxes
with tabs[1]:
    st.markdown("## Model Selection (Multi-Choice)")
    
    # Model type selector
    model_type = st.radio(
        "Select Model Type",
        ["SD 1.5 Models", "SDXL Models"],
        horizontal=True,
        help="Switch between SD 1.5 and SDXL model databases"
    )
    
    if model_type == "SD 1.5 Models":
        st.markdown("### SD 1.5 Models from _models_data.py")
        
        if sd15_models:
            # Create columns for checkbox layout
            cols = st.columns(3)
            
            for idx, (name, info) in enumerate(sd15_models.items()):
                with cols[idx % 3]:
                    # Multi-select checkbox for each model
                    selected = st.checkbox(
                        name,
                        key=f"sd15_{name}",
                        value=name in st.session_state.selected_models
                    )
                    
                    if selected and name not in st.session_state.selected_models:
                        st.session_state.selected_models.append(name)
                    elif not selected and name in st.session_state.selected_models:
                        st.session_state.selected_models.remove(name)
                    
                    # Show model info on hover/expand
                    if selected:
                        with st.expander("Info", expanded=False):
                            st.text(f"Type: {info.get('type', 'checkpoint')}")
                            st.text(f"Size: {info.get('size', 'Unknown')}")
        else:
            st.warning("No SD 1.5 models found in _models_data.py")
    
    else:  # SDXL Models
        st.markdown("### SDXL Models from _xl_models_data.py")
        
        if sdxl_models:
            cols = st.columns(3)
            
            for idx, (name, info) in enumerate(sdxl_models.items()):
                with cols[idx % 3]:
                    selected = st.checkbox(
                        name,
                        key=f"sdxl_{name}",
                        value=name in st.session_state.selected_models
                    )
                    
                    if selected and name not in st.session_state.selected_models:
                        st.session_state.selected_models.append(name)
                    elif not selected and name in st.session_state.selected_models:
                        st.session_state.selected_models.remove(name)
        else:
            st.warning("No SDXL models found in _xl_models_data.py")
    
    # Batch operations
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Select All", use_container_width=True):
            if model_type == "SD 1.5 Models":
                st.session_state.selected_models = list(sd15_models.keys())
            else:
                st.session_state.selected_models = list(sdxl_models.keys())
            st.rerun()
    
    with col2:
        if st.button("Clear All", use_container_width=True):
            st.session_state.selected_models = []
            st.rerun()
    
    with col3:
        st.info(f"Selected: {len(st.session_state.selected_models)} models")

# LoRA Tab - Main interface integration (NOT in custom downloads)
with tabs[2]:
    st.markdown("## LoRA Selection (Main Interface)")
    st.info("LoRA selection integrated in main interface as per specification - NOT in custom downloads")
    
    # LoRA categories
    lora_categories = ["Character", "Style", "Concept", "Pose", "Clothing", "Background", "Effect"]
    selected_category = st.selectbox("Select LoRA Category", lora_categories)
    
    st.markdown(f"### {selected_category} LoRAs")
    
    # Example LoRAs with multi-select checkboxes
    example_loras = [f"{selected_category}_LoRA_{i+1}" for i in range(12)]
    
    cols = st.columns(4)
    for idx, lora in enumerate(example_loras):
        with cols[idx % 4]:
            selected = st.checkbox(
                lora,
                key=f"lora_{lora}",
                value=lora in st.session_state.selected_loras
            )
            
            if selected and lora not in st.session_state.selected_loras:
                st.session_state.selected_loras.append(lora)
            elif not selected and lora in st.session_state.selected_loras:
                st.session_state.selected_loras.remove(lora)
            
            # Strength slider for selected LoRAs
            if selected:
                st.slider(f"Strength", 0.0, 1.0, 0.7, 0.1, key=f"strength_{lora}")
    
    st.markdown("---")
    st.success(f"Selected {len(st.session_state.selected_loras)} LoRAs")

# CivitAI Browser Tab - Native integration
with tabs[3]:
    st.markdown("## 🔍 Native CivitAI Browser")
    st.info("Native CivitAI browser embedded in main interface")
    
    # Search interface
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "Search CivitAI",
            placeholder="Enter model name, style, or keyword...",
            key="civitai_search"
        )
    
    with col2:
        model_type_filter = st.selectbox(
            "Type",
            ["All", "Checkpoint", "LoRA", "Embedding", "VAE"],
            key="civitai_type"
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort",
            ["Most Downloaded", "Highest Rated", "Newest"],
            key="civitai_sort"
        )
    
    # Results grid (mock data for demonstration)
    if search_query:
        st.markdown("### Search Results")
        
        # Create a grid of results
        cols = st.columns(3)
        
        for i in range(6):
            with cols[i % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style="background: rgba(31, 41, 55, 0.5); padding: 1rem; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.2);">
                        <h4>Model {i+1}</h4>
                        <p>Type: {model_type_filter}</p>
                        <p>Downloads: {1000 * (i+1)}</p>
                        <p>Rating: ⭐ 4.{i}/5</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Download", key=f"civitai_dl_{i}"):
                        st.success(f"Added Model {i+1} to download queue")
    
    # Direct download by ID
    with st.expander("Direct Download by Model ID"):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            model_id = st.number_input("CivitAI Model ID", min_value=1, value=1)
        
        with col2:
            if st.button("Download", key="civitai_direct"):
                st.info(f"Downloading model {model_id} from CivitAI...")

# Extensions Tab
with tabs[4]:
    st.markdown("## Extension Management")
    st.info(f"Extensions loaded from _extensions.txt: {len(extensions)} found")
    
    if extensions:
        # Multi-select checkboxes for extensions
        cols = st.columns(2)
        
        for idx, ext_url in enumerate(extensions):
            ext_name = ext_url.split('/')[-1].replace('.git', '')
            
            with cols[idx % 2]:
                selected = st.checkbox(
                    ext_name,
                    key=f"ext_{ext_name}",
                    value=ext_name in st.session_state.selected_extensions,
                    help=ext_url
                )
                
                if selected and ext_name not in st.session_state.selected_extensions:
                    st.session_state.selected_extensions.append(ext_name)
                elif not selected and ext_name in st.session_state.selected_extensions:
                    st.session_state.selected_extensions.remove(ext_name)
        
        st.markdown("---")
        
        if st.button("Install Selected Extensions", type="primary", use_container_width=True):
            st.success(f"Ready to install {len(st.session_state.selected_extensions)} extensions")
    else:
        st.warning("No extensions found in _extensions.txt")

# Settings Tab
with tabs[5]:
    st.markdown("## WebUI Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### WebUI Settings")
        webui_type = st.selectbox(
            "WebUI Type",
            ["Automatic1111", "ComfyUI", "Forge", "Vladmandic", "ReForge", "SD.Next"],
            help="Select the WebUI to launch"
        )
        
        port = st.number_input(
            "Port",
            min_value=1000,
            max_value=65535,
            value=7860,
            help="Port for WebUI"
        )
        
        share_gradio = st.checkbox("Enable Gradio Share", value=False)
        enable_api = st.checkbox("Enable API", value=True)
        enable_xformers = st.checkbox("Enable xFormers", value=False)
    
    with col2:
        st.markdown("### Tunnel Settings")
        tunnel_service = st.selectbox(
            "Tunnel Service",
            ["None", "Cloudflare", "Ngrok", "Localtunnel", "Bore", "Serveo"],
            help="Select tunnel service for remote access"
        )
        
        if tunnel_service != "None":
            tunnel_port = st.number_input(
                "Tunnel Port",
                min_value=1000,
                max_value=65535,
                value=8080
            )
    
    # Save configuration
    if st.button("Save Configuration", type="primary", use_container_width=True):
        config = {
            'webui_type': webui_type,
            'port': port,
            'share': share_gradio,
            'api': enable_api,
            'xformers': enable_xformers,
            'tunnel': tunnel_service
        }
        
        config_file = project_root / 'configs' / 'webui_config.json'
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        st.success("Configuration saved successfully!")

# Downloads Tab
with tabs[6]:
    st.markdown("## Download Manager")
    
    # Queue status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Models Queued", len(st.session_state.selected_models))
    
    with col2:
        st.metric("LoRAs Queued", len(st.session_state.selected_loras))
    
    with col3:
        st.metric("Active Downloads", 0)
    
    with col4:
        st.metric("Completed", 0)
    
    # Download actions
    st.markdown("### Download Actions")
    
    if st.button("🚀 Start All Downloads", type="primary", use_container_width=True):
        total = len(st.session_state.selected_models) + len(st.session_state.selected_loras)
        st.info(f"Starting download of {total} items...")
        st.markdown("Run: `python scripts/downloading-en.py`")
    
    # Download history
    with st.expander("Download History"):
        st.markdown("""
        Recent downloads:
        - No downloads yet
        """)

# Storage Tab
with tabs[7]:
    st.markdown("## Storage Management")
    
    storage_path = project_root / 'storage'
    
    if storage_path.exists():
        # Calculate storage stats
        total_size = 0
        file_count = 0
        
        category_sizes = {}
        for category_path in storage_path.iterdir():
            if category_path.is_dir():
                category_size = sum(f.stat().st_size for f in category_path.rglob('*') if f.is_file())
                category_files = sum(1 for f in category_path.rglob('*') if f.is_file())
                category_sizes[category_path.name] = {
                    'size': category_size,
                    'files': category_files
                }
                total_size += category_size
                file_count += category_files
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Storage", f"{total_size / (1024*1024):.1f} MB")
        
        with col2:
            st.metric("Total Files", file_count)
        
        with col3:
            st.metric("Categories", len(category_sizes))
        
        # Category breakdown
        st.markdown("### Storage Breakdown")
        
        for category, info in category_sizes.items():
            col1, col2, col3 = st.columns([2, 3, 1])
            
            with col1:
                st.text(category.capitalize())
            
            with col2:
                if total_size > 0:
                    progress = info['size'] / total_size
                else:
                    progress = 0
                st.progress(progress)
            
            with col3:
                st.text(f"{info['size'] / (1024*1024):.1f} MB")
        
        # Cleanup actions
        st.markdown("---")
        
        if st.button("🧹 Run Storage Cleanup", use_container_width=True):
            st.info("Run: python scripts/auto-cleaner.py")
    else:
        st.warning("Storage directory not initialized. Run setup first.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280;">
    🎨 <b>SD-DarkMaster-Pro</b> | Unified AI Art Generation Platform<br>
    Framework: Streamlit (Primary) | Dark Mode Pro Theme Active
</div>
""", unsafe_allow_html=True)
''')
    
    # Launch Streamlit with proper configuration
    env = os.environ.copy()
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(streamlit_app),
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--theme.base", "dark",
        "--theme.primaryColor", "#10B981",
        "--theme.backgroundColor", "#111827",
        "--theme.secondaryBackgroundColor", "#1F2937",
        "--theme.textColor", "#6B7280"
    ]
    
    print(f"\n📍 Access the Config UI at: http://localhost:8501")
    print("Press Ctrl+C to stop\n")
    
    try:
        process = subprocess.Popen(cmd, env=env)
        process.wait()
    except KeyboardInterrupt:
        print("\n✅ Streamlit stopped")
        process.terminate()
        return True
    except Exception as e:
        print(f"❌ Streamlit failed: {e}")
        return False

def launch_gradio_fallback():
    """Launch the fallback Gradio interface"""
    print("\n🔄 Launching FALLBACK Gradio Config UI...")
    print("="*60)
    
    # Import and run the gradio config
    from config_ui import interface
    
    print("\n📍 Access the Config UI at: http://localhost:7860")
    print("Press Ctrl+C to stop\n")
    
    try:
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            inbrowser=False
        )
        return True
    except Exception as e:
        print(f"❌ Gradio also failed: {e}")
        return False

def main():
    """Main launcher with dual-framework approach"""
    print("\n" + "="*60)
    print("🎨 SD-DarkMaster-Pro Config UI")
    print("Dual-Framework System: Streamlit Primary, Gradio Fallback")
    print("="*60 + "\n")
    
    # Check framework availability
    streamlit_available = check_streamlit_available()
    gradio_available = check_gradio_available()
    
    print(f"✅ Streamlit: {'Available' if streamlit_available else 'Not Available'}")
    print(f"✅ Gradio: {'Available' if gradio_available else 'Not Available'}")
    print()
    
    # Try Streamlit first (PRIMARY)
    if streamlit_available:
        success = launch_streamlit_primary()
        if success:
            return
        else:
            print("\n⚠️ Streamlit failed, falling back to Gradio...")
    
    # Fallback to Gradio
    if gradio_available:
        success = launch_gradio_fallback()
        if success:
            return
    
    # Both failed
    print("\n❌ ERROR: Both Streamlit and Gradio failed to launch!")
    print("Please check your environment and dependencies.")
    sys.exit(1)

if __name__ == "__main__":
    main()