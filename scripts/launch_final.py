#!/usr/bin/env python3
"""
SD-DarkMaster-Pro WebUI Launcher - Final Version
Uses AnxietySolo packages + custom Forge build
"""

import os
import sys
import subprocess
import asyncio
import json
import time
import shutil
import zipfile
import lz4.frame
from pathlib import Path
from typing import Dict, Optional
import urllib.request
from tqdm import tqdm
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

# Add project root to path
try:
    project_root = Path(__file__).parent.parent
except NameError:
    project_root = Path('/workspace/SD-DarkMaster-Pro')
sys.path.insert(0, str(project_root))

# ============================================================================
# PACKAGE CONFIGURATIONS - FINAL VERSION
# ============================================================================

WEBUI_PACKAGES = {
    'ComfyUI': {
        'name': 'ComfyUI (AnxietySolo)',
        'package_url': 'https://huggingface.co/NagisaNao/ANXETY/resolve/main/ComfyUI.zip',
        'venv_name': 'python31018-venv-torch260-cu124',
        'size': '1.04 GB',
        'launch_script': 'main.py',
        'default_port': 8188,
        'ready': True,
        'source': 'anxietysolo'
    },
    'Forge': {
        'name': 'Forge NSFW Maximum (Custom)',
        'package_url': None,  # Will use your custom package
        'package_path': '/workspace/packages/Forge_NSFW_Maximum.zip',  # Local path
        'venv_name': 'python31018-venv-torch260-cu124',  # Same venv
        'size': '~4.5 GB',
        'launch_script': 'launch.py',
        'default_port': 7860,
        'ready': False,  # Until you create it
        'source': 'custom'
    }
}

# Shared venv configuration
SHARED_VENV = {
    'url': 'https://huggingface.co/NagisaNao/ANXETY/resolve/main/python31018-venv-torch260-cu124-C-fca.tar.lz4',
    'name': 'python31018-venv-torch260-cu124',
    'size': '5.22 GB'
}

# ============================================================================
# SIMPLIFIED PACKAGE MANAGER
# ============================================================================

