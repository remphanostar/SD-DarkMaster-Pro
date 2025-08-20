
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import the dashboard components
from scripts.widgets_en import HybridDashboardManager

# Configure Streamlit
st.set_page_config(
    page_title="SD-DarkMaster-Pro Config UI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Dark Mode Pro theme
st.markdown('''
<style>
    /* Dark Mode Pro Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* Buttons */
    .stButton > button {
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
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(26, 26, 46, 0.5);
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #9CA3AF;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white !important;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: rgba(26, 26, 46, 0.5);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        background: rgba(26, 26, 46, 0.5);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: white;
    }
    
    /* Checkboxes */
    .stCheckbox {
        color: #E5E7EB;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
    }
</style>
''', unsafe_allow_html=True)

# Title
st.markdown("# 🎨 SD-DarkMaster-Pro Config UI")
st.markdown("### Unified Control Center for AI Art Generation")

# Create tabs
tabs = st.tabs([
    "🏠 Dashboard",
    "📦 Models",
    "🎨 LoRA",
    "🔧 Extensions", 
    "⚙️ Settings",
    "📥 Downloads",
    "📊 Storage"
])

with tabs[0]:
    st.markdown("## Dashboard")
    
    # Platform info
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Platform", "Workspace")
    with col2:
        st.metric("Status", "Ready", delta="Active")
    with col3:
        st.metric("Models", "0", delta="+0")
    with col4:
        st.metric("Storage", "0 GB", delta="0%")
    
    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Launch WebUI", use_container_width=True, type="primary"):
            st.info("WebUI launch would start here")
    
    with col2:
        if st.button("📥 Download Models", use_container_width=True):
            st.info("Model download interface would open")
    
    with col3:
        if st.button("🧹 Clean Storage", use_container_width=True):
            st.info("Storage cleaner would run")

with tabs[1]:
    st.markdown("## Model Selection")
    
    # Import model data
    try:
        from scripts._models_data import model_list as sd15_models
        from scripts._xl_models_data import model_list as sdxl_models
        
        model_type = st.radio("Model Type", ["SD 1.5", "SDXL"], horizontal=True)
        
        if model_type == "SD 1.5":
            st.markdown("### SD 1.5 Models")
            
            # Create columns for checkboxes
            cols = st.columns(3)
            selected_models = []
            
            for idx, (name, info) in enumerate(sd15_models.items()):
                with cols[idx % 3]:
                    if st.checkbox(name, key=f"sd15_{name}"):
                        selected_models.append(name)
            
            if selected_models:
                st.success(f"Selected {len(selected_models)} models")
                st.session_state['selected_models'] = selected_models
        else:
            st.markdown("### SDXL Models")
            
            cols = st.columns(3)
            selected_models = []
            
            for idx, (name, info) in enumerate(sdxl_models.items()):
                with cols[idx % 3]:
                    if st.checkbox(name, key=f"sdxl_{name}"):
                        selected_models.append(name)
            
            if selected_models:
                st.success(f"Selected {len(selected_models)} models")
                st.session_state['selected_xl_models'] = selected_models
    except ImportError:
        st.warning("Model data files not found")

with tabs[2]:
    st.markdown("## LoRA Selection")
    st.info("LoRA models would be listed here with multi-select checkboxes")
    
    # Example LoRA categories
    categories = ["Character", "Style", "Concept", "Pose", "Clothing", "Background"]
    selected_category = st.selectbox("Category", categories)
    
    st.markdown(f"### {selected_category} LoRAs")
    
    # Example LoRAs
    example_loras = [f"{selected_category} LoRA {i+1}" for i in range(6)]
    cols = st.columns(3)
    
    for idx, lora in enumerate(example_loras):
        with cols[idx % 3]:
            st.checkbox(lora, key=f"lora_{lora}")

with tabs[3]:
    st.markdown("## Extension Management")
    
    try:
        extensions_file = project_root / 'scripts' / '_extensions.txt'
        if extensions_file.exists():
            with open(extensions_file, 'r') as f:
                extensions = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            st.info(f"Found {len(extensions)} extensions")
            
            cols = st.columns(2)
            selected_extensions = []
            
            for idx, ext in enumerate(extensions):
                with cols[idx % 2]:
                    ext_name = ext.split('/')[-1].replace('.git', '')
                    if st.checkbox(ext_name, key=f"ext_{ext_name}"):
                        selected_extensions.append(ext)
            
            if st.button("Install Selected Extensions", type="primary"):
                st.success(f"Would install {len(selected_extensions)} extensions")
        else:
            st.warning("Extensions file not found")
    except Exception as e:
        st.error(f"Error loading extensions: {e}")

with tabs[4]:
    st.markdown("## Settings")
    
    # WebUI Settings
    st.markdown("### WebUI Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        webui_type = st.selectbox("WebUI Type", ["Automatic1111", "ComfyUI", "Forge", "Vladmandic"])
        port = st.number_input("Port", value=7860, min_value=1000, max_value=65535)
        share_gradio = st.checkbox("Enable Gradio Share")
    
    with col2:
        tunnel_service = st.selectbox("Tunnel Service", ["None", "Cloudflare", "Ngrok", "Localtunnel"])
        api_enabled = st.checkbox("Enable API", value=True)
        xformers = st.checkbox("Enable xFormers")
    
    # Theme Settings
    st.markdown("### Theme Settings")
    
    theme_preset = st.selectbox("Theme Preset", ["Dark Mode Pro", "Midnight", "Ocean", "Forest"])
    accent_color = st.color_picker("Accent Color", "#10B981")
    
    if st.button("Save Settings", type="primary"):
        st.success("Settings saved successfully!")

with tabs[5]:
    st.markdown("## Download Manager")
    
    # Download queue status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Queued", "0")
    with col2:
        st.metric("Active", "0")
    with col3:
        st.metric("Completed", "0")
    
    # CivitAI Direct Download
    st.markdown("### CivitAI Direct Download")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        model_id = st.number_input("Model ID", min_value=1, value=1)
    
    with col2:
        version_id = st.number_input("Version ID", min_value=0, value=0)
    
    if st.button("Download from CivitAI", type="primary"):
        st.info(f"Would download model {model_id}")

with tabs[6]:
    st.markdown("## Storage Overview")
    
    # Storage metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Storage", "0 GB")
    with col2:
        st.metric("Models", "0 GB")
    with col3:
        st.metric("Outputs", "0 GB")
    
    # Storage breakdown
    st.markdown("### Storage Breakdown")
    
    storage_data = {
        "Models": 0,
        "LoRA": 0,
        "VAE": 0,
        "Embeddings": 0,
        "Outputs": 0,
        "Cache": 0
    }
    
    for category, size in storage_data.items():
        col1, col2, col3 = st.columns([2, 3, 1])
        
        with col1:
            st.text(category)
        with col2:
            st.progress(0)
        with col3:
            st.text(f"{size} GB")
    
    if st.button("Run Cleanup", type="secondary"):
        st.info("Cleanup would run here")

# Footer
st.markdown("---")
st.markdown("🎨 **SD-DarkMaster-Pro** | Unified AI Art Generation Platform")
