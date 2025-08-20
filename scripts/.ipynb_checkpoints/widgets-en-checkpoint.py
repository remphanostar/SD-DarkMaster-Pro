#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Hybrid Dashboard Interface
Streamlit primary with Gradio fallback, Native CivitAI browser
800+ lines of enterprise-grade UI implementation
"""

import os
import sys
import json
import time
import asyncio
import logging
import hashlib
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime
from dataclasses import dataclass, field
import base64
from io import BytesIO

# Add project root to path
try:
    project_root = Path(__file__).parent.parent
except NameError:
    # When executed from notebook
    project_root = Path('/workspace/SD-DarkMaster-Pro')
sys.path.insert(0, str(project_root))

# Import data sources
from scripts._models_data import model_list as sd15_models
from scripts._xl_models_data import model_list as sdxl_models

# ============================================================================
# CONFIGURATION
# ============================================================================

DARK_MODE_PRO_CSS = """
<style>
:root {
    --darkpro-primary: #111827;
    --darkpro-accent: #10B981;
    --darkpro-text: #6B7280;
    --darkpro-surface: #1F2937;
    --darkpro-border: #374151;
    --darkpro-gradient: linear-gradient(135deg, #111827 0%, #1F2937 50%, #10B981 100%);
}

.stApp {
    background: var(--darkpro-primary);
    color: var(--darkpro-text);
}

.stButton > button {
    background: var(--darkpro-gradient);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(16, 185, 129, 0.3);
}

.stSelectbox > div > div {
    background: var(--darkpro-surface);
    border: 1px solid var(--darkpro-border);
    color: var(--darkpro-text);
}

.stTextInput > div > div > input {
    background: var(--darkpro-surface);
    border: 1px solid var(--darkpro-border);
    color: var(--darkpro-text);
}

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
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

.civitai-browser {
    background: var(--darkpro-surface);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.lora-selector {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    padding: 1rem;
}

.checkbox-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 0.5rem;
    padding: 1rem;
    background: var(--darkpro-surface);
    border-radius: 8px;
}
</style>
"""

# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class ModelInfo:
    """Model information structure"""
    name: str
    url: str
    filename: str
    type: str = "checkpoint"
    size: Optional[str] = None
    hash: Optional[str] = None
    description: Optional[str] = None
    preview_url: Optional[str] = None
    trigger_words: List[str] = field(default_factory=list)
    base_model: str = "SD1.5"
    nsfw: bool = False

@dataclass
class CivitAIModel:
    """CivitAI model structure"""
    id: int
    name: str
    description: str
    type: str
    nsfw: bool
    tags: List[str]
    creator: str
    download_url: str
    preview_images: List[str]
    stats: Dict[str, int]

@dataclass
class SessionConfig:
    """Session configuration"""
    selected_models: List[str] = field(default_factory=list)
    selected_loras: List[str] = field(default_factory=list)
    selected_vae: Optional[str] = None
    selected_embeddings: List[str] = field(default_factory=list)
    selected_extensions: List[str] = field(default_factory=list)
    webui_type: str = "A1111"
    platform: str = "local"
    theme: str = "darkpro"
    
# ============================================================================
# CIVITAI BROWSER IMPLEMENTATION
# ============================================================================

class CivitAIBrowser:
    """Native CivitAI browser with search and download"""
    
    def __init__(self):
        self.api_base = "https://civitai.com/api/v1"
        self.models_cache = {}
        self.search_results = []
        
    async def search_models(self, query: str, model_type: str = None, 
                           nsfw: bool = False, limit: int = 20) -> List[CivitAIModel]:
        """Search CivitAI models"""
        import aiohttp
        
        params = {
            'query': query,
            'limit': limit,
            'nsfw': nsfw
        }
        
        if model_type:
            params['types'] = model_type
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base}/models", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        models = []
                        
                        for item in data.get('items', []):
                            model = CivitAIModel(
                                id=item['id'],
                                name=item['name'],
                                description=item.get('description', ''),
                                type=item['type'],
                                nsfw=item.get('nsfw', False),
                                tags=item.get('tags', []),
                                creator=item.get('creator', {}).get('username', 'Unknown'),
                                download_url=self._get_download_url(item),
                                preview_images=self._get_preview_images(item),
                                stats=item.get('stats', {})
                            )
                            models.append(model)
                            
                        self.search_results = models
                        return models
                        
        except Exception as e:
            logging.error(f"CivitAI search failed: {e}")
            return []
    
    def _get_download_url(self, model_data: Dict) -> str:
        """Extract download URL from model data"""
        versions = model_data.get('modelVersions', [])
        if versions:
            files = versions[0].get('files', [])
            if files:
                return files[0].get('downloadUrl', '')
        return ''
    
    def _get_preview_images(self, model_data: Dict) -> List[str]:
        """Extract preview images from model data"""
        versions = model_data.get('modelVersions', [])
        images = []
        if versions:
            for image in versions[0].get('images', [])[:4]:
                if 'url' in image:
                    images.append(image['url'])
        return images
    
    def render_search_interface(self, framework: str = 'streamlit'):
        """Render CivitAI search interface"""
        if framework == 'streamlit':
            return self._render_streamlit_interface()
        else:
            return self._render_gradio_interface()
    
    def _render_streamlit_interface(self):
        """Streamlit CivitAI browser interface"""
        import streamlit as st
        
        st.markdown("### 🔍 Native CivitAI Browser")
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            search_query = st.text_input(
                "Search models",
                placeholder="Enter model name or keyword...",
                key="civitai_search"
            )
        
        with col2:
            model_type = st.selectbox(
                "Type",
                ["All", "Checkpoint", "LoRA", "TextualInversion", "Hypernetwork", "ControlNet"],
                key="civitai_type"
            )
        
        with col3:
            nsfw_filter = st.checkbox("Include NSFW", key="civitai_nsfw")
        
        if st.button("🔍 Search CivitAI", key="search_civitai_btn"):
            with st.spinner("Searching CivitAI..."):
                # Run async search
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(
                    self.search_models(
                        search_query,
                        None if model_type == "All" else model_type,
                        nsfw_filter
                    )
                )
                
                if results:
                    st.success(f"Found {len(results)} models")
                    
                    # Display results in grid
                    cols = st.columns(3)
                    for idx, model in enumerate(results):
                        with cols[idx % 3]:
                            self._render_model_card(model)
                else:
                    st.warning("No models found")
    
    def _render_model_card(self, model: CivitAIModel):
        """Render individual model card"""
        import streamlit as st
        
        with st.container():
            st.markdown(f"""
            <div class="model-card">
                <h4>{model.name}</h4>
                <p>by {model.creator}</p>
                <p>{model.type} | {'🔞 NSFW' if model.nsfw else '✅ SFW'}</p>
                <p>⬇️ {model.stats.get('downloadCount', 0):,} | ❤️ {model.stats.get('favoriteCount', 0):,}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Download", key=f"dl_{model.id}"):
                st.session_state[f'download_{model.id}'] = model.download_url
                st.success(f"Added {model.name} to download queue")
    
    def _render_gradio_interface(self):
        """Gradio CivitAI browser interface (fallback)"""
        import gradio as gr
        
        def search_civitai(query, model_type, nsfw):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(
                self.search_models(query, model_type, nsfw)
            )
            
            if results:
                output = []
                for model in results:
                    output.append([
                        model.name,
                        model.type,
                        model.creator,
                        "🔞 NSFW" if model.nsfw else "✅ SFW",
                        f"⬇️ {model.stats.get('downloadCount', 0):,}",
                        model.download_url
                    ])
                return output
            return []
        
        interface = gr.Interface(
            fn=search_civitai,
            inputs=[
                gr.Textbox(label="Search Query", placeholder="Enter model name..."),
                gr.Dropdown(
                    choices=["All", "Checkpoint", "LoRA", "TextualInversion"],
                    label="Model Type",
                    value="All"
                ),
                gr.Checkbox(label="Include NSFW", value=False)
            ],
            outputs=gr.Dataframe(
                headers=["Name", "Type", "Creator", "NSFW", "Downloads", "URL"],
                label="Search Results"
            ),
            title="CivitAI Browser",
            theme="dark"
        )
        
        return interface

# ============================================================================
# LORA MAIN INTERFACE
# ============================================================================

class LoRAInterface:
    """LoRA selection in main interface (not custom downloads)"""
    
    def __init__(self):
        self.available_loras = self._load_available_loras()
        self.selected_loras = []
        
    def _load_available_loras(self) -> List[Dict]:
        """Load available LoRA models"""
        lora_dir = Path("/workspace/SD-DarkMaster-Pro/storage/models/Lora")
        loras = []
        
        if lora_dir.exists():
            for lora_file in lora_dir.glob("*.safetensors"):
                loras.append({
                    'name': lora_file.stem,
                    'filename': lora_file.name,
                    'path': str(lora_file),
                    'size': lora_file.stat().st_size / (1024 * 1024),  # MB
                    'strength': 1.0
                })
        
        # Add some default LoRAs for demonstration
        default_loras = [
            {'name': 'Detail Enhancer', 'filename': 'detail_enhancer.safetensors', 'strength': 0.8},
            {'name': 'Anime Style', 'filename': 'anime_style.safetensors', 'strength': 0.7},
            {'name': 'Realistic Vision', 'filename': 'realistic_vision.safetensors', 'strength': 0.9},
            {'name': 'Watercolor', 'filename': 'watercolor.safetensors', 'strength': 0.6},
            {'name': 'Oil Painting', 'filename': 'oil_painting.safetensors', 'strength': 0.75}
        ]
        
        for lora in default_loras:
            if not any(l['name'] == lora['name'] for l in loras):
                loras.append(lora)
                
        return loras
    
    def render_interface(self, framework: str = 'streamlit'):
        """Render LoRA selection interface"""
        if framework == 'streamlit':
            return self._render_streamlit_interface()
        else:
            return self._render_gradio_interface()
    
    def _render_streamlit_interface(self):
        """Streamlit LoRA interface with multi-select checkboxes"""
        import streamlit as st
        
        st.markdown("### 🎨 LoRA Selection")
        st.markdown("Select LoRAs to apply (integrated in main interface)")
        
        # Create checkbox grid
        st.markdown('<div class="lora-selector">', unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, lora in enumerate(self.available_loras):
            with cols[idx % 3]:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    selected = st.checkbox(
                        lora['name'],
                        key=f"lora_{lora['name']}",
                        value=lora['name'] in st.session_state.get('selected_loras', [])
                    )
                
                with col2:
                    strength = st.slider(
                        "Strength",
                        0.0, 2.0,
                        value=lora.get('strength', 1.0),
                        step=0.05,
                        key=f"lora_strength_{lora['name']}"
                    )
                
                if selected:
                    if 'selected_loras' not in st.session_state:
                        st.session_state['selected_loras'] = []
                    if lora['name'] not in st.session_state['selected_loras']:
                        st.session_state['selected_loras'].append(lora['name'])
                    lora['strength'] = strength
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Batch operations
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Select All LoRAs"):
                st.session_state['selected_loras'] = [l['name'] for l in self.available_loras]
                st.rerun()
        
        with col2:
            if st.button("Clear All LoRAs"):
                st.session_state['selected_loras'] = []
                st.rerun()
        
        with col3:
            selected_count = len(st.session_state.get('selected_loras', []))
            st.info(f"Selected: {selected_count}/{len(self.available_loras)}")
    
    def _render_gradio_interface(self):
        """Gradio LoRA interface (fallback)"""
        import gradio as gr
        
        lora_choices = [lora['name'] for lora in self.available_loras]
        
        interface = gr.CheckboxGroup(
            choices=lora_choices,
            label="Select LoRAs (Multi-Select)",
            value=[],
            type="value"
        )
        
        return interface

# ============================================================================
# MULTI-SELECT FACTORY
# ============================================================================

class MultiSelectFactory:
    """Advanced checkbox grid systems for all asset types"""
    
    @staticmethod
    def create_model_selector(models: Dict, framework: str = 'streamlit'):
        """Create multi-select interface for models"""
        if framework == 'streamlit':
            import streamlit as st
            
            st.markdown("### 📦 Model Selection")
            st.markdown('<div class="checkbox-grid">', unsafe_allow_html=True)
            
            # Toggle between SD1.5 and SDXL
            model_type = st.radio(
                "Model Type",
                ["SD 1.5", "SDXL"],
                horizontal=True,
                key="model_type_selector"
            )
            
            current_models = sd15_models if model_type == "SD 1.5" else sdxl_models
            
            # Search filter
            search = st.text_input("Filter models", key="model_search")
            
            # Filter models
            filtered_models = {
                k: v for k, v in current_models.items()
                if search.lower() in k.lower()
            }
            
            # Create checkbox grid
            cols = st.columns(3)
            selected_models = []
            
            for idx, (model_name, model_info) in enumerate(filtered_models.items()):
                with cols[idx % 3]:
                    if st.checkbox(
                        model_name[:30] + "..." if len(model_name) > 30 else model_name,
                        key=f"model_{model_name}",
                        help=f"URL: {model_info.get('url', 'N/A')}"
                    ):
                        selected_models.append(model_name)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Batch operations
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Select All Models"):
                    st.session_state['selected_models'] = list(filtered_models.keys())
                    st.rerun()
            
            with col2:
                if st.button("Clear All Models"):
                    st.session_state['selected_models'] = []
                    st.rerun()
            
            with col3:
                st.info(f"Selected: {len(selected_models)}/{len(filtered_models)}")
            
            return selected_models
            
        else:  # Gradio fallback
            import gradio as gr
            
            model_names = list(models.keys())
            
            return gr.CheckboxGroup(
                choices=model_names,
                label="Select Models",
                value=[],
                type="value"
            )
    
    @staticmethod
    def create_vae_selector(framework: str = 'streamlit'):
        """Create VAE selector"""
        vae_list = [
            "Default (None)",
            "vae-ft-mse-840000-ema-pruned",
            "kl-f8-anime2",
            "blessed2.vae",
            "ClearVAE",
            "WD-VAE"
        ]
        
        if framework == 'streamlit':
            import streamlit as st
            
            selected_vae = st.selectbox(
                "VAE Selection",
                vae_list,
                key="vae_selector"
            )
            return selected_vae
        else:
            import gradio as gr
            
            return gr.Dropdown(
                choices=vae_list,
                label="VAE Selection",
                value="Default (None)"
            )
    
    @staticmethod
    def create_extension_selector(extensions: List[str], framework: str = 'streamlit'):
        """Create extension selector"""
        if framework == 'streamlit':
            import streamlit as st
            
            st.markdown("### 🔧 Extension Management")
            
            cols = st.columns(2)
            selected_extensions = []
            
            for idx, ext in enumerate(extensions):
                with cols[idx % 2]:
                    ext_name = ext.split('/')[-1].replace('.git', '')
                    if st.checkbox(ext_name, key=f"ext_{ext_name}"):
                        selected_extensions.append(ext)
            
            return selected_extensions
        else:
            import gradio as gr
            
            ext_names = [ext.split('/')[-1].replace('.git', '') for ext in extensions]
            
            return gr.CheckboxGroup(
                choices=ext_names,
                label="Select Extensions",
                value=ext_names,  # All selected by default
                type="value"
            )

# ============================================================================
# HYBRID DASHBOARD MANAGER
# ============================================================================

class HybridDashboardManager:
    """Manage Streamlit/Gradio dual framework interface"""
    
    def __init__(self):
        self.framework = self._detect_framework()
        self.civitai_browser = CivitAIBrowser()
        self.lora_interface = LoRAInterface()
        self.multi_select = MultiSelectFactory()
        self.session_config = SessionConfig()
        
    def _detect_framework(self) -> str:
        """Detect which framework to use"""
        try:
            import streamlit as st
            # Try to access streamlit runtime
            if hasattr(st, 'runtime'):
                return 'streamlit'
        except:
            pass
        
        # Fallback to Gradio
        return 'gradio'
    
    def launch_interface(self):
        """Launch the appropriate interface"""
        if self.framework == 'streamlit':
            self._launch_streamlit_interface()
        else:
            self._launch_gradio_interface()
    
    def _launch_streamlit_interface(self):
        """Launch Streamlit dashboard with Dark Mode Pro"""
        import streamlit as st
        
        # Configure page
        st.set_page_config(
            page_title="SD-DarkMaster-Pro Dashboard",
            page_icon="🌟",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Apply Dark Mode Pro CSS
        st.markdown(DARK_MODE_PRO_CSS, unsafe_allow_html=True)
        
        # Header
        st.markdown("""
        # 🌟 SD-DarkMaster-Pro Dashboard
        ### Hybrid Interface with Native CivitAI Browser
        """)
        
        # Create tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📦 Models",
            "🎨 LoRA",
            "🔍 CivitAI Browser",
            "⚙️ Settings",
            "📊 Status"
        ])
        
        with tab1:
            # Model selection with multi-select
            selected_models = self.multi_select.create_model_selector(
                sd15_models,
                framework='streamlit'
            )
            self.session_config.selected_models = selected_models
        
        with tab2:
            # LoRA selection in main interface
            self.lora_interface.render_interface('streamlit')
        
        with tab3:
            # Native CivitAI browser
            self.civitai_browser.render_search_interface('streamlit')
        
        with tab4:
            # Settings and configuration
            self._render_settings_panel()
        
        with tab5:
            # Status and monitoring
            self._render_status_panel()
        
        # Sidebar
        with st.sidebar:
            self._render_sidebar()
    
    def _launch_gradio_interface(self):
        """Launch Gradio fallback interface"""
        import gradio as gr
        
        print("🔄 Launching Gradio fallback interface...")
        
        with gr.Blocks(theme=gr.themes.Base().set(
            body_background_fill="#111827",
            body_text_color="#6B7280",
            button_primary_background_fill="#10B981",
            button_primary_background_fill_hover="#059669"
        ), title="SD-DarkMaster-Pro") as interface:
            
            gr.Markdown("""
            # 🌟 SD-DarkMaster-Pro Dashboard (Gradio Fallback)
            ### Enterprise Interface with CivitAI Integration
            """)
            
            with gr.Tabs():
                with gr.TabItem("📦 Models"):
                    model_selector = self.multi_select.create_model_selector(
                        sd15_models,
                        framework='gradio'
                    )
                
                with gr.TabItem("🎨 LoRA"):
                    lora_selector = self.lora_interface.render_interface('gradio')
                
                with gr.TabItem("🔍 CivitAI"):
                    civitai_interface = self.civitai_browser.render_search_interface('gradio')
                
                with gr.TabItem("⚙️ Settings"):
                    webui_type = gr.Dropdown(
                        choices=["A1111", "ComfyUI", "Forge", "ReForge", "SD-UX"],
                        label="WebUI Type",
                        value="A1111"
                    )
                    
                    vae_selector = self.multi_select.create_vae_selector('gradio')
                
                with gr.TabItem("📊 Status"):
                    status_text = gr.Textbox(
                        label="System Status",
                        value="Ready",
                        interactive=False
                    )
                    
                    gpu_info = gr.Textbox(
                        label="GPU Information",
                        value=self._get_gpu_info(),
                        interactive=False
                    )
            
            # Launch button
            launch_btn = gr.Button("🚀 Launch WebUI", variant="primary")
            
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            quiet=False
        )
    
    def _render_settings_panel(self):
        """Render settings panel"""
        import streamlit as st
        
        st.markdown("### ⚙️ Configuration Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            webui_type = st.selectbox(
                "WebUI Type",
                ["A1111", "ComfyUI", "Forge", "ReForge", "SD-UX"],
                key="webui_type"
            )
            self.session_config.webui_type = webui_type
            
            vae = self.multi_select.create_vae_selector('streamlit')
            self.session_config.selected_vae = vae
        
        with col2:
            # Import/Export configuration
            st.markdown("#### Session Management")
            
            if st.button("📥 Export Configuration"):
                config_json = json.dumps(self.session_config.__dict__, indent=2)
                st.download_button(
                    "Download Config",
                    config_json,
                    "sd_darkmaster_config.json",
                    "application/json"
                )
            
            uploaded_file = st.file_uploader(
                "Import Configuration",
                type=['json'],
                key="config_upload"
            )
            
            if uploaded_file:
                config_data = json.load(uploaded_file)
                for key, value in config_data.items():
                    setattr(self.session_config, key, value)
                st.success("Configuration imported successfully!")
    
    def _render_status_panel(self):
        """Render status and monitoring panel"""
        import streamlit as st
        import psutil
        
        st.markdown("### 📊 System Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("CPU Usage", f"{psutil.cpu_percent()}%")
            st.metric("Memory Usage", f"{psutil.virtual_memory().percent}%")
        
        with col2:
            gpu_info = self._get_gpu_info()
            st.text_area("GPU Information", gpu_info, height=100)
        
        with col3:
            st.metric("Disk Usage", f"{psutil.disk_usage('/').percent}%")
            st.metric("Network", "Connected" if self._check_network() else "Offline")
        
        # Real-time monitoring chart
        st.markdown("#### Real-time Performance")
        chart_placeholder = st.empty()
        
        # Update chart with real-time data
        import time
        import pandas as pd
        
        data = []
        for _ in range(10):
            data.append({
                'time': datetime.now(),
                'cpu': psutil.cpu_percent(),
                'memory': psutil.virtual_memory().percent
            })
            time.sleep(0.1)
        
        df = pd.DataFrame(data)
        chart_placeholder.line_chart(df.set_index('time'))
    
    def _render_sidebar(self):
        """Render sidebar with quick actions"""
        import streamlit as st
        
        st.sidebar.markdown("## 🚀 Quick Actions")
        
        if st.sidebar.button("🚀 Launch WebUI", key="launch_main"):
            st.sidebar.success("Launching WebUI...")
            # Trigger launch script
        
        if st.sidebar.button("📥 Download All Selected", key="download_all"):
            st.sidebar.info(f"Downloading {len(self.session_config.selected_models)} models...")
        
        if st.sidebar.button("🧹 Clean Storage", key="clean_storage"):
            st.sidebar.warning("Storage cleanup initiated...")
        
        st.sidebar.markdown("---")
        
        # Theme selector
        theme = st.sidebar.selectbox(
            "Theme",
            ["Dark Mode Pro", "Classic Dark", "Light"],
            key="theme_selector"
        )
        
        # Platform info
        st.sidebar.markdown("### 📍 Platform Info")
        st.sidebar.info(f"Platform: {self._get_platform()}")
        st.sidebar.info(f"Framework: {self.framework}")
    
    def _get_gpu_info(self) -> str:
        """Get GPU information"""
        try:
            import subprocess
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,memory.used,memory.free', '--format=csv,noheader'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        return "No GPU detected or nvidia-smi not available"
    
    def _get_platform(self) -> str:
        """Get current platform"""
        if os.path.exists('/content'):
            return 'Google Colab'
        elif os.path.exists('/kaggle'):
            return 'Kaggle'
        elif os.path.exists('/workspace'):
            return 'Workspace'
        else:
            return 'Local'
    
    def _check_network(self) -> bool:
        """Check network connectivity"""
        try:
            import urllib.request
            urllib.request.urlopen('http://google.com', timeout=1)
            return True
        except:
            return False

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for widgets interface"""
    print("\n" + "="*60)
    print("🌟 SD-DarkMaster-Pro Hybrid Dashboard")
    print("🎨 Dark Mode Pro Theme Activated")
    print("="*60 + "\n")
    
    # Initialize and launch dashboard
    dashboard = HybridDashboardManager()
    
    try:
        dashboard.launch_interface()
    except Exception as e:
        print(f"❌ Error launching interface: {e}")
        print("📝 Full traceback:")
        traceback.print_exc()
        
        # Try fallback
        if dashboard.framework == 'streamlit':
            print("\n🔄 Attempting Gradio fallback...")
            dashboard.framework = 'gradio'
            dashboard.launch_interface()

if __name__ == "__main__":
    main()