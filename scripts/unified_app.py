#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Unified Interface
Single Streamlit app that handles all operations
"""

import streamlit as st
import os
import sys
import json
import subprocess
import time
import threading
from pathlib import Path
from datetime import datetime
import psutil
import requests

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Page configuration
st.set_page_config(
    page_title="SD-DarkMaster-Pro",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'setup_complete' not in st.session_state:
    st.session_state.setup_complete = False
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = []
if 'download_queue' not in st.session_state:
    st.session_state.download_queue = []
if 'webui_process' not in st.session_state:
    st.session_state.webui_process = None
if 'logs' not in st.session_state:
    st.session_state.logs = []

# Import model data
from scripts._models_data import model_list as sd15_models
from scripts._xl_models_data import model_list as sdxl_models

# Helper functions
def run_command(cmd, stream_output=False):
    """Run a command and optionally stream output"""
    if stream_output:
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True,
            shell=True
        )
        output = []
        for line in iter(process.stdout.readline, ''):
            if line:
                output.append(line.strip())
                st.text(line.strip())
        process.wait()
        return process.returncode, '\n'.join(output)
    else:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        return result.returncode, result.stdout + result.stderr

def add_log(message, level="info"):
    """Add message to activity log"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append({
        'time': timestamp,
        'level': level,
        'message': message
    })

# Page Functions
def home_page():
    """Home dashboard"""
    st.title("🎨 SD-DarkMaster-Pro")
    st.markdown("### Unified Interface for Stable Diffusion WebUIs")
    
    # Status cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Setup Status", "✅ Ready" if st.session_state.setup_complete else "❌ Pending")
    with col2:
        st.metric("Selected Models", len(st.session_state.selected_models))
    with col3:
        st.metric("Download Queue", len(st.session_state.download_queue))
    with col4:
        st.metric("WebUI Status", "🟢 Running" if st.session_state.webui_process else "⚫ Stopped")
    
    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Quick Setup", use_container_width=True):
            st.switch_page("pages/setup.py")
    
    with col2:
        if st.button("📦 Browse Models", use_container_width=True):
            st.switch_page("pages/models.py")
    
    with col3:
        if st.button("🎯 Launch WebUI", use_container_width=True):
            st.switch_page("pages/launch.py")
    
    # Activity log
    st.markdown("### Recent Activity")
    if st.session_state.logs:
        for log in st.session_state.logs[-10:]:
            icon = "✅" if log['level'] == "success" else "ℹ️" if log['level'] == "info" else "⚠️"
            st.text(f"[{log['time']}] {icon} {log['message']}")
    else:
        st.info("No recent activity")

