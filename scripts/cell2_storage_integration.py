#!/usr/bin/env python3
"""
Cell 2 Storage Integration - Ties central storage into the main workflow
Called by widgets-en.py to ensure models are ready before WebUI launch
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

# Import our central storage manager
sys.path.insert(0, str(Path(__file__).parent))
from setup_central_storage import CentralStorageManager, MODEL_REGISTRY, EXTENSION_MODEL_MAP

# ============================================================================
# CELL 2 INTEGRATION MANAGER
# ============================================================================

class Cell2StorageIntegration:
    """Manages storage operations for Cell 2 (Config UI)"""
    
    def __init__(self):
        self.project_root = Path('/workspace/SD-DarkMaster-Pro')
        self.storage_root = self.project_root / 'storage'
        self.packages_dir = self.project_root / 'packages'
        self.webuis_dir = self.project_root / 'webuis'
        
        # Track what's ready
        self.status = {
            'comfyui_ready': False,
            'forge_ready': False,
            'venv_ready': False,
            'models_ready': {},
            'extensions_ready': {}
        }
        
        # Initialize central storage manager
        self.storage_manager = None
        
    def check_package_status(self) -> Dict[str, bool]:
        """Check which packages are available"""
        
        status = {}
        
        # Check ComfyUI package
        comfy_package = self.packages_dir / 'ComfyUI.zip'
        comfy_extracted = self.webuis_dir / 'ComfyUI'
        status['comfyui_package'] = comfy_package.exists()
        status['comfyui_extracted'] = comfy_extracted.exists()
        
        # Check Forge package
        forge_package = self.packages_dir / 'Forge_NSFW_Maximum.zip'
        forge_extracted = self.webuis_dir / 'Forge'
        status['forge_package'] = forge_package.exists()
        status['forge_extracted'] = forge_extracted.exists()
        
        # Check venv
        venv_path = Path('/workspace/venv')
        status['venv_ready'] = venv_path.exists()
        
        # Check venv archive
        venv_archive = self.packages_dir / 'python31018-venv-torch260-cu124-C-fca.tar.lz4'
        status['venv_archive'] = venv_archive.exists()
        
        return status
    
    def setup_webui_storage(self, webui_type: str) -> bool:
        """Setup central storage for a specific WebUI"""
        
        logger.info(f"Setting up storage for {webui_type}...")
        
        webui_root = self.webuis_dir / webui_type
        if not webui_root.exists():
            logger.error(f"WebUI not found: {webui_root}")
            return False
        
        # Initialize storage manager for this WebUI
        self.storage_manager = CentralStorageManager(
            storage_root=self.storage_root,
            webui_root=webui_root
        )
        
        # Setup extensions based on WebUI type
        if webui_type == 'Forge':
            return self._setup_forge_storage()
        elif webui_type == 'ComfyUI':
            return self._setup_comfyui_storage()
        else:
            logger.warning(f"Unknown WebUI type: {webui_type}")
            return False
    
    def _setup_forge_storage(self) -> bool:
        """Setup storage for Forge with all extensions"""
        
        logger.info("🔧 Setting up Forge central storage...")
        
        # List of extensions that need models
        model_extensions = [
            'sd-webui-segment-anything',
            'sd-webui-inpaint-anything', 
            'sd-webui-replacer',
            'adetailer',
            'sd-webui-controlnet',
            'sd-webui-reactor-Nsfw_freedom'
        ]
        
        success_count = 0
        for ext_name in model_extensions:
            if self.storage_manager.setup_extension(ext_name):
                success_count += 1
                self.status['extensions_ready'][ext_name] = True
        
        logger.info(f"✅ Set up {success_count}/{len(model_extensions)} extensions")
        
        # Download essential models if not present
        self._ensure_essential_models()
        
        return success_count > 0
    
    def _setup_comfyui_storage(self) -> bool:
        """Setup storage for ComfyUI"""
        
        logger.info("🔧 Setting up ComfyUI central storage...")
        
        # ComfyUI has different structure
        comfy_models = self.webuis_dir / 'ComfyUI' / 'models'
        
        # Create symlinks to central storage
        model_mappings = {
            'checkpoints': self.storage_root / 'models',
            'loras': self.storage_root / 'loras',
            'vae': self.storage_root / 'vae',
            'controlnet': self.storage_root / 'controlnet',
            'upscale_models': self.storage_root / 'upscalers'
        }
        
        for comfy_dir, storage_dir in model_mappings.items():
            comfy_path = comfy_models / comfy_dir
            if comfy_path.exists() and not comfy_path.is_symlink():
                # Backup existing
                backup = comfy_path.with_suffix('.backup')
                if not backup.exists():
                    comfy_path.rename(backup)
            
            # Create symlink
            if not comfy_path.exists():
                storage_dir.mkdir(parents=True, exist_ok=True)
                comfy_path.symlink_to(storage_dir)
                logger.info(f"Linked {comfy_dir} → {storage_dir}")
        
        return True
    
    def _ensure_essential_models(self):
        """Download essential models if not present"""
        
        essential_checks = {
            'sam': self.storage_root / 'sam' / 'sam_vit_b_01ec64.pth',
            'adetailer_face': self.storage_root / 'adetailer' / 'face_yolov8n.pt',
            'adetailer_person': self.storage_root / 'adetailer' / 'person_yolov8n-seg.pt'
        }
        
        missing = [name for name, path in essential_checks.items() if not path.exists()]
        
        if missing:
            logger.info(f"📥 Downloading {len(missing)} essential models...")
            self.storage_manager.download_essential_models()
            
            # Update status
            for name in missing:
                self.status['models_ready'][name] = True
    
    def prepare_for_launch(self, webui_type: str, selected_models: List[str] = None) -> Tuple[bool, str]:
        """
        Prepare everything needed before launching a WebUI
        Returns: (success, message)
        """
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Preparing {webui_type} for launch...")
        logger.info(f"{'='*60}")
        
        # Check package status
        pkg_status = self.check_package_status()
        
        # Handle venv
        if not pkg_status['venv_ready'] and pkg_status['venv_archive']:
            logger.info("📦 Extracting shared venv...")
            if not self._extract_venv():
                return False, "Failed to extract venv"
        
        # Handle WebUI package
        if webui_type == 'ComfyUI':
            if not pkg_status['comfyui_extracted']:
                if not pkg_status['comfyui_package']:
                    return False, "ComfyUI package not found. Download from AnxietySolo's HF."
                
                logger.info("📦 Extracting ComfyUI package...")
                if not self._extract_package('ComfyUI'):
                    return False, "Failed to extract ComfyUI"
        
        elif webui_type == 'Forge':
            if not pkg_status['forge_extracted']:
                if not pkg_status['forge_package']:
                    # Try to create it
                    logger.info("📦 Creating Forge package...")
                    if not self._create_forge_package():
                        return False, "Forge package not ready. Run package_forge_nsfw.sh"
                
                logger.info("📦 Extracting Forge package...")
                if not self._extract_package('Forge_NSFW_Maximum'):
                    return False, "Failed to extract Forge"
        
        # Setup central storage
        if not self.setup_webui_storage(webui_type):
            logger.warning("Central storage setup had issues but continuing...")
        
        # Download selected models if specified
        if selected_models:
            self._download_selected_models(selected_models)
        
        # Final status
        self.status[f'{webui_type.lower()}_ready'] = True
        
        logger.info(f"\n✅ {webui_type} is ready to launch!")
        return True, f"{webui_type} prepared successfully"
    
    def _extract_venv(self) -> bool:
        """Extract the shared venv archive"""
        
        venv_archive = self.packages_dir / 'python31018-venv-torch260-cu124-C-fca.tar.lz4'
        
        try:
            cmd = f"cd /workspace && pv {venv_archive} | lz4 -d | tar xf -"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Venv extracted successfully")
                return True
            else:
                logger.error(f"Failed to extract venv: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error extracting venv: {e}")
            return False
    
    def _extract_package(self, package_name: str) -> bool:
        """Extract a WebUI package"""
        
        package_file = self.packages_dir / f"{package_name}.zip"
        
        try:
            cmd = f"cd {self.webuis_dir} && unzip -q {package_file}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"✅ {package_name} extracted successfully")
                return True
            else:
                logger.error(f"Failed to extract {package_name}: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error extracting {package_name}: {e}")
            return False
    
    def _create_forge_package(self) -> bool:
        """Create Forge package using our script"""
        
        script_path = self.project_root / 'scripts' / 'package_forge_nsfw.sh'
        
        if not script_path.exists():
            logger.error("Package creation script not found")
            return False
        
        try:
            # Make executable and run
            script_path.chmod(0o755)
            result = subprocess.run(str(script_path), capture_output=True, text=True)
            
            if result.returncode == 0:
                # Move to packages dir
                package_file = self.project_root / 'package_build' / 'Forge_NSFW_Maximum.zip'
                if package_file.exists():
                    package_file.rename(self.packages_dir / 'Forge_NSFW_Maximum.zip')
                    logger.info("✅ Forge package created")
                    return True
            
            logger.error(f"Package creation failed: {result.stderr}")
            return False
        except Exception as e:
            logger.error(f"Error creating package: {e}")
            return False
    
    def _download_selected_models(self, model_list: List[str]):
        """Download specific models selected in UI"""
        
        logger.info(f"📥 Downloading {len(model_list)} selected models...")
        
        for model_spec in model_list:
            # Parse model spec (format: "type/name")
            if '/' in model_spec:
                model_type, model_name = model_spec.split('/', 1)
                if self.storage_manager:
                    self.storage_manager.download_model(model_type, model_name)
    
    def get_storage_report(self) -> Dict:
        """Get current storage status for UI display"""
        
        report = {
            'total_size': 0,
            'model_counts': {},
            'saved_space': 0,
            'status': self.status
        }
        
        # Calculate sizes
        for model_type in ['sam', 'adetailer', 'controlnet', 'upscalers', 'reactor']:
            model_dir = self.storage_root / model_type
            if model_dir.exists():
                files = list(model_dir.glob('*'))
                size = sum(f.stat().st_size for f in files if f.is_file())
                report['model_counts'][model_type] = len(files)
                report['total_size'] += size
        
        # Estimate saved space (rough calculation)
        # Each extension would have its own copy without central storage
        extension_count = len(self.status.get('extensions_ready', {}))
        if extension_count > 1:
            report['saved_space'] = report['total_size'] * (extension_count - 1)
        
        return report

# ============================================================================
# INTEGRATION FUNCTIONS FOR CELL 2
# ============================================================================

def prepare_webui_launch(webui_type: str, **kwargs) -> Tuple[bool, str]:
    """
    Main entry point from widgets-en.py
    Called when user clicks launch button
    """
    
    integration = Cell2StorageIntegration()
    
    # Get any selected models from UI
    selected_models = kwargs.get('selected_models', [])
    
    # Prepare for launch
    success, message = integration.prepare_for_launch(webui_type, selected_models)
    
    # Get storage report for display
    report = integration.get_storage_report()
    
    # Log report
    if report['saved_space'] > 0:
        saved_gb = report['saved_space'] / (1024**3)
        logger.info(f"💾 Central storage saved {saved_gb:.2f} GB of disk space!")
    
    return success, message

def get_model_options() -> Dict[str, List[Dict]]:
    """
    Get available models for UI selection
    Returns categorized model options
    """
    
    options = {}
    
    for model_type, models in MODEL_REGISTRY.items():
        options[model_type] = []
        for model_name, info in models.items():
            options[model_type].append({
                'name': model_name,
                'size': info.get('size', 'Unknown'),
                'description': info.get('description', ''),
                'value': f"{model_type}/{model_name}"
            })
    
    return options

def check_extension_compatibility(webui_type: str, extension_list: List[str]) -> Dict[str, bool]:
    """
    Check which extensions are compatible with selected WebUI
    """
    
    compatibility = {}
    
    # Based on our analysis
    if webui_type == 'Forge':
        # 29/31 work
        incompatible = ['wd14-tagger', 'sd-webui-reactor']  # Original reactor
        for ext in extension_list:
            ext_name = ext.split('/')[-1] if '/' in ext else ext
            compatibility[ext] = ext_name not in incompatible
    
    elif webui_type == 'ComfyUI':
        # ComfyUI doesn't use A1111 extensions
        for ext in extension_list:
            compatibility[ext] = False
    
    return compatibility

# ============================================================================
# MAIN (for testing)
# ============================================================================

if __name__ == "__main__":
    # Test the integration
    success, message = prepare_webui_launch('ComfyUI')
    print(f"Result: {success} - {message}")
    
    # Get model options
    options = get_model_options()
    print(f"\nAvailable models: {len(options)} categories")
    
    # Check compatibility
    test_extensions = ['adetailer', 'sd-webui-controlnet']
    compat = check_extension_compatibility('Forge', test_extensions)
    print(f"\nExtension compatibility: {compat}")