class DarkMasterPackageManager:
    """Manages WebUI packages - AnxietySolo + Custom"""
    
    def __init__(self):
        self.project_root = project_root
        self.packages_dir = self.project_root / 'packages'
        self.webuis_dir = self.project_root / 'webuis'
        self.venv_dir = self.project_root / 'venv'  # Single shared venv
        self.storage_dir = self.project_root / 'storage'
        
        # Create directories
        for dir_path in [self.packages_dir, self.webuis_dir, self.storage_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create storage subdirectories
        for subdir in ['models', 'loras', 'vae', 'embeddings', 'controlnet', 'upscalers']:
            (self.storage_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    def download_with_progress(self, url: str, dest_path: Path, description: str = "Downloading"):
        """Download file with progress bar"""
        
        if dest_path.exists():
            logger.info(f"Using cached: {dest_path.name}")
            return dest_path
        
        logger.info(f"Downloading: {url}")
        
        # Simple download for now (can add progress bar later)
        urllib.request.urlretrieve(url, dest_path)
        logger.info(f"✅ Downloaded: {dest_path.name}")
        return dest_path
    
    def extract_zip(self, zip_path: Path, extract_to: Path):
        """Extract ZIP archive"""
        logger.info(f"Extracting {zip_path.name}...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        logger.info(f"✅ Extracted to {extract_to}")
    
    def extract_lz4(self, lz4_path: Path):
        """Extract LZ4 compressed tar archive to venv directory"""
        logger.info(f"Extracting venv from {lz4_path.name}...")
        
        # Extract using system commands (simpler than Python lz4)
        cmd = f"tar -xf {lz4_path} -C {self.project_root} --use-compress-program=lz4"
        subprocess.run(cmd, shell=True, check=True)
        
        logger.info(f"✅ Venv extracted to {self.venv_dir}")
    
    def setup_shared_venv(self):
        """Download and setup the shared venv if needed"""
        
        # Check if venv already exists
        venv_python = self.venv_dir / 'bin' / 'python'
        if venv_python.exists():
            logger.info("✅ Shared venv already setup")
            return True
        
        # Download venv archive
        venv_archive = self.packages_dir / f"{SHARED_VENV['name']}.tar.lz4"
        
        if not venv_archive.exists():
            logger.info(f"Downloading shared venv ({SHARED_VENV['size']})...")
            self.download_with_progress(
                SHARED_VENV['url'],
                venv_archive,
                "Downloading Python environment"
            )
        
        # Extract venv
        self.extract_lz4(venv_archive)
        
        # Verify it worked
        if venv_python.exists():
            logger.info("✅ Shared venv ready!")
            return True
        else:
            logger.error("Failed to setup venv")
            return False
    
    def link_unified_storage(self, webui_path: Path, webui_type: str):
        """Create symbolic links to unified storage"""
        logger.info("Linking unified storage...")
        
        # Storage mapping
        if webui_type == 'ComfyUI':
            mappings = {
                'models/checkpoints': self.storage_dir / 'models',
                'models/loras': self.storage_dir / 'loras',
                'models/vae': self.storage_dir / 'vae',
                'models/embeddings': self.storage_dir / 'embeddings',
                'models/controlnet': self.storage_dir / 'controlnet',
                'models/upscale_models': self.storage_dir / 'upscalers'
            }
        else:  # Forge
            mappings = {
                'models/Stable-diffusion': self.storage_dir / 'models',
                'models/Lora': self.storage_dir / 'loras',
                'models/VAE': self.storage_dir / 'vae',
                'embeddings': self.storage_dir / 'embeddings',
                'models/ControlNet': self.storage_dir / 'controlnet',
                'models/ESRGAN': self.storage_dir / 'upscalers'
            }
        
        for webui_subpath, storage_path in mappings.items():
            link_path = webui_path / webui_subpath
            
            # Create parent directory if needed
            link_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Remove existing link or directory
            if link_path.exists() or link_path.is_symlink():
                if link_path.is_symlink():
                    link_path.unlink()
                elif link_path.is_dir() and not any(link_path.iterdir()):
                    link_path.rmdir()
            
            # Create symbolic link
            if not link_path.exists():
                link_path.symlink_to(storage_path)
                logger.info(f"  Linked: {webui_subpath} → storage/{storage_path.name}")
    
    def install_webui(self, webui_type: str) -> bool:
        """Install WebUI package"""
        
        config = WEBUI_PACKAGES.get(webui_type)
        if not config:
            logger.error(f"Unknown WebUI type: {webui_type}")
            return False
        
        webui_path = self.webuis_dir / webui_type
        
        # Check if already installed
        if webui_path.exists():
            logger.info(f"{webui_type} already installed at {webui_path}")
            return True
        
        # Setup shared venv first
        if not self.setup_shared_venv():
            return False
        
        logger.info(f"Installing {config['name']}...")
        
        # Determine package source
        if config['source'] == 'anxietysolo':
            # Download from HuggingFace
            package_filename = f"{webui_type}.zip"
            package_path = self.packages_dir / package_filename
            
            if not package_path.exists():
                self.download_with_progress(
                    config['package_url'],
                    package_path,
                    f"Downloading {webui_type} ({config['size']})"
                )
        else:  # custom
            # Use local package
            package_path = Path(config['package_path'])
            if not package_path.exists():
                logger.error(f"Custom package not found: {package_path}")
                logger.info("Please create your Forge package first!")
                return False
        
        # Extract WebUI
        self.extract_zip(package_path, self.webuis_dir)
        
        # Link unified storage
        self.link_unified_storage(webui_path, webui_type)
        
        logger.info(f"✅ {config['name']} installed successfully!")
        return True
    
    def launch_webui(self, webui_type: str, port: Optional[int] = None, 
                    share: bool = False, api: bool = False) -> subprocess.Popen:
        """Launch WebUI using shared venv"""
        
        config = WEBUI_PACKAGES.get(webui_type)
        if not config:
            raise ValueError(f"Unknown WebUI type: {webui_type}")
        
        webui_path = self.webuis_dir / webui_type
        if not webui_path.exists():
            raise FileNotFoundError(f"{webui_type} not installed. Run install first.")
        
        # Use shared venv Python
        venv_python = self.venv_dir / 'bin' / 'python'
        if not venv_python.exists():
            # Windows compatibility
            venv_python = self.venv_dir / 'Scripts' / 'python.exe'
        
        # Build launch command
        cmd = [str(venv_python), config['launch_script']]
        
        # Add port
        if port is None:
            port = config['default_port']
        
        if webui_type == 'ComfyUI':
            cmd.extend(['--port', str(port)])
            if api:
                cmd.append('--enable-cors-header')
        else:  # Forge
            cmd.extend(['--port', str(port)])
            if share:
                cmd.append('--share')
            if api:
                cmd.append('--api')
            # Optimizations for 16GB VRAM
            cmd.extend(['--xformers', '--medvram-sdxl'])
        
        logger.info(f"Launching {config['name']} on port {port}...")
        logger.info(f"Command: {' '.join(cmd)}")
        
        # Launch process
        process = subprocess.Popen(
            cmd,
            cwd=webui_path,
            env={
                **os.environ,
                'CUDA_VISIBLE_DEVICES': '0',
                'PYTORCH_CUDA_ALLOC_CONF': 'max_split_size_mb:512'
            }
        )
        
        logger.info(f"✅ {config['name']} launched! Access at http://localhost:{port}")
        
        return process

# ============================================================================
# MAIN INTERFACE
# ============================================================================

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("🚀 SD-DarkMaster-Pro WebUI Launcher - Final Version")
    print("📦 Using AnxietySolo ComfyUI + Custom Forge")
    print("="*60 + "\n")
    
    manager = DarkMasterPackageManager()
    
    # Show available WebUIs
    print("Available WebUIs:")
    for webui_type, config in WEBUI_PACKAGES.items():
        status = "✅ Ready" if config['ready'] else "⏳ Pending"
        source = f"[{config['source']}]"
        print(f"  {webui_type}: {config['name']} {source} - {status}")
    
    print("\n" + "-"*60 + "\n")
    
    # For testing, install and launch ComfyUI
    print("For testing, you can use ComfyUI now:")
    print("1. Install ComfyUI (AnxietySolo package)")
    print("2. Launch ComfyUI")
    print("\nOnce you create your Forge package:")
    print("3. Place it in /workspace/packages/Forge_NSFW_Maximum.zip")
    print("4. Install and launch Forge")
    
    # Interactive mode
    while True:
        print("\nOptions:")
        print("1. Install ComfyUI (for testing)")
        print("2. Install Forge (need your package)")
        print("3. Launch ComfyUI")
        print("4. Launch Forge")
        print("5. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            if manager.install_webui('ComfyUI'):
                print("✅ ComfyUI ready for testing!")
        
        elif choice == '2':
            if manager.install_webui('Forge'):
                print("✅ Forge ready!")
            else:
                print("⚠️ Create your Forge package first:")
                print("  Place at: /workspace/packages/Forge_NSFW_Maximum.zip")
        
        elif choice == '3':
            try:
                process = manager.launch_webui('ComfyUI')
                print(f"ComfyUI running with PID: {process.pid}")
                print("Press Ctrl+C to stop")
                process.wait()
            except KeyboardInterrupt:
                print("\nStopping ComfyUI...")
                process.terminate()
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '4':
            try:
                process = manager.launch_webui('Forge')
                print(f"Forge running with PID: {process.pid}")
                print("Press Ctrl+C to stop")
                process.wait()
            except KeyboardInterrupt:
                print("\nStopping Forge...")
                process.terminate()
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == '5':
            break

if __name__ == "__main__":
    main()