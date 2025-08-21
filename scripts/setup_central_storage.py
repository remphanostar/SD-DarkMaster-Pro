#!/usr/bin/env python3
"""
Central Model Storage Setup for SD-DarkMaster-Pro
Eliminates duplicate model downloads across extensions
"""

import os
import sys
import shutil
import hashlib
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# CENTRAL STORAGE CONFIGURATION
# ============================================================================

# Model URLs and hashes for verification
MODEL_REGISTRY = {
    'sam': {
        'sam_vit_h_4b8939.pth': {
            'url': 'https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth',
            'size': '2.4GB',
            'hash': '4b8939',
            'description': 'Best quality SAM model'
        },
        'sam_vit_l_0b3195.pth': {
            'url': 'https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth',
            'size': '1.2GB',
            'hash': '0b3195',
            'description': 'Large SAM model'
        },
        'sam_vit_b_01ec64.pth': {
            'url': 'https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth',
            'size': '375MB',
            'hash': '01ec64',
            'description': 'Base SAM model (fastest)'
        }
    },
    'adetailer': {
        'face_yolov8n.pt': {
            'url': 'https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8n.pt',
            'size': '6MB',
            'description': 'Face detection model'
        },
        'face_yolov8s.pt': {
            'url': 'https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8s.pt',
            'size': '22MB',
            'description': 'Face detection model (better)'
        },
        'hand_yolov8n.pt': {
            'url': 'https://huggingface.co/Bingsu/adetailer/resolve/main/hand_yolov8n.pt',
            'size': '6MB',
            'description': 'Hand detection model'
        },
        'person_yolov8n-seg.pt': {
            'url': 'https://huggingface.co/Bingsu/adetailer/resolve/main/person_yolov8n-seg.pt',
            'size': '6MB',
            'description': 'Person segmentation model'
        },
        'person_yolov8s-seg.pt': {
            'url': 'https://huggingface.co/Bingsu/adetailer/resolve/main/person_yolov8s-seg.pt',
            'size': '22MB',
            'description': 'Person segmentation model (better)'
        }
    },
    'controlnet': {
        'control_v11p_sd15_openpose.pth': {
            'url': 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth',
            'size': '1.45GB',
            'description': 'OpenPose ControlNet'
        },
        'control_v11p_sd15_canny.pth': {
            'url': 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.pth',
            'size': '1.45GB',
            'description': 'Canny edge ControlNet'
        },
        'control_v11f1p_sd15_depth.pth': {
            'url': 'https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth',
            'size': '1.45GB',
            'description': 'Depth ControlNet'
        }
    },
    'upscalers': {
        '4x-UltraSharp.pth': {
            'url': 'https://huggingface.co/lokCX/4x-Ultrasharp/resolve/main/4x-UltraSharp.pth',
            'size': '64MB',
            'description': 'High quality upscaler'
        },
        '4x_NMKD-Siax_200k.pth': {
            'url': 'https://huggingface.co/gemasai/4x_NMKD-Siax_200k/resolve/main/4x_NMKD-Siax_200k.pth',
            'size': '64MB',
            'description': 'NMKD upscaler'
        }
    },
    'reactor': {
        'inswapper_128.onnx': {
            'url': 'https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx',
            'size': '250MB',
            'description': 'Face swap model'
        },
        'GFPGANv1.4.pth': {
            'url': 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth',
            'size': '350MB',
            'description': 'Face restoration model'
        }
    }
}

# Extension to model mappings
EXTENSION_MODEL_MAP = {
    'sd-webui-segment-anything': {
        'models_dir': 'models',
        'required_models': ['sam'],
        'optional_models': []
    },
    'sd-webui-inpaint-anything': {
        'models_dir': 'models',
        'required_models': ['sam'],
        'optional_models': []
    },
    'sd-webui-replacer': {
        'models_dir': 'models',
        'required_models': [],
        'optional_models': ['sam']
    },
    'adetailer': {
        'models_dir': 'models',
        'required_models': ['adetailer'],
        'optional_models': []
    },
    'sd-webui-controlnet': {
        'models_dir': 'models',
        'required_models': [],
        'optional_models': ['controlnet']
    },
    'sd-webui-reactor-Nsfw_freedom': {
        'models_dir': 'models',
        'required_models': ['reactor'],
        'optional_models': []
    }
}

