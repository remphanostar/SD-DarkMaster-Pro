#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Intelligent Downloads & Storage Script
Orchestrates download operations with unified storage management
"""

import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import modules
from modules.enterprise.unified_storage_manager import UnifiedStorageManager
from modules.enterprise.download_manager import DownloadManager, DownloadTask

# Import data sources
from scripts._models_data import model_list as sd15_models
from scripts._xl_models_data import model_list as sdxl_models

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# DOWNLOAD ORCHESTRATOR
# ============================================================================

class DownloadOrchestrator:
    """Main orchestrator for download operations"""
    
    def __init__(self):
        self.storage_manager = UnifiedStorageManager()
        self.download_manager = DownloadManager(self.storage_manager)
        self.session_config = self._load_session_config()
        self.download_history = []
        
        # Initialize storage
        self.storage_manager.initialize_storage()
        
        # Audio notification paths
        self.audio_paths = {
            'start': Path(project_root) / 'assets' / 'audio' / 'download-start.mp3',
            'complete': Path(project_root) / 'assets' / 'audio' / 'download-complete.mp3',
            'error': Path(project_root) / 'assets' / 'audio' / 'error-recovery.mp3'
        }
    
    def _load_session_config(self) -> Dict:
        """Load session configuration"""
        config_file = project_root / 'configs' / 'session.json'
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _play_audio(self, audio_type: str):
        """Play audio notification"""
        try:
            audio_file = self.audio_paths.get(audio_type)
            if audio_file and audio_file.exists():
                # Try different audio playback methods based on platform
                if sys.platform == 'darwin':  # macOS
                    os.system(f'afplay {audio_file}')
                elif sys.platform == 'linux':
                    os.system(f'aplay {audio_file} 2>/dev/null || paplay {audio_file} 2>/dev/null')
                elif sys.platform == 'win32':
                    import winsound
                    winsound.PlaySound(str(audio_file), winsound.SND_FILENAME)
        except Exception as e:
            logger.debug(f"Could not play audio: {e}")
    
    async def download_selected_models(self, selected_models: List[str], model_type: str = "SD1.5"):
        """Download selected models from configuration"""
        logger.info(f"Starting download of {len(selected_models)} models")
        self._play_audio('start')
        
        # Get model data
        model_data = sd15_models if model_type == "SD1.5" else sdxl_models
        
        # Add downloads to queue
        for model_name in selected_models:
            if model_name in model_data:
                model_info = model_data[model_name]
                url = model_info.get('url')
                if url:
                    self.download_manager.add_download(
                        url=url,
                        asset_type='checkpoint',
                        metadata={'model_name': model_name, 'model_type': model_type}
                    )
        
        # Process download queue
        async with self.download_manager as dm:
            # Add progress callback
            dm.add_progress_callback(self._download_progress_callback)
            
            # Process all downloads
            summary = await dm.process_queue()
            
            # Save download history
            self._save_download_history(summary)
            
            # Play completion sound
            if summary['failed'] == 0:
                self._play_audio('complete')
            else:
                self._play_audio('error')
            
            return summary
    
    async def download_from_civitai(self, civitai_urls: List[str]):
        """Download models from CivitAI"""
        logger.info(f"Downloading {len(civitai_urls)} models from CivitAI")
        
        for url in civitai_urls:
            # Determine asset type from URL or metadata
            asset_type = self._determine_asset_type(url)
            
            self.download_manager.add_download(
                url=url,
                asset_type=asset_type,
                metadata={'source': 'civitai'}
            )
        
        async with self.download_manager as dm:
            summary = await dm.process_queue()
            return summary
    
    async def download_loras(self, lora_urls: List[str]):
        """Download LoRA models"""
        logger.info(f"Downloading {len(lora_urls)} LoRA models")
        
        for url in lora_urls:
            self.download_manager.add_download(
                url=url,
                asset_type='lora',
                metadata={'type': 'lora'}
            )
        
        async with self.download_manager as dm:
            summary = await dm.process_queue()
            return summary
    
    async def download_extensions(self):
        """Download and install extensions from _extensions.txt"""
        extensions_file = project_root / 'scripts' / '_extensions.txt'
        
        if not extensions_file.exists():
            logger.warning("Extensions file not found")
            return
        
        with open(extensions_file, 'r') as f:
            extensions = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        logger.info(f"Installing {len(extensions)} extensions")
        
        # Extensions are git repositories, clone them
        extensions_dir = self.storage_manager.get_storage_path('configs', 'webui') / 'extensions'
        extensions_dir.mkdir(parents=True, exist_ok=True)
        
        for ext_url in extensions:
            ext_name = ext_url.split('/')[-1].replace('.git', '')
            ext_path = extensions_dir / ext_name
            
            if not ext_path.exists():
                try:
                    process = await asyncio.create_subprocess_exec(
                        'git', 'clone', ext_url, str(ext_path),
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    await process.communicate()
                    logger.info(f"Installed extension: {ext_name}")
                except Exception as e:
                    logger.error(f"Failed to install extension {ext_name}: {e}")
            else:
                logger.info(f"Extension already installed: {ext_name}")
    
    def _determine_asset_type(self, url: str) -> str:
        """Determine asset type from URL"""
        url_lower = url.lower()
        
        if 'lora' in url_lower or 'lycoris' in url_lower:
            return 'lora'
        elif 'vae' in url_lower:
            return 'vae'
        elif 'embedding' in url_lower or 'textual' in url_lower:
            return 'embedding'
        elif 'controlnet' in url_lower:
            return 'controlnet'
        elif 'upscaler' in url_lower or 'esrgan' in url_lower:
            return 'upscaler'
        else:
            return 'checkpoint'
    
    def _download_progress_callback(self, task: DownloadTask):
        """Callback for download progress updates"""
        # This can be used to update UI or send websocket updates
        logger.debug(f"Download progress: {task.filename} - {task.progress:.1f}%")
    
    def _save_download_history(self, summary: Dict):
        """Save download history to file"""
        history_file = project_root / 'configs' / 'download_history.json'
        
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'summary': summary,
            'downloads': [
                {
                    'filename': task.filename,
                    'url': task.url,
                    'status': task.status,
                    'size': task.expected_size,
                    'duration': (task.end_time - task.start_time) if task.end_time and task.start_time else None
                }
                for task in self.download_manager.completed_downloads
            ]
        }
        
        # Load existing history
        if history_file.exists():
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []
        
        # Add new entry
        history.append(history_entry)
        
        # Save updated history
        history_file.parent.mkdir(parents=True, exist_ok=True)
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def get_storage_report(self) -> Dict:
        """Get comprehensive storage report"""
        usage = self.storage_manager.get_storage_usage()
        stats = self.download_manager.get_download_stats()
        
        report = {
            'storage_usage': usage,
            'download_stats': stats,
            'total_storage_gb': sum(
                cat.get('size_gb', 0) if isinstance(cat, dict) and 'size_gb' in cat
                else sum(subcat.get('size_gb', 0) for subcat in cat.values()) if isinstance(cat, dict)
                else 0
                for cat in usage.values()
            )
        }
        
        return report

# ============================================================================
# UI INTERFACE
# ============================================================================

class DownloadInterface:
    """Interface for download operations"""
    
    def __init__(self):
        self.orchestrator = DownloadOrchestrator()
        self.framework = self._detect_framework()
    
    def _detect_framework(self) -> str:
        """Detect UI framework"""
        try:
            import streamlit as st
            if hasattr(st, 'runtime'):
                return 'streamlit'
        except:
            pass
        return 'gradio'
    
    def render_interface(self):
        """Render download interface"""
        if self.framework == 'streamlit':
            self._render_streamlit_interface()
        else:
            self._render_gradio_interface()
    
    def _render_streamlit_interface(self):
        """Render Streamlit download interface"""
        import streamlit as st
        
        st.markdown("""
        # 📦 Intelligent Downloads & Storage
        ### Unified storage management with progress tracking
        """)
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📥 Download Queue",
            "📊 Storage Overview",
            "🔧 Extensions",
            "📜 History"
        ])
        
        with tab1:
            self._render_download_queue()
        
        with tab2:
            self._render_storage_overview()
        
        with tab3:
            self._render_extensions_manager()
        
        with tab4:
            self._render_download_history()
    
    def _render_download_queue(self):
        """Render download queue interface"""
        import streamlit as st
        
        st.markdown("### Download Queue")
        
        # Get selected models from session
        selected_models = st.session_state.get('selected_models', [])
        selected_loras = st.session_state.get('selected_loras', [])
        civitai_downloads = st.session_state.get('civitai_downloads', [])
        
        # Display queue
        total_items = len(selected_models) + len(selected_loras) + len(civitai_downloads)
        
        if total_items > 0:
            st.info(f"📦 Total items in queue: {total_items}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Models", len(selected_models))
            with col2:
                st.metric("LoRAs", len(selected_loras))
            with col3:
                st.metric("CivitAI", len(civitai_downloads))
            
            # Download button
            if st.button("🚀 Start Downloads", key="start_downloads"):
                with st.spinner("Downloading..."):
                    # Run async downloads
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    # Download models
                    if selected_models:
                        model_summary = loop.run_until_complete(
                            self.orchestrator.download_selected_models(selected_models)
                        )
                        st.success(f"✅ Downloaded {model_summary['completed']} models")
                    
                    # Download LoRAs
                    if selected_loras:
                        # Convert LoRA names to URLs (would need actual URLs)
                        lora_urls = []  # Would get actual URLs
                        if lora_urls:
                            lora_summary = loop.run_until_complete(
                                self.orchestrator.download_loras(lora_urls)
                            )
                            st.success(f"✅ Downloaded {lora_summary['completed']} LoRAs")
                    
                    # Download from CivitAI
                    if civitai_downloads:
                        civitai_summary = loop.run_until_complete(
                            self.orchestrator.download_from_civitai(civitai_downloads)
                        )
                        st.success(f"✅ Downloaded {civitai_summary['completed']} from CivitAI")
        else:
            st.warning("No items in download queue. Select models from the Models or CivitAI tabs.")
    
    def _render_storage_overview(self):
        """Render storage overview"""
        import streamlit as st
        import plotly.express as px
        import pandas as pd
        
        st.markdown("### Storage Overview")
        
        # Get storage report
        report = self.orchestrator.get_storage_report()
        
        # Display total storage
        total_gb = report.get('total_storage_gb', 0)
        st.metric("Total Storage Used", f"{total_gb:.2f} GB")
        
        # Create storage breakdown chart
        usage_data = []
        for category, data in report['storage_usage'].items():
            if isinstance(data, dict):
                if 'size_gb' in data:
                    usage_data.append({
                        'Category': category,
                        'Size (GB)': data['size_gb'],
                        'Files': data.get('file_count', 0)
                    })
                else:
                    for subcat, subdata in data.items():
                        usage_data.append({
                            'Category': f"{category}/{subcat}",
                            'Size (GB)': subdata.get('size_gb', 0),
                            'Files': subdata.get('file_count', 0)
                        })
        
        if usage_data:
            df = pd.DataFrame(usage_data)
            
            # Pie chart for storage distribution
            fig = px.pie(df, values='Size (GB)', names='Category', 
                        title='Storage Distribution',
                        color_discrete_sequence=['#10B981', '#059669', '#047857', '#065F46'])
            st.plotly_chart(fig)
            
            # Table view
            st.dataframe(df, use_container_width=True)
        
        # Cleanup options
        st.markdown("### Storage Management")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Find Duplicates"):
                with st.spinner("Scanning for duplicates..."):
                    duplicates = self.orchestrator.storage_manager.cleanup_duplicates()
                    st.success(f"Removed {duplicates} duplicate files")
        
        with col2:
            if st.button("🧹 Clean Cache"):
                st.warning("Cache cleanup will remove temporary files")
    
    def _render_extensions_manager(self):
        """Render extensions manager"""
        import streamlit as st
        
        st.markdown("### Extension Management")
        
        if st.button("📦 Install All Extensions"):
            with st.spinner("Installing extensions..."):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.orchestrator.download_extensions())
                st.success("✅ All extensions installed")
        
        # Display installed extensions
        extensions_dir = self.orchestrator.storage_manager.get_storage_path('configs', 'webui') / 'extensions'
        if extensions_dir.exists():
            installed = [d.name for d in extensions_dir.iterdir() if d.is_dir()]
            if installed:
                st.markdown("#### Installed Extensions")
                for ext in installed:
                    st.text(f"✅ {ext}")
    
    def _render_download_history(self):
        """Render download history"""
        import streamlit as st
        
        st.markdown("### Download History")
        
        history_file = Path(project_root) / 'configs' / 'download_history.json'
        
        if history_file.exists():
            with open(history_file, 'r') as f:
                history = json.load(f)
            
            if history:
                # Display recent downloads
                for entry in history[-5:]:  # Last 5 sessions
                    with st.expander(f"Session: {entry['timestamp']}"):
                        summary = entry['summary']
                        st.json(summary)
                        
                        if 'downloads' in entry:
                            st.markdown("#### Downloaded Files")
                            for dl in entry['downloads']:
                                status_icon = "✅" if dl['status'] == 'completed' else "❌"
                                st.text(f"{status_icon} {dl['filename']}")
        else:
            st.info("No download history available")
    
    def _render_gradio_interface(self):
        """Render Gradio download interface (fallback)"""
        import gradio as gr
        
        with gr.Blocks(title="Downloads & Storage") as interface:
            gr.Markdown("""
            # 📦 Intelligent Downloads & Storage
            ### Unified storage management
            """)
            
            with gr.Tabs():
                with gr.TabItem("Download Queue"):
                    download_btn = gr.Button("Start Downloads", variant="primary")
                    download_output = gr.Textbox(label="Download Status", lines=10)
                    
                    def process_downloads():
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        # Get selections from session/config
                        selected_models = []  # Would get from config
                        
                        if selected_models:
                            summary = loop.run_until_complete(
                                self.orchestrator.download_selected_models(selected_models)
                            )
                            return f"Downloaded: {summary}"
                        return "No items in queue"
                    
                    download_btn.click(process_downloads, outputs=download_output)
                
                with gr.TabItem("Storage"):
                    storage_info = gr.JSON(
                        value=self.orchestrator.get_storage_report(),
                        label="Storage Report"
                    )
                    refresh_btn = gr.Button("Refresh")
                    refresh_btn.click(
                        lambda: self.orchestrator.get_storage_report(),
                        outputs=storage_info
                    )
                
                with gr.TabItem("Extensions"):
                    install_ext_btn = gr.Button("Install Extensions")
                    ext_output = gr.Textbox(label="Installation Status", lines=5)
                    
                    def install_extensions():
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(self.orchestrator.download_extensions())
                        return "Extensions installed successfully"
                    
                    install_ext_btn.click(install_extensions, outputs=ext_output)
        
        interface.launch(server_name="0.0.0.0", server_port=7861, share=False)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("📦 SD-DarkMaster-Pro Download Manager")
    print("🎨 Unified Storage & Intelligent Downloads")
    print("="*60 + "\n")
    
    # Initialize and render interface
    interface = DownloadInterface()
    interface.render_interface()

if __name__ == "__main__":
    main()