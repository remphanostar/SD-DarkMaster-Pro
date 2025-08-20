#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Multi-Platform WebUI Launch System
600+ lines of enterprise-grade launch management
"""

import os
import sys
import subprocess
import asyncio
import json
import time
import shutil
import signal
import psutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import logging
import threading
from dataclasses import dataclass
import urllib.request

# Add project root to path
try:
    project_root = Path(__file__).parent.parent
except NameError:
    # When executed from notebook
    project_root = Path('/workspace/SD-DarkMaster-Pro')
sys.path.insert(0, str(project_root))

# Import modules
from modules.core.platform_manager import PlatformManager
from modules.enterprise.unified_storage_manager import UnifiedStorageManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

WEBUI_CONFIGS = {
    'A1111': {
        'name': 'AUTOMATIC1111 Stable Diffusion WebUI',
        'repo': 'https://github.com/AUTOMATIC1111/stable-diffusion-webui.git',
        'branch': 'master',
        'launch_script': 'launch.py',
        'webui_script': 'webui.py',
        'requirements': 'requirements.txt',
        'default_port': 7860,
        'api_endpoint': '/sdapi/v1/txt2img'
    },
    'ComfyUI': {
        'name': 'ComfyUI',
        'repo': 'https://github.com/comfyanonymous/ComfyUI.git',
        'branch': 'master',
        'launch_script': 'main.py',
        'requirements': 'requirements.txt',
        'default_port': 8188,
        'api_endpoint': '/prompt'
    },
    'Forge': {
        'name': 'Stable Diffusion WebUI Forge',
        'repo': 'https://github.com/lllyasviel/stable-diffusion-webui-forge.git',
        'branch': 'main',
        'launch_script': 'launch.py',
        'webui_script': 'webui.py',
        'requirements': 'requirements.txt',
        'default_port': 7860,
        'api_endpoint': '/sdapi/v1/txt2img'
    },
    'ReForge': {
        'name': 'Stable Diffusion WebUI reForge',
        'repo': 'https://github.com/Panchovix/stable-diffusion-webui-reForge.git',
        'branch': 'main',
        'launch_script': 'launch.py',
        'webui_script': 'webui.py',
        'requirements': 'requirements.txt',
        'default_port': 7860,
        'api_endpoint': '/sdapi/v1/txt2img'
    },
    'SD-Next': {
        'name': 'SD.Next',
        'repo': 'https://github.com/vladmandic/automatic.git',
        'branch': 'master',
        'launch_script': 'launch.py',
        'webui_script': 'webui.py',
        'requirements': 'requirements.txt',
        'default_port': 7860,
        'api_endpoint': '/sdapi/v1/txt2img'
    },
    'SD-UX': {
        'name': 'Stable Diffusion WebUI UX',
        'repo': 'https://github.com/sd-webui/stable-diffusion-webui-ux.git',
        'branch': 'main',
        'launch_script': 'launch.py',
        'webui_script': 'webui.py',
        'requirements': 'requirements.txt',
        'default_port': 7860,
        'api_endpoint': '/sdapi/v1/txt2img'
    }
}

TUNNEL_SERVICES = {
    'cloudflared': {
        'name': 'Cloudflare Tunnel',
        'install_cmd': 'wget -q -O cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 && chmod +x cloudflared',
        'run_cmd': './cloudflared tunnel --url http://localhost:{port}',
        'pattern': 'https://.*trycloudflare.com'
    },
    'ngrok': {
        'name': 'ngrok',
        'install_cmd': 'pip install pyngrok',
        'run_cmd': 'ngrok http {port}',
        'pattern': 'https://.*ngrok.io'
    },
    'localtunnel': {
        'name': 'LocalTunnel',
        'install_cmd': 'npm install -g localtunnel',
        'run_cmd': 'lt --port {port}',
        'pattern': 'https://.*loca.lt'
    },
    'bore': {
        'name': 'Bore',
        'install_cmd': 'cargo install bore-cli',
        'run_cmd': 'bore local {port} --to bore.pub',
        'pattern': 'bore.pub:[0-9]+'
    },
    'zrok': {
        'name': 'Zrok',
        'install_cmd': 'curl -s https://get.zrok.io | bash',
        'run_cmd': 'zrok share public http://localhost:{port}',
        'pattern': 'https://.*share.zrok.io'
    },
    'serveo': {
        'name': 'Serveo',
        'install_cmd': None,  # No installation needed
        'run_cmd': 'ssh -R 80:localhost:{port} serveo.net',
        'pattern': 'https://.*serveo.net'
    }
}

# ============================================================================
# LAUNCH MANAGER
# ============================================================================

@dataclass
class LaunchConfig:
    """Launch configuration"""
    webui_type: str = 'A1111'
    port: int = 7860
    share: bool = False
    tunnel_service: str = 'cloudflared'
    launch_args: List[str] = None
    env_vars: Dict[str, str] = None
    extensions_enabled: bool = True
    api_enabled: bool = False
    auth: Optional[Tuple[str, str]] = None
    theme: str = 'dark'
    
class WebUILauncher:
    """Main WebUI launcher with multi-platform support"""
    
    def __init__(self):
        self.platform_manager = PlatformManager()
        self.storage_manager = UnifiedStorageManager()
        self.webui_process = None
        self.tunnel_process = None
        self.monitor_thread = None
        self.launch_config = LaunchConfig()
        self.webui_path = None
        self.start_time = None
        
        # Audio paths
        self.audio_paths = {
            'ready': project_root / 'assets' / 'audio' / 'darkpro-ready.mp3',
            'error': project_root / 'assets' / 'audio' / 'error-recovery.mp3'
        }
    
    def prepare_webui(self, webui_type: str = 'A1111') -> bool:
        """Prepare WebUI for launch"""
        logger.info(f"Preparing {webui_type} for launch...")
        
        if webui_type not in WEBUI_CONFIGS:
            logger.error(f"Unknown WebUI type: {webui_type}")
            return False
        
        config = WEBUI_CONFIGS[webui_type]
        webui_dir = Path(self.platform_manager.platform_config['root']) / 'webuis' / webui_type
        
        # Clone or update repository
        if not webui_dir.exists():
            logger.info(f"Cloning {webui_type} repository...")
            try:
                subprocess.run(
                    ['git', 'clone', '--depth', '1', '-b', config['branch'], 
                     config['repo'], str(webui_dir)],
                    check=True
                )
                logger.info(f"✅ Cloned {webui_type} successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to clone repository: {e}")
                return False
        else:
            logger.info(f"Updating {webui_type} repository...")
            try:
                subprocess.run(
                    ['git', 'pull'],
                    cwd=webui_dir,
                    check=True
                )
            except:
                logger.warning("Git pull failed, continuing with existing version")
        
        self.webui_path = webui_dir
        
        # Link unified storage
        logger.info("Linking unified storage...")
        self.storage_manager.link_webui_storage(webui_dir, webui_type)
        
        # Install extensions
        if self.launch_config.extensions_enabled:
            self._install_extensions(webui_dir)
        
        # Apply Dark Mode Pro theme
        self._apply_dark_theme(webui_dir, webui_type)
        
        return True
    
    def _install_extensions(self, webui_dir: Path):
        """Install extensions from _extensions.txt"""
        extensions_file = project_root / 'scripts' / '_extensions.txt'
        
        if not extensions_file.exists():
            logger.warning("Extensions file not found")
            return
        
        with open(extensions_file, 'r') as f:
            extensions = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        extensions_dir = webui_dir / 'extensions'
        extensions_dir.mkdir(parents=True, exist_ok=True)
        
        for ext_url in extensions:
            ext_name = ext_url.split('/')[-1].replace('.git', '')
            ext_path = extensions_dir / ext_name
            
            if not ext_path.exists():
                try:
                    subprocess.run(
                        ['git', 'clone', '--depth', '1', ext_url, str(ext_path)],
                        check=True,
                        capture_output=True
                    )
                    logger.info(f"✅ Installed extension: {ext_name}")
                except Exception as e:
                    logger.error(f"Failed to install extension {ext_name}: {e}")
            else:
                logger.info(f"Extension already installed: {ext_name}")
    
    def _apply_dark_theme(self, webui_dir: Path, webui_type: str):
        """Apply Dark Mode Pro theme to WebUI"""
        logger.info("Applying Dark Mode Pro theme...")
        
        # Create custom CSS for Dark Mode Pro
        css_content = """