# ============================================================================
# CENTRAL STORAGE MANAGER
# ============================================================================

class CentralStorageManager:
    """Manages central model storage and symlinks"""
    
    def __init__(self, storage_root: Path = None, webui_root: Path = None):
        self.storage_root = storage_root or Path('/workspace/SD-DarkMaster-Pro/storage')
        self.webui_root = webui_root or Path('/workspace/SD-DarkMaster-Pro/webuis/Forge')
        self.extensions_dir = self.webui_root / 'extensions'
        
        # Create storage directories
        self.model_dirs = {
            'sam': self.storage_root / 'sam',
            'adetailer': self.storage_root / 'adetailer',
            'controlnet': self.storage_root / 'controlnet',
            'upscalers': self.storage_root / 'upscalers',
            'reactor': self.storage_root / 'reactor',
            'clip': self.storage_root / 'clip',
            'vae': self.storage_root / 'vae'
        }
        
        for dir_path in self.model_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def download_model(self, model_type: str, model_name: str, force: bool = False) -> Optional[Path]:
        """Download a model to central storage"""
        
        if model_type not in MODEL_REGISTRY:
            logger.error(f"Unknown model type: {model_type}")
            return None
        
        if model_name not in MODEL_REGISTRY[model_type]:
            logger.error(f"Unknown model: {model_name}")
            return None
        
        model_info = MODEL_REGISTRY[model_type][model_name]
        model_path = self.model_dirs[model_type] / model_name
        
        # Check if already exists
        if model_path.exists() and not force:
            logger.info(f"Model already exists: {model_path}")
            return model_path
        
        # Download
        logger.info(f"Downloading {model_name} ({model_info['size']})...")
        logger.info(f"Description: {model_info.get('description', 'N/A')}")
        
        try:
            urllib.request.urlretrieve(model_info['url'], model_path)
            logger.info(f"✅ Downloaded to: {model_path}")
            return model_path
        except Exception as e:
            logger.error(f"Failed to download {model_name}: {e}")
            return None
    
    def find_extension_models(self, extension_path: Path) -> Dict[str, List[Path]]:
        """Find existing models in an extension"""
        
        found_models = {}
        
        # Check common model directories
        for subdir in ['models', 'checkpoints', 'weights']:
            models_dir = extension_path / subdir
            if models_dir.exists():
                for model_file in models_dir.iterdir():
                    if model_file.is_file() and not model_file.is_symlink():
                        # Categorize by extension
                        ext = model_file.suffix
                        if ext not in found_models:
                            found_models[ext] = []
                        found_models[ext].append(model_file)
        
        return found_models
    
    def migrate_to_central(self, extension_path: Path, model_type: str) -> int:
        """Migrate existing models to central storage"""
        
        migrated = 0
        central_dir = self.model_dirs.get(model_type)
        
        if not central_dir:
            logger.error(f"Unknown model type: {model_type}")
            return 0
        
        # Find existing models
        found_models = self.find_extension_models(extension_path)
        
        for ext, model_files in found_models.items():
            for model_file in model_files:
                # Check if this model should be centralized
                if model_type == 'sam' and 'sam_' in model_file.name:
                    central_path = central_dir / model_file.name
                    
                    if not central_path.exists():
                        logger.info(f"Migrating {model_file.name} to central storage...")
                        shutil.move(str(model_file), str(central_path))
                    else:
                        logger.info(f"Removing duplicate: {model_file}")
                        model_file.unlink()
                    
                    migrated += 1
        
        return migrated
    
    def create_symlinks(self, extension_name: str, model_types: List[str]) -> int:
        """Create symlinks from extension to central storage"""
        
        extension_path = self.extensions_dir / extension_name
        if not extension_path.exists():
            logger.warning(f"Extension not found: {extension_name}")
            return 0
        
        created = 0
        
        # Get extension config
        ext_config = EXTENSION_MODEL_MAP.get(extension_name, {})
        models_subdir = ext_config.get('models_dir', 'models')
        models_dir = extension_path / models_subdir
        models_dir.mkdir(parents=True, exist_ok=True)
        
        for model_type in model_types:
            central_dir = self.model_dirs.get(model_type)
            if not central_dir:
                continue
            
            # Link all models of this type
            for model_file in central_dir.glob('*'):
                if model_file.is_file():
                    link_path = models_dir / model_file.name
                    
                    if link_path.exists():
                        if link_path.is_symlink():
                            logger.debug(f"Symlink already exists: {link_path}")
                        else:
                            logger.warning(f"File exists, not symlinking: {link_path}")
                    else:
                        link_path.symlink_to(model_file)
                        logger.info(f"Created symlink: {link_path} → {model_file}")
                        created += 1
        
        return created
    
    def setup_extension(self, extension_name: str) -> bool:
        """Complete setup for an extension"""
        
        if extension_name not in EXTENSION_MODEL_MAP:
            logger.warning(f"Unknown extension: {extension_name}")
            return False
        
        extension_path = self.extensions_dir / extension_name
        if not extension_path.exists():
            logger.warning(f"Extension not installed: {extension_name}")
            return False
        
        config = EXTENSION_MODEL_MAP[extension_name]
        
        logger.info(f"\nSetting up {extension_name}...")
        logger.info(f"Required models: {config['required_models']}")
        logger.info(f"Optional models: {config['optional_models']}")
        
        # Migrate existing models
        for model_type in config['required_models'] + config['optional_models']:
            migrated = self.migrate_to_central(extension_path, model_type)
            if migrated > 0:
                logger.info(f"Migrated {migrated} {model_type} models to central storage")
        
        # Create symlinks
        all_types = config['required_models'] + config['optional_models']
        created = self.create_symlinks(extension_name, all_types)
        logger.info(f"Created {created} symlinks")
        
        return True
    
    def setup_all_extensions(self):
        """Setup central storage for all known extensions"""
        
        logger.info("="*60)
        logger.info("Setting up central model storage for all extensions...")
        logger.info("="*60)
        
        for extension_name in EXTENSION_MODEL_MAP.keys():
            self.setup_extension(extension_name)
        
        logger.info("\n" + "="*60)
        logger.info("Central storage setup complete!")
        self.print_storage_report()
    
    def print_storage_report(self):
        """Print storage usage report"""
        
        logger.info("\n📊 Storage Report:")
        logger.info("-"*40)
        
        total_size = 0
        for model_type, model_dir in self.model_dirs.items():
            if model_dir.exists():
                size = sum(f.stat().st_size for f in model_dir.glob('*') if f.is_file())
                size_gb = size / (1024**3)
                count = len(list(model_dir.glob('*')))
                
                if count > 0:
                    logger.info(f"{model_type:12} : {count:3} files, {size_gb:.2f} GB")
                    total_size += size
        
        logger.info("-"*40)
        logger.info(f"Total        : {total_size / (1024**3):.2f} GB")
    
    def download_essential_models(self):
        """Download essential models for NSFW package"""
        
        logger.info("\n📦 Downloading essential models...")
        logger.info("-"*40)
        
        # Essential models for NSFW functionality
        essential = {
            'sam': ['sam_vit_b_01ec64.pth'],  # Start with smaller SAM
            'adetailer': ['face_yolov8n.pt', 'person_yolov8n-seg.pt'],
            'reactor': ['inswapper_128.onnx']  # For face swap
        }
        
        for model_type, models in essential.items():
            for model_name in models:
                self.download_model(model_type, model_name)

# ============================================================================
# MAIN FUNCTIONS
# ============================================================================

def main():
    """Main entry point"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup central model storage')
    parser.add_argument('--storage-root', type=Path, 
                       default='/workspace/SD-DarkMaster-Pro/storage',
                       help='Central storage root directory')
    parser.add_argument('--webui-root', type=Path,
                       default='/workspace/SD-DarkMaster-Pro/webuis/Forge',
                       help='WebUI root directory')
    parser.add_argument('--download-essential', action='store_true',
                       help='Download essential models')
    parser.add_argument('--setup-extension', type=str,
                       help='Setup specific extension')
    parser.add_argument('--setup-all', action='store_true',
                       help='Setup all known extensions')
    
    args = parser.parse_args()
    
    # Create manager
    manager = CentralStorageManager(args.storage_root, args.webui_root)
    
    # Execute requested actions
    if args.download_essential:
        manager.download_essential_models()
    
    if args.setup_extension:
        manager.setup_extension(args.setup_extension)
    
    if args.setup_all:
        manager.setup_all_extensions()
    
    if not any([args.download_essential, args.setup_extension, args.setup_all]):
        # Default action
        manager.setup_all_extensions()
        manager.print_storage_report()

if __name__ == "__main__":
    main()