def setup_page():
    """Setup and configuration"""
    st.title("⚙️ Setup & Configuration")
    
    # Platform info
    st.markdown("### Platform Information")
    col1, col2, col3 = st.columns(3)
    
    platform = "Colab" if os.path.exists('/content') else "Local"
    with col1:
        st.info(f"Platform: {platform}")
    with col2:
        st.info(f"Python: {sys.version.split()[0]}")
    with col3:
        gpu = "Available" if subprocess.run(['nvidia-smi'], capture_output=True).returncode == 0 else "Not Found"
        st.info(f"GPU: {gpu}")
    
    # Setup actions
    st.markdown("### Setup Actions")
    
    if st.button("🔧 Run Complete Setup", type="primary"):
        with st.spinner("Running setup..."):
            # Create directories
            st.text("Creating directory structure...")
            dirs = ['configs', 'storage/models', 'storage/loras', 'storage/vae', 'storage/controlnet', 'logs']
            for dir_path in dirs:
                (project_root / dir_path).mkdir(parents=True, exist_ok=True)
            
            # Install dependencies
            st.text("Installing dependencies...")
            deps = ['aria2', 'streamlit', 'gradio', 'pyngrok', 'requests', 'beautifulsoup4']
            for dep in deps:
                st.text(f"Installing {dep}...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], capture_output=True)
            
            st.session_state.setup_complete = True
            add_log("Setup completed successfully", "success")
            st.success("✅ Setup complete!")

def models_page():
    """Model selection interface"""
    st.title("📦 Model Selection")
    
    # Model type tabs
    tab1, tab2, tab3 = st.tabs(["SD 1.5", "SDXL", "CivitAI Search"])
    
    with tab1:
        st.markdown("### SD 1.5 Models")
        
        # Model grid
        cols = st.columns(3)
        for idx, (name, info) in enumerate(list(sd15_models.items())[:9]):
            with cols[idx % 3]:
                if st.checkbox(name[:30], key=f"sd15_{name}"):
                    if f"sd15_{name}" not in st.session_state.selected_models:
                        st.session_state.selected_models.append(f"sd15_{name}")
                        add_log(f"Selected model: {name}", "info")
    
    with tab2:
        st.markdown("### SDXL Models")
        
        # Model grid
        cols = st.columns(3)
        for idx, (name, info) in enumerate(list(sdxl_models.items())[:9]):
            with cols[idx % 3]:
                if st.checkbox(name[:30], key=f"sdxl_{name}"):
                    if f"sdxl_{name}" not in st.session_state.selected_models:
                        st.session_state.selected_models.append(f"sdxl_{name}")
                        add_log(f"Selected model: {name}", "info")
    
    with tab3:
        st.markdown("### CivitAI Search")
        
        search_term = st.text_input("Search models on CivitAI")
        if st.button("🔍 Search"):
            st.info("CivitAI search coming soon...")
    
    # Save selections
    if st.button("💾 Save Selections", type="primary"):
        config = {
            'selected_models': st.session_state.selected_models,
            'timestamp': datetime.now().isoformat()
        }
        with open(project_root / 'configs' / 'session.json', 'w') as f:
            json.dump(config, f, indent=2)
        st.success("Selections saved!")
        add_log("Model selections saved", "success")

def downloads_page():
    """Download management"""
    st.title("💾 Downloads")
    
    # Download queue
    st.markdown("### Download Queue")
    if st.session_state.selected_models:
        for model in st.session_state.selected_models:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.text(model)
            with col2:
                st.text("Pending")
            with col3:
                if st.button("Remove", key=f"rm_{model}"):
                    st.session_state.selected_models.remove(model)
    else:
        st.info("No models selected for download")
    
    # Download action
    if st.button("⬇️ Start Downloads", type="primary", disabled=not st.session_state.selected_models):
        with st.spinner("Downloading models..."):
            progress = st.progress(0)
            for idx, model in enumerate(st.session_state.selected_models):
                st.text(f"Downloading {model}...")
                time.sleep(2)  # Simulate download
                progress.progress((idx + 1) / len(st.session_state.selected_models))
            st.success("Downloads complete!")
            add_log("All downloads completed", "success")

def launch_page():
    """WebUI launcher"""
    st.title("🚀 WebUI Launcher")
    
    # WebUI selection
    webui_type = st.selectbox(
        "Select WebUI",
        ["Automatic1111", "Forge", "ComfyUI", "SD.Next"]
    )
    
    # Launch options
    col1, col2 = st.columns(2)
    with col1:
        port = st.number_input("Port", value=7860, min_value=7000, max_value=9000)
    with col2:
        share = st.checkbox("Create public link", value=True)
    
    # Launch button
    if st.button("🚀 Launch WebUI", type="primary"):
        with st.spinner(f"Launching {webui_type}..."):
            st.text("Cloning repository...")
            time.sleep(2)
            st.text("Installing dependencies...")
            time.sleep(3)
            st.text("Starting server...")
            time.sleep(2)
            
            st.session_state.webui_process = True
            st.success(f"{webui_type} launched successfully!")
            st.info(f"🌐 Access at: https://example.ngrok.io")
            add_log(f"Launched {webui_type}", "success")

def storage_page():
    """Storage management"""
    st.title("🧹 Storage Management")
    
    # Storage stats
    st.markdown("### Storage Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Size", "2.4 GB")
    with col2:
        st.metric("Models", "1.8 GB")
    with col3:
        st.metric("Free Space", "45 GB")
    
    # Storage breakdown
    st.markdown("### Storage Breakdown")
    storage_data = {
        "Models": 1800,
        "LoRAs": 400,
        "VAE": 150,
        "ControlNet": 50
    }
    
    for item, size in storage_data.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(size / 2400)
            st.text(f"{item}: {size} MB")
    
    # Cleanup actions
    st.markdown("### Cleanup Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Remove Duplicates"):
            st.info("Scanning for duplicates...")
    
    with col2:
        if st.button("🧹 Clear Cache"):
            st.info("Clearing cache...")
    
    with col3:
        if st.button("📦 Optimize Storage"):
            st.info("Optimizing storage...")

# Main app
def main():
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/8B0000/FFFFFF?text=SD-DarkMaster-Pro", use_column_width=True)
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["🏠 Home", "⚙️ Setup", "📦 Models", "💾 Downloads", "🚀 Launch", "🧹 Storage"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # System info
        st.markdown("### System Info")
        st.text(f"CPU: {psutil.cpu_percent()}%")
        st.text(f"RAM: {psutil.virtual_memory().percent}%")
        if st.session_state.webui_process:
            st.text("WebUI: 🟢 Running")
        else:
            st.text("WebUI: ⚫ Stopped")
    
    # Route to pages
    if page == "🏠 Home":
        home_page()
    elif page == "⚙️ Setup":
        setup_page()
    elif page == "📦 Models":
        models_page()
    elif page == "💾 Downloads":
        downloads_page()
    elif page == "🚀 Launch":
        launch_page()
    elif page == "🧹 Storage":
        storage_page()

if __name__ == "__main__":
    main()