/* SD-DarkMaster-Pro Theme */
:root {
    --darkpro-primary: #111827;
    --darkpro-accent: #10B981;
    --darkpro-text: #6B7280;
    --darkpro-surface: #1F2937;
    --darkpro-border: #374151;
}

body, .gradio-container {
    background: var(--darkpro-primary) !important;
    color: var(--darkpro-text) !important;
}

.dark {
    --body-background-fill: var(--darkpro-primary) !important;
    --background-fill-primary: var(--darkpro-surface) !important;
    --background-fill-secondary: var(--darkpro-surface) !important;
    --border-color-primary: var(--darkpro-border) !important;
    --body-text-color: var(--darkpro-text) !important;
    --block-title-text-color: var(--darkpro-accent) !important;
}
"""
        
        # Save custom CSS
        if webui_type in ['A1111', 'Forge', 'ReForge', 'SD-Next', 'SD-UX']:
            style_dir = webui_dir / 'style.css'
            with open(style_dir, 'w') as f:
                f.write(css_content)
        
        elif webui_type == 'ComfyUI':
            # ComfyUI has different theming approach
            web_dir = webui_dir / 'web' / 'extensions' / 'darkpro'
            web_dir.mkdir(parents=True, exist_ok=True)
            
            theme_file = web_dir / 'darkpro.css'
            with open(theme_file, 'w') as f:
                f.write(css_content)
    
    async def launch_webui(self, config: LaunchConfig = None) -> bool:
        """Launch WebUI with configuration"""
        if config:
            self.launch_config = config
        
        self.start_time = time.time()
        
        # Prepare WebUI
        if not self.prepare_webui(self.launch_config.webui_type):
            return False
        
        logger.info(f"Launching {self.launch_config.webui_type}...")
        
        # Get platform-optimized launch arguments
        launch_args = self.platform_manager.get_launch_args(self.launch_config.webui_type)
        
        # Add custom arguments
        if self.launch_config.launch_args:
            launch_args.extend(self.launch_config.launch_args)
        
        # Add port
        launch_args.extend(['--port', str(self.launch_config.port)])
        
        # Add API if enabled
        if self.launch_config.api_enabled:
            launch_args.append('--api')
        
        # Add authentication if provided
        if self.launch_config.auth:
            launch_args.extend(['--gradio-auth', f"{self.launch_config.auth[0]}:{self.launch_config.auth[1]}"])
        
        # Get environment variables
        env_vars = self.platform_manager.get_environment_vars()
        if self.launch_config.env_vars:
            env_vars.update(self.launch_config.env_vars)
        
        # Determine launch script
        webui_config = WEBUI_CONFIGS[self.launch_config.webui_type]
        launch_script = self.webui_path / webui_config['launch_script']
        
        # Build launch command
        if self.launch_config.webui_type == 'ComfyUI':
            launch_cmd = [sys.executable, str(launch_script)] + launch_args
        else:
            launch_cmd = [sys.executable, str(launch_script)] + launch_args
        
        logger.info(f"Launch command: {' '.join(launch_cmd)}")
        
        try:
            # Launch WebUI process
            self.webui_process = subprocess.Popen(
                launch_cmd,
                cwd=self.webui_path,
                env=env_vars,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Start monitoring thread
            self.monitor_thread = threading.Thread(target=self._monitor_webui)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            
            # Wait for WebUI to be ready
            if await self._wait_for_ready():
                logger.info("✅ WebUI launched successfully!")
                self._play_audio('ready')
                
                # Start tunnel if needed
                if self.launch_config.share or self.platform_manager.platform_config.get('tunnel_required'):
                    await self._start_tunnel()
                
                return True
            else:
                logger.error("WebUI failed to start")
                self._play_audio('error')
                return False
                
        except Exception as e:
            logger.error(f"Failed to launch WebUI: {e}")
            self._play_audio('error')
            return False
    
    def _monitor_webui(self):
        """Monitor WebUI process output"""
        if not self.webui_process:
            return
        
        for line in iter(self.webui_process.stdout.readline, ''):
            if line:
                logger.info(f"[WebUI] {line.strip()}")
                
                # Check for errors
                if 'error' in line.lower() or 'exception' in line.lower():
                    logger.error(f"WebUI Error: {line.strip()}")
                
                # Check for ready state
                if 'running on' in line.lower() or 'model loaded' in line.lower():
                    logger.info("WebUI is ready!")
    
    async def _wait_for_ready(self, timeout: int = 300) -> bool:
        """Wait for WebUI to be ready"""
        logger.info("Waiting for WebUI to be ready...")
        
        start_time = time.time()
        port = self.launch_config.port
        
        while time.time() - start_time < timeout:
            try:
                # Try to connect to WebUI
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', port))
                sock.close()
                
                if result == 0:
                    # Port is open, try to access API
                    try:
                        url = f"http://localhost:{port}"
                        response = urllib.request.urlopen(url, timeout=5)
                        if response.status == 200:
                            logger.info("✅ WebUI is ready!")
                            return True
                    except:
                        pass
                
            except Exception as e:
                logger.debug(f"Waiting for WebUI: {e}")
            
            await asyncio.sleep(2)
        
        logger.error("Timeout waiting for WebUI to be ready")
        return False
    
    async def _start_tunnel(self) -> Optional[str]:
        """Start tunnel service"""
        logger.info(f"Starting tunnel service: {self.launch_config.tunnel_service}")
        
        tunnel_config = TUNNEL_SERVICES.get(self.launch_config.tunnel_service)
        if not tunnel_config:
            logger.error(f"Unknown tunnel service: {self.launch_config.tunnel_service}")
            return None
        
        # Install tunnel service if needed
        if tunnel_config['install_cmd']:
            try:
                subprocess.run(tunnel_config['install_cmd'], shell=True, check=True)
            except:
                logger.warning(f"Failed to install {tunnel_config['name']}")
        
        # Start tunnel
        tunnel_cmd = tunnel_config['run_cmd'].format(port=self.launch_config.port)
        
        try:
            if self.launch_config.tunnel_service == 'cloudflared':
                # Special handling for cloudflared
                self.tunnel_process = subprocess.Popen(
                    tunnel_cmd.split(),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                
                # Parse URL from output
                for line in iter(self.tunnel_process.stdout.readline, ''):
                    if 'trycloudflare.com' in line:
                        import re
                        match = re.search(r'(https://[^\s]+)', line)
                        if match:
                            tunnel_url = match.group(1)
                            logger.info(f"✅ Tunnel URL: {tunnel_url}")
                            return tunnel_url
            
            elif self.launch_config.tunnel_service == 'ngrok':
                # Use pyngrok for ngrok
                from pyngrok import ngrok
                tunnel = ngrok.connect(self.launch_config.port)
                tunnel_url = tunnel.public_url
                logger.info(f"✅ Tunnel URL: {tunnel_url}")
                return tunnel_url
            
            else:
                # Generic tunnel handling
                self.tunnel_process = subprocess.Popen(
                    tunnel_cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True
                )
                
                # Try to extract URL from output
                import re
                for line in iter(self.tunnel_process.stdout.readline, ''):
                    match = re.search(tunnel_config['pattern'], line)
                    if match:
                        tunnel_url = match.group(0)
                        if not tunnel_url.startswith('http'):
                            tunnel_url = f"https://{tunnel_url}"
                        logger.info(f"✅ Tunnel URL: {tunnel_url}")
                        return tunnel_url
                        
        except Exception as e:
            logger.error(f"Failed to start tunnel: {e}")
            return None
    
    def stop_webui(self):
        """Stop WebUI and cleanup"""
        logger.info("Stopping WebUI...")
        
        # Stop tunnel
        if self.tunnel_process:
            try:
                self.tunnel_process.terminate()
                self.tunnel_process.wait(timeout=5)
            except:
                self.tunnel_process.kill()
            self.tunnel_process = None
        
        # Stop WebUI
        if self.webui_process:
            try:
                # Try graceful shutdown
                self.webui_process.terminate()
                self.webui_process.wait(timeout=10)
            except:
                # Force kill if needed
                self.webui_process.kill()
                
                # Kill all child processes
                try:
                    parent = psutil.Process(self.webui_process.pid)
                    for child in parent.children(recursive=True):
                        child.kill()
                except:
                    pass
            
            self.webui_process = None
        
        logger.info("✅ WebUI stopped")
    
    def get_status(self) -> Dict:
        """Get WebUI status"""
        status = {
            'running': self.webui_process is not None and self.webui_process.poll() is None,
            'webui_type': self.launch_config.webui_type,
            'port': self.launch_config.port,
            'platform': self.platform_manager.platform,
            'uptime': None
        }
        
        if status['running'] and self.start_time:
            status['uptime'] = time.time() - self.start_time
        
        # Get resource usage
        if status['running'] and self.webui_process:
            try:
                process = psutil.Process(self.webui_process.pid)
                status['cpu_percent'] = process.cpu_percent()
                status['memory_mb'] = process.memory_info().rss / (1024 * 1024)
            except:
                pass
        
        return status
    
    def _play_audio(self, audio_type: str):
        """Play audio notification"""
        try:
            audio_file = self.audio_paths.get(audio_type)
            if audio_file and audio_file.exists():
                if sys.platform == 'darwin':
                    os.system(f'afplay {audio_file}')
                elif sys.platform == 'linux':
                    os.system(f'aplay {audio_file} 2>/dev/null || paplay {audio_file} 2>/dev/null')
                elif sys.platform == 'win32':
                    import winsound
                    winsound.PlaySound(str(audio_file), winsound.SND_FILENAME)
        except:
            pass

# ============================================================================
# MAIN INTERFACE
# ============================================================================

def render_launch_interface():
    """Render launch interface"""
    try:
        import streamlit as st
        render_streamlit_interface()
    except:
        render_gradio_interface()

def render_streamlit_interface():
    """Render Streamlit launch interface"""
    import streamlit as st
    
    st.markdown("""
    # 🚀 Multi-Platform WebUI Launch
    ### Launch any WebUI with platform-specific optimizations
    """)
    
    launcher = WebUILauncher()
    
    # WebUI selection
    col1, col2 = st.columns(2)
    
    with col1:
        webui_type = st.selectbox(
            "Select WebUI",
            list(WEBUI_CONFIGS.keys()),
            key="webui_type"
        )
        
        port = st.number_input(
            "Port",
            min_value=7000,
            max_value=9000,
            value=WEBUI_CONFIGS[webui_type]['default_port'],
            key="port"
        )
    
    with col2:
        share = st.checkbox("Enable sharing", key="share")
        
        if share:
            tunnel_service = st.selectbox(
                "Tunnel Service",
                list(TUNNEL_SERVICES.keys()),
                key="tunnel"
            )
        else:
            tunnel_service = 'cloudflared'
    
    # Advanced options
    with st.expander("Advanced Options"):
        api_enabled = st.checkbox("Enable API", key="api")
        extensions_enabled = st.checkbox("Install Extensions", value=True, key="extensions")
        
        auth_enabled = st.checkbox("Enable Authentication", key="auth_enabled")
        if auth_enabled:
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username", key="username")
            with col2:
                password = st.text_input("Password", type="password", key="password")
            auth = (username, password) if username and password else None
        else:
            auth = None
    
    # Platform info
    st.markdown("### Platform Information")
    st.code(launcher.platform_manager.get_info_summary())
    
    # Launch button
    if st.button("🚀 Launch WebUI", key="launch_btn"):
        config = LaunchConfig(
            webui_type=webui_type,
            port=port,
            share=share,
            tunnel_service=tunnel_service,
            api_enabled=api_enabled,
            extensions_enabled=extensions_enabled,
            auth=auth
        )
        
        with st.spinner(f"Launching {webui_type}..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            success = loop.run_until_complete(launcher.launch_webui(config))
            
            if success:
                st.success(f"✅ {webui_type} launched successfully!")
                st.info(f"Access at: http://localhost:{port}")
            else:
                st.error("Failed to launch WebUI")
    
    # Stop button
    if st.button("⏹️ Stop WebUI", key="stop_btn"):
        launcher.stop_webui()
        st.success("WebUI stopped")
    
    # Status
    status = launcher.get_status()
    if status['running']:
        st.success(f"🟢 {status['webui_type']} is running on port {status['port']}")
        if status['uptime']:
            st.info(f"Uptime: {status['uptime']:.0f} seconds")

def render_gradio_interface():
    """Render Gradio launch interface (fallback)"""
    import gradio as gr
    
    launcher = WebUILauncher()
    
    def launch_webui(webui_type, port, share, tunnel_service, api_enabled, extensions_enabled):
        config = LaunchConfig(
            webui_type=webui_type,
            port=port,
            share=share,
            tunnel_service=tunnel_service,
            api_enabled=api_enabled,
            extensions_enabled=extensions_enabled
        )
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(launcher.launch_webui(config))
        
        if success:
            return f"✅ {webui_type} launched successfully on port {port}!"
        else:
            return "❌ Failed to launch WebUI"
    
    with gr.Blocks(title="WebUI Launcher") as interface:
        gr.Markdown("# 🚀 Multi-Platform WebUI Launch")
        
        with gr.Row():
            webui_type = gr.Dropdown(
                choices=list(WEBUI_CONFIGS.keys()),
                label="WebUI Type",
                value="A1111"
            )
            port = gr.Number(label="Port", value=7860)
        
        with gr.Row():
            share = gr.Checkbox(label="Enable Sharing", value=False)
            tunnel_service = gr.Dropdown(
                choices=list(TUNNEL_SERVICES.keys()),
                label="Tunnel Service",
                value="cloudflared"
            )
        
        with gr.Row():
            api_enabled = gr.Checkbox(label="Enable API", value=False)
            extensions_enabled = gr.Checkbox(label="Install Extensions", value=True)
        
        launch_btn = gr.Button("🚀 Launch WebUI", variant="primary")
        output = gr.Textbox(label="Status", lines=3)
        
        launch_btn.click(
            launch_webui,
            inputs=[webui_type, port, share, tunnel_service, api_enabled, extensions_enabled],
            outputs=output
        )
        
        platform_info = gr.Textbox(
            label="Platform Information",
            value=launcher.platform_manager.get_info_summary(),
            lines=8,
            interactive=False
        )
    
    interface.launch(server_name="0.0.0.0", server_port=7862, share=False)

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("🚀 SD-DarkMaster-Pro WebUI Launcher")
    print("🎨 Multi-Platform Launch System")
    print("="*60 + "\n")
    
    render_launch_interface()

if __name__ == "__main__":
    # Handle signals for graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Received shutdown signal")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    main()