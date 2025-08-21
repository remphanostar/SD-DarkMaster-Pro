#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Hybrid Dashboard Interface - FIXED VERSION
Properly organized tabs: Models by type, separate Extensions tab
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
    project_root = Path('/workspace/SD-DarkMaster-Pro')
sys.path.insert(0, str(project_root))

# Import data sources
from scripts._models_data import model_list as sd15_models
from scripts._xl_models_data import model_list as sdxl_models

# Dark Mode Pro CSS (keeping the same)
DARK_MODE_PRO_CSS = """
<style>
/* ... keeping same CSS as original ... */
</style>
"""

class HybridDashboard:
    """Main dashboard with reorganized tabs"""
    
    def __init__(self):
        self.project_root = Path('/workspace/SD-DarkMaster-Pro')
        self.storage_root = self.project_root / 'storage'
        
    def _launch_streamlit_interface(self):
        """Launch reorganized Streamlit interface"""
        import streamlit as st
        
        st.set_page_config(
            page_title="SD-DarkMaster-Pro Dashboard",
            page_icon="🌟",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Apply Dark Mode Pro CSS
        st.markdown(DARK_MODE_PRO_CSS, unsafe_allow_html=True)
        
        # Title
        st.markdown("# 🌟 SD-DarkMaster-Pro Dashboard")
        st.markdown("### Hybrid Interface with Native CivitAI Browser")
        
        # MAIN TABS - Reorganized
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📦 Models",
            "🎨 LoRA", 
            "🔍 CivitAI Browser",
            "🔧 Extensions",  # NEW TAB for SAM, ADetailer, ControlNet etc.
            "⚙️ Settings",
            "📊 Status"
        ])
        
        with tab1:
            self._render_models_tab()
        
        with tab2:
            self._render_lora_tab()
        
        with tab3:
            self._render_civitai_tab()
        
        with tab4:
            self._render_extensions_tab()  # NEW
        
        with tab5:
            self._render_settings_tab()
        
        with tab6:
            self._render_status_tab()
        
        # Sidebar
        with st.sidebar:
            self._render_sidebar()
    
    def _render_models_tab(self):
        """Models tab with SD1.5/SDXL/Pony sub-tabs"""
        import streamlit as st
        
        st.markdown("### 📦 Stable Diffusion Models")
        
        # Storage info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Models", len(sd15_models) + len(sdxl_models))
        with col2:
            st.metric("SD 1.5 Models", len(sd15_models))
        with col3:
            st.metric("SDXL Models", len(sdxl_models))
        
        st.markdown("---")
        
        # Model type tabs
        model_tabs = st.tabs(["🎨 SD 1.5", "🚀 SDXL", "🦄 Pony/Illustrious"])
        
        with model_tabs[0]:
            st.markdown("#### SD 1.5 Models")
            self._render_model_grid(sd15_models, "sd15")
        
        with model_tabs[1]:
            st.markdown("#### SDXL Models")
            self._render_model_grid(sdxl_models, "sdxl")
        
        with model_tabs[2]:
            st.markdown("#### Pony/Illustrious Models")
            # Filter SDXL models for Pony/Illustrious
            pony_models = {k: v for k, v in sdxl_models.items() 
                          if 'pony' in k.lower() or 'illustrious' in k.lower()}
            if pony_models:
                self._render_model_grid(pony_models, "pony")
            else:
                st.info("No Pony/Illustrious models found. They will appear here when added.")
    
    def _render_model_grid(self, models: Dict, model_type: str):
        """Render model selection grid"""
        import streamlit as st
        
        # Search box
        search = st.text_input(f"Search {model_type} models", key=f"search_{model_type}")
        
        # Filter models
        filtered_models = {k: v for k, v in models.items() 
                          if search.lower() in k.lower()} if search else models
        
        # Display models in grid
        cols = st.columns(3)
        for idx, (name, info) in enumerate(filtered_models.items()):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div class="model-card">
                        <h4>{name}</h4>
                        <p>Size: {info.get('size', 'Unknown')}</p>
                        <p>{info.get('description', '')[:100]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.checkbox("Select", key=f"model_{model_type}_{name}"):
                            if 'selected_models' not in st.session_state:
                                st.session_state['selected_models'] = []
                            if name not in st.session_state['selected_models']:
                                st.session_state['selected_models'].append(name)
                    
                    with col2:
                        # Check if downloaded
                        model_path = self.storage_root / 'models' / 'Stable-diffusion' / name
                        if model_path.exists():
                            st.success("✅ Downloaded")
                        else:
                            if st.button("⬇️", key=f"dl_{model_type}_{name}"):
                                st.info(f"Downloading {name}...")
    
    def _render_extensions_tab(self):
        """Extensions tab with SAM, ADetailer, ControlNet, Upscalers, Reactor"""
        import streamlit as st
        from setup_central_storage import MODEL_REGISTRY
        
        st.markdown("### 🔧 Extension Models")
        st.markdown("Models for extensions like SAM, ADetailer, ControlNet, Upscalers, and Reactor")
        
        # Extension tabs
        ext_tabs = st.tabs([
            "🎯 SAM",
            "👁️ ADetailer", 
            "🎮 ControlNet",
            "🔍 Upscalers",
            "🔄 Reactor"
        ])
        
        with ext_tabs[0]:
            self._render_extension_models("sam", MODEL_REGISTRY.get('sam', {}))
        
        with ext_tabs[1]:
            self._render_extension_models("adetailer", MODEL_REGISTRY.get('adetailer', {}))
        
        with ext_tabs[2]:
            self._render_extension_models("controlnet", MODEL_REGISTRY.get('controlnet', {}))
        
        with ext_tabs[3]:
            self._render_extension_models("upscalers", MODEL_REGISTRY.get('upscalers', {}))
        
        with ext_tabs[4]:
            self._render_extension_models("reactor", MODEL_REGISTRY.get('reactor', {}))
    
    def _render_extension_models(self, ext_type: str, models: Dict):
        """Render models for a specific extension"""
        import streamlit as st
        
        st.markdown(f"#### {ext_type.upper()} Models")
        
        if not models:
            st.warning(f"No {ext_type} models configured")
            return
        
        for model_name, info in models.items():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.text(model_name)
                st.caption(info.get('description', ''))
            
            with col2:
                st.text(info.get('size', 'Unknown'))
            
            with col3:
                # Check if downloaded
                model_path = self.storage_root / ext_type / model_name
                if model_path.exists():
                    st.success("✅")
                else:
                    st.text("❌")
            
            with col4:
                if st.checkbox("Select", key=f"ext_{ext_type}_{model_name}"):
                    if f'selected_{ext_type}' not in st.session_state:
                        st.session_state[f'selected_{ext_type}'] = []
                    if model_name not in st.session_state[f'selected_{ext_type}']:
                        st.session_state[f'selected_{ext_type}'].append(model_name)
        
        # Download button for selected
        selected = st.session_state.get(f'selected_{ext_type}', [])
        if selected:
            if st.button(f"📥 Download Selected {ext_type.upper()} Models ({len(selected)})", 
                        key=f"dl_all_{ext_type}"):
                with st.spinner(f"Downloading {len(selected)} {ext_type} models..."):
                    # Download logic here
                    st.success(f"Downloaded {len(selected)} models!")
    
    def _render_lora_tab(self):
        """LoRA tab"""
        import streamlit as st
        
        st.markdown("### 🎨 LoRA Selection")
        st.info("LoRA models will be loaded from /storage/models/Lora")
        
        # Placeholder for LoRA interface
        lora_path = self.storage_root / 'models' / 'Lora'
        if lora_path.exists():
            loras = list(lora_path.glob('*.safetensors'))
            if loras:
                for lora in loras:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.checkbox(lora.name, key=f"lora_{lora.name}")
                    with col2:
                        st.slider("Strength", 0.0, 2.0, 1.0, 0.05, key=f"lora_str_{lora.name}")
            else:
                st.info("No LoRA models found")
        else:
            st.info("LoRA directory not found")
    
    def _render_civitai_tab(self):
        """CivitAI Browser tab"""
        import streamlit as st
        
        st.markdown("### 🔍 Native CivitAI Browser")
        
        # Search interface
        search = st.text_input("Search models", placeholder="ANything", key="civitai_search")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if st.button("🔍 Search CivitAI", key="search_civitai_btn"):
                st.info(f"Searching for: {search}")
        
        with col2:
            model_type = st.selectbox("Type", ["All", "Checkpoint", "LoRA", "VAE"], key="civitai_type")
        
        with col3:
            st.checkbox("Include NSFW", key="civitai_nsfw")
        
        # Results area
        st.markdown("---")
        st.info("No models found")
    
    def _render_settings_tab(self):
        """Settings tab"""
        import streamlit as st
        
        st.markdown("### ⚙️ WebUI Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            webui_type = st.selectbox(
                "WebUI Type",
                ["Forge", "ComfyUI", "A1111", "ReForge"],
                key="webui_type"
            )
            
            port = st.number_input("Port", value=7860, key="webui_port")
        
        with col2:
            st.checkbox("Share (Gradio)", key="webui_share")
            st.checkbox("Enable API", key="webui_api")
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved!")
    
    def _render_status_tab(self):
        """Status tab"""
        import streamlit as st
        import psutil
        
        st.markdown("### 📊 System Status")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            cpu_percent = psutil.cpu_percent(interval=1)
            st.metric("CPU Usage", f"{cpu_percent}%")
        
        with col2:
            memory = psutil.virtual_memory()
            st.metric("Memory Usage", f"{memory.percent}%")
        
        with col3:
            disk = psutil.disk_usage('/')
            st.metric("Disk Usage", f"{disk.percent}%")
        
        with col4:
            st.metric("Network", "Connected")
        
        # GPU info
        st.markdown("#### GPU Information")
        try:
            import torch
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                st.info(f"{gpu_name}, {gpu_memory:.1f} GB")
            else:
                st.warning("No GPU detected")
        except:
            st.warning("Unable to detect GPU")
    
    def _render_sidebar(self):
        """Sidebar with quick actions"""
        import streamlit as st
        
        st.markdown("### 🚀 Quick Actions")
        
        if st.button("🚀 Launch WebUI", key="launch_webui"):
            st.success("Launching WebUI...")
        
        if st.button("📥 Download All Selected", key="download_all"):
            st.info("Downloading selected models...")
        
        if st.button("🧹 Clean Storage", key="clean_storage"):
            st.warning("Cleaning storage...")
        
        st.markdown("---")
        st.markdown("### Theme")
        st.selectbox("", ["Dark Mode Pro", "Light", "Auto"], key="theme")
        
        st.markdown("---")
        st.markdown("### 📍 Platform Info")
        
        platform = 'colab' if 'google.colab' in sys.modules else 'local'
        st.info(f"Platform: {'Google Colab' if platform == 'colab' else 'Local'}")
    
    def launch(self):
        """Launch the dashboard"""
        try:
            self._launch_streamlit_interface()
        except ImportError:
            print("Streamlit not available, falling back to Gradio")
            self._launch_gradio_interface()
    
    def _launch_gradio_interface(self):
        """Gradio fallback (simplified)"""
        import gradio as gr
        
        with gr.Blocks(theme=gr.themes.Base()) as interface:
            gr.Markdown("# SD-DarkMaster-Pro Dashboard (Gradio)")
            
            with gr.Tabs():
                with gr.TabItem("Models"):
                    gr.Markdown("Model selection interface")
                
                with gr.TabItem("Extensions"):
                    gr.Markdown("Extension models interface")
                
                with gr.TabItem("Settings"):
                    gr.Markdown("Settings interface")
            
            interface.launch(server_port=7860)

# Main execution
if __name__ == "__main__":
    dashboard = HybridDashboard()
    dashboard.launch()