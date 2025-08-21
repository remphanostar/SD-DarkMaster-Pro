#!/usr/bin/env python3
"""
Unified Model Manager - Tracks all models from dictionaries and downloads
Integrates with CivitAI browser and extension requirements
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import hashlib
import requests
from datetime import datetime

# Import model dictionaries
from _models_data import model_list as sd15_models
from _xl_models_data import model_list as sdxl_models
from setup_central_storage import MODEL_REGISTRY, EXTENSION_MODEL_MAP

class UnifiedModelManager:
    """Manages all models - dictionary, downloaded, and browser"""
    
    def __init__(self):
        self.project_root = Path('/workspace/SD-DarkMaster-Pro')
        self.storage_root = self.project_root / 'storage'
        self.models_dir = self.storage_root / 'models'
        self.downloaded_models_file = self.project_root / 'configs' / 'downloaded_models.json'
        
        # Create directories
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.downloaded_models_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load downloaded models tracker
        self.downloaded_models = self._load_downloaded_models()
        
        # Scan for installed extensions
        self.installed_extensions = self._scan_installed_extensions()
        
    def _load_downloaded_models(self) -> Dict:
        """Load the downloaded models database"""
        if self.downloaded_models_file.exists():
            with open(self.downloaded_models_file, 'r') as f:
                return json.load(f)
        return {
            'checkpoints': {},
            'loras': {},
            'vae': {},
            'controlnet': {},
            'extensions': {}  # SAM, ADetailer, etc.
        }
    
    def _save_downloaded_models(self):
        """Save the downloaded models database"""
        with open(self.downloaded_models_file, 'w') as f:
            json.dump(self.downloaded_models, f, indent=2)
    
    def _scan_installed_extensions(self) -> Set[str]:
        """Scan for installed extensions in WebUI directories"""
        extensions = set()
        
        # Check Forge extensions
        forge_ext_dir = self.project_root / 'webuis' / 'Forge' / 'extensions'
        if forge_ext_dir.exists():
            for ext_dir in forge_ext_dir.iterdir():
                if ext_dir.is_dir():
                    extensions.add(ext_dir.name)
        
        # Check ComfyUI custom nodes
        comfy_nodes_dir = self.project_root / 'webuis' / 'ComfyUI' / 'custom_nodes'
        if comfy_nodes_dir.exists():
            for node_dir in comfy_nodes_dir.iterdir():
                if node_dir.is_dir():
                    extensions.add(node_dir.name)
        
        return extensions
    
    def get_all_models(self, model_type: str = 'all') -> Dict:
        """Get all models from dictionaries + downloaded"""
        models = {}
        
        if model_type in ['all', 'sd15']:
            models['sd15'] = {
                'dictionary': sd15_models,
                'downloaded': self._get_downloaded_by_type('sd15'),
                'installed': self._check_installed_models(sd15_models, 'sd15')
            }
        
        if model_type in ['all', 'sdxl']:
            # Separate SDXL, Pony, and Illustrious
            sdxl_standard = {k: v for k, v in sdxl_models.items() 
                           if 'pony' not in k.lower() and 'illustrious' not in k.lower()}
            pony = {k: v for k, v in sdxl_models.items() if 'pony' in k.lower()}
            illustrious = {k: v for k, v in sdxl_models.items() if 'illustrious' in k.lower()}
            
            models['sdxl'] = {
                'dictionary': sdxl_standard,
                'downloaded': self._get_downloaded_by_type('sdxl'),
                'installed': self._check_installed_models(sdxl_standard, 'sdxl')
            }
            models['pony'] = {
                'dictionary': pony,
                'downloaded': self._get_downloaded_by_type('pony'),
                'installed': self._check_installed_models(pony, 'pony')
            }
            models['illustrious'] = {
                'dictionary': illustrious,
                'downloaded': self._get_downloaded_by_type('illustrious'),
                'installed': self._check_installed_models(illustrious, 'illustrious')
            }
        
        return models
    
    def _get_downloaded_by_type(self, model_type: str) -> Dict:
        """Get downloaded models by type"""
        if model_type in ['sd15', 'sdxl', 'pony', 'illustrious']:
            return self.downloaded_models.get('checkpoints', {}).get(model_type, {})
        return {}
    
    def _check_installed_models(self, model_dict: Dict, model_type: str) -> Dict:
        """Check which models from dictionary are actually installed"""
        installed = {}
        
        for model_name in model_dict:
            # Check various possible paths
            paths_to_check = [
                self.models_dir / 'Stable-diffusion' / model_name,
                self.models_dir / 'Stable-diffusion' / f"{model_name}.safetensors",
                self.models_dir / 'Stable-diffusion' / f"{model_name}.ckpt",
            ]
            
            for path in paths_to_check:
                if path.exists():
                    installed[model_name] = {
                        'path': str(path),
                        'size': path.stat().st_size,
                        'modified': datetime.fromtimestamp(path.stat().st_mtime).isoformat()
                    }
                    break
        
        return installed
    
    def get_extension_requirements(self) -> Dict[str, List[str]]:
        """Get model requirements for installed extensions"""
        requirements = {}
        
        for ext_name in self.installed_extensions:
            # Check if extension is in our map
            if ext_name in EXTENSION_MODEL_MAP:
                ext_info = EXTENSION_MODEL_MAP[ext_name]
                requirements[ext_name] = {
                    'required': ext_info.get('required_models', []),
                    'optional': ext_info.get('optional_models', []),
                    'models': self._get_models_for_categories(
                        ext_info.get('required_models', []) + 
                        ext_info.get('optional_models', [])
                    )
                }
            # Try to detect requirements from extension files
            else:
                detected = self._detect_extension_requirements(ext_name)
                if detected:
                    requirements[ext_name] = detected
        
        return requirements
    
    def _get_models_for_categories(self, categories: List[str]) -> Dict:
        """Get specific models for given categories (sam, adetailer, etc.)"""
        models = {}
        
        for category in categories:
            if category in MODEL_REGISTRY:
                models[category] = MODEL_REGISTRY[category]
        
        return models
    
    def _detect_extension_requirements(self, ext_name: str) -> Optional[Dict]:
        """Try to detect what models an extension needs by scanning its files"""
        requirements = {
            'required': [],
            'optional': [],
            'models': {}
        }
        
        # Common patterns to look for
        patterns = {
            'sam': ['segment', 'sam_', 'segment_anything'],
            'controlnet': ['controlnet', 'control_'],
            'adetailer': ['adetailer', 'yolo', 'detection'],
            'upscalers': ['upscale', 'esrgan', 'realesrgan'],
            'reactor': ['reactor', 'inswapper', 'face_swap']
        }
        
        # Scan extension files for patterns
        ext_paths = [
            self.project_root / 'webuis' / 'Forge' / 'extensions' / ext_name,
            self.project_root / 'webuis' / 'ComfyUI' / 'custom_nodes' / ext_name
        ]
        
        for ext_path in ext_paths:
            if ext_path.exists():
                # Check Python files for imports/references
                for py_file in ext_path.rglob('*.py'):
                    try:
                        content = py_file.read_text().lower()
                        for category, keywords in patterns.items():
                            if any(keyword in content for keyword in keywords):
                                if category not in requirements['required']:
                                    requirements['optional'].append(category)
                                    requirements['models'][category] = MODEL_REGISTRY.get(category, {})
                    except:
                        continue
        
        return requirements if requirements['optional'] or requirements['required'] else None
    
    def add_downloaded_model(self, model_info: Dict):
        """Add a model downloaded from CivitAI or other sources"""
        model_type = model_info.get('type', 'checkpoints')
        model_subtype = model_info.get('subtype', 'unknown')
        model_name = model_info.get('name')
        
        if model_type not in self.downloaded_models:
            self.downloaded_models[model_type] = {}
        
        if model_subtype not in self.downloaded_models[model_type]:
            self.downloaded_models[model_type][model_subtype] = {}
        
        self.downloaded_models[model_type][model_subtype][model_name] = {
            'url': model_info.get('url'),
            'size': model_info.get('size'),
            'hash': model_info.get('hash'),
            'downloaded_at': datetime.now().isoformat(),
            'source': model_info.get('source', 'unknown'),
            'path': model_info.get('path'),
            'metadata': model_info.get('metadata', {})
        }
        
        self._save_downloaded_models()
    
    def get_model_status(self, model_name: str) -> Dict:
        """Get complete status of a model"""
        status = {
            'in_dictionary': False,
            'downloaded': False,
            'installed': False,
            'path': None,
            'size': None,
            'source': None
        }
        
        # Check dictionaries
        if model_name in sd15_models:
            status['in_dictionary'] = True
            status['source'] = 'sd15_dictionary'
        elif model_name in sdxl_models:
            status['in_dictionary'] = True
            status['source'] = 'sdxl_dictionary'
        
        # Check downloaded
        for model_type in self.downloaded_models:
            for subtype in self.downloaded_models[model_type]:
                if model_name in self.downloaded_models[model_type][subtype]:
                    status['downloaded'] = True
                    status['source'] = self.downloaded_models[model_type][subtype][model_name].get('source')
                    break
        
        # Check installed
        possible_paths = [
            self.models_dir / 'Stable-diffusion' / model_name,
            self.models_dir / 'Stable-diffusion' / f"{model_name}.safetensors",
            self.models_dir / 'Stable-diffusion' / f"{model_name}.ckpt",
            self.models_dir / 'Lora' / model_name,
            self.models_dir / 'Lora' / f"{model_name}.safetensors",
        ]
        
        for path in possible_paths:
            if path.exists():
                status['installed'] = True
                status['path'] = str(path)
                status['size'] = path.stat().st_size
                break
        
        return status
    
    def scan_storage_directory(self) -> Dict:
        """Scan storage directory and update database"""
        found_models = {
            'checkpoints': [],
            'loras': [],
            'vae': [],
            'controlnet': [],
            'extensions': {}
        }
        
        # Scan checkpoints
        ckpt_dir = self.models_dir / 'Stable-diffusion'
        if ckpt_dir.exists():
            for file in ckpt_dir.iterdir():
                if file.suffix in ['.safetensors', '.ckpt']:
                    found_models['checkpoints'].append({
                        'name': file.stem,
                        'path': str(file),
                        'size': file.stat().st_size
                    })
        
        # Scan LoRAs
        lora_dir = self.models_dir / 'Lora'
        if lora_dir.exists():
            for file in lora_dir.iterdir():
                if file.suffix in ['.safetensors', '.pt']:
                    found_models['loras'].append({
                        'name': file.stem,
                        'path': str(file),
                        'size': file.stat().st_size
                    })
        
        # Scan extension models
        for ext_type in ['sam', 'adetailer', 'controlnet', 'upscalers', 'reactor']:
            ext_dir = self.storage_root / ext_type
            if ext_dir.exists():
                found_models['extensions'][ext_type] = []
                for file in ext_dir.iterdir():
                    if file.is_file():
                        found_models['extensions'][ext_type].append({
                            'name': file.name,
                            'path': str(file),
                            'size': file.stat().st_size
                        })
        
        return found_models

# Singleton instance
_manager = None

def get_model_manager() -> UnifiedModelManager:
    """Get or create the singleton model manager"""
    global _manager
    if _manager is None:
        _manager = UnifiedModelManager()
    return _manager

if __name__ == "__main__":
    # Test the manager
    manager = get_model_manager()
    
    print("📊 Model Status Report")
    print("="*50)
    
    # Get all models
    all_models = manager.get_all_models()
    for model_type, info in all_models.items():
        dict_count = len(info['dictionary'])
        installed_count = len(info['installed'])
        print(f"{model_type.upper()}: {installed_count}/{dict_count} installed")
    
    # Get extension requirements
    print("\n📦 Extension Requirements")
    print("="*50)
    requirements = manager.get_extension_requirements()
    for ext, req in requirements.items():
        print(f"{ext}:")
        print(f"  Required: {req['required']}")
        print(f"  Optional: {req['optional']}")
    
    # Scan storage
    print("\n💾 Storage Scan")
    print("="*50)
    found = manager.scan_storage_directory()
    for category, items in found.items():
        if isinstance(items, list):
            print(f"{category}: {len(items)} files")
        elif isinstance(items, dict):
            for subcat, subitems in items.items():
                print(f"{category}/{subcat}: {len(subitems)} files")