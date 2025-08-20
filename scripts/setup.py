#!/usr/bin/env python3
"""
SD-DarkMaster-Pro Setup Script
Dual-framework platform setup with Dark Mode Pro theming
400+ lines of enterprise-grade initialization
"""

import os
import sys
import subprocess
import json
import time
import asyncio
import platform
import shutil
import hashlib
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request
import urllib.error

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

PROJECT_NAME = "SD-DarkMaster-Pro"
VERSION = "1.0.0"
GITHUB_REPO = "https://github.com/anxietysolo/SD-DarkMaster-Pro"

# Platform detection configurations
PLATFORM_CONFIGS = {
    'colab': {
        'root': '/content',
        'gpu_check': 'nvidia-smi',
        'package_manager': 'apt-get',
        'python_path': '/usr/local/lib/python3.10/dist-packages'
    },
    'kaggle': {
        'root': '/kaggle/working',
        'gpu_check': 'nvidia-smi',
        'package_manager': 'apt-get',
        'python_path': '/opt/conda/lib/python3.10/site-packages'
    },
    'workspace': {
        'root': '/workspace',
        'gpu_check': 'nvidia-smi',
        'package_manager': 'apt-get',
        'python_path': '/usr/local/lib/python3.10/dist-packages'
    },
    'lightning': {
        'root': str(Path.home() / 'work'),
        'gpu_check': 'nvidia-smi',
        'package_manager': 'apt-get',
        'python_path': '/opt/conda/lib/python3.10/site-packages'
    },
    'paperspace': {
        'root': '/notebooks',
        'gpu_check': 'nvidia-smi',
        'package_manager': 'apt-get',
        'python_path': '/usr/local/lib/python3.10/dist-packages'
    },
    'runpod': {
        'root': '/workspace',
        'gpu_check': 'nvidia-smi',
        'package_manager': 'apt-get',
        'python_path': '/usr/local/lib/python3.10/dist-packages'
    },
    'vast': {
        'root': '/workspace',
        'gpu_check': 'nvidia-smi',
        'package_manager': 'apt-get',
        'python_path': '/usr/local/lib/python3.10/dist-packages'
    },
    'sagemaker': {
        'root': '/opt/ml/code',
        'gpu_check': 'nvidia-smi',
        'package_manager': 'yum',
        'python_path': '/opt/conda/lib/python3.10/site-packages'
    },
    'azure': {
        'root': '/mnt/batch/tasks/shared/LS_root',
        'gpu_check': 'nvidia-smi',
        'package_manager': 'apt-get',
        'python_path': '/usr/local/lib/python3.10/dist-packages'
    },
    'gcp': {
        'root': '/home/jupyter',
        'gpu_check': 'nvidia-smi',
        'package_manager': 'apt-get',
        'python_path': '/opt/conda/lib/python3.10/site-packages'
    },
    'lambda': {
        'root': '/home/ubuntu',
        'gpu_check': 'nvidia-smi',
        'package_manager': 'apt-get',
        'python_path': '/usr/local/lib/python3.10/dist-packages'
    },
    'local': {
        'root': str(Path.home()),
        'gpu_check': 'nvidia-smi',
        'package_manager': 'pip',
        'python_path': str(Path(sys.executable).parent.parent / 'lib' / 'python3.10' / 'site-packages')
    }
}

# Dark Mode Pro theme configuration
DARK_MODE_PRO_THEME = {
    'primary': '#111827',      # Deep black
    'accent': '#10B981',       # Electric green
    'text': '#6B7280',         # Cool gray
    'surface': '#1F2937',      # Elevated surfaces
    'border': '#374151',       # Subtle borders
    'gradient': 'linear-gradient(135deg, #111827 0%, #1F2937 50%, #10B981 100%)'
}

# Required dependencies
CORE_DEPENDENCIES = [
    'streamlit>=1.28.0',
    'gradio>=4.0.0',
    'torch>=2.0.0',
    'torchvision',
    'transformers>=4.30.0',
    'diffusers>=0.21.0',
    'accelerate',
    'xformers',
    'opencv-python',
    'Pillow>=10.0.0',
    'numpy',
    'pandas',
    'requests',
    'tqdm',
    'pyyaml',
    'jsonschema',
    'aiohttp',
    'aiofiles',
    'psutil',
    'matplotlib',
    'seaborn',
    'plotly',
    'rich'
]

# WebUI configurations
WEBUI_CONFIGS = {
    'A1111': {
        'repo': 'https://github.com/AUTOMATIC1111/stable-diffusion-webui',
        'launch_script': 'launch.py',
        'requirements': 'requirements.txt'
    },
    'ComfyUI': {
        'repo': 'https://github.com/comfyanonymous/ComfyUI',
        'launch_script': 'main.py',
        'requirements': 'requirements.txt'
    },
    'Forge': {
        'repo': 'https://github.com/lllyasviel/stable-diffusion-webui-forge',
        'launch_script': 'launch.py',
        'requirements': 'requirements.txt'
    },
    'ReForge': {
        'repo': 'https://github.com/Panchovix/stable-diffusion-webui-reForge',
        'launch_script': 'launch.py',
        'requirements': 'requirements.txt'
    },
    'SD-UX': {
        'repo': 'https://github.com/sd-ux/stable-diffusion-webui-ux',
        'launch_script': 'launch.py',
        'requirements': 'requirements.txt'
    }
}

# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging():
    """Configure enterprise-grade logging with Dark Mode Pro styling"""
    log_dir = Path('/workspace/SD-DarkMaster-Pro/logs')
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f"setup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()

# ============================================================================
# PLATFORM DETECTION & OPTIMIZATION
# ============================================================================

class PlatformDetector:
    """Advanced platform detection with 12+ platform support"""
    
    @staticmethod
    def detect_platform() -> str:
        """Detect current cloud GPU platform"""
        # Check for Colab
        if os.path.exists('/content'):
            return 'colab'
        
        # Check for Kaggle
        if os.path.exists('/kaggle'):
            return 'kaggle'
        
        # Check for various cloud platforms
        if 'LIGHTNING_CLOUD_PROJECT_ID' in os.environ:
            return 'lightning'
        
        if 'PAPERSPACE_GRADIENT_ID' in os.environ:
            return 'paperspace'
        
        if 'RUNPOD_POD_ID' in os.environ:
            return 'runpod'
        
        if 'VAST_CONTAINERLABEL' in os.environ:
            return 'vast'
        
        if 'SAGEMAKER_INTERNAL_IMAGE_URI' in os.environ:
            return 'sagemaker'
        
        if 'AZURE_BATCH_POOL_ID' in os.environ:
            return 'azure'
        
        if 'GCP_PROJECT' in os.environ:
            return 'gcp'
        
        if 'LAMBDA_CLOUD' in os.environ:
            return 'lambda'
        
        # Check for workspace environments
        if os.path.exists('/workspace'):
            return 'workspace'
        
        # Default to local
        return 'local'
    
    @staticmethod
    def get_platform_config(platform: str) -> Dict[str, Any]:
        """Get platform-specific configuration"""
        return PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS['local'])
    
    @staticmethod
    def optimize_for_platform(platform: str) -> Dict[str, Any]:
        """Apply platform-specific optimizations"""
        optimizations = {
            'num_workers': 4,
            'batch_size': 1,
            'mixed_precision': 'fp16',
            'gradient_checkpointing': True,
            'cpu_offload': False,
            'attention_slicing': True
        }
        
        # Platform-specific adjustments
        if platform == 'colab':
            if PlatformDetector.check_gpu_availability():
                optimizations['batch_size'] = 4
                optimizations['mixed_precision'] = 'fp16'
        
        elif platform in ['paperspace', 'runpod', 'vast', 'lambda']:
            optimizations['num_workers'] = 8
            optimizations['batch_size'] = 8
            
        elif platform == 'kaggle':
            optimizations['gradient_checkpointing'] = True
            optimizations['cpu_offload'] = True
            
        return optimizations
    
    @staticmethod
    def check_gpu_availability() -> bool:
        """Check if GPU is available"""
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

# ============================================================================
# DEPENDENCY MANAGEMENT
# ============================================================================

class DependencyManager:
    """Manage Python dependencies with platform-specific handling"""
    
    def __init__(self, platform: str):
        self.platform = platform
        self.config = PlatformDetector.get_platform_config(platform)
        
    async def install_dependencies(self, dependencies: List[str]) -> bool:
        """Install dependencies asynchronously"""
        logger.info(f"Installing {len(dependencies)} dependencies for {self.platform}")
        
        # Upgrade pip first
        await self._run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # Install dependencies in batches
        batch_size = 5
        for i in range(0, len(dependencies), batch_size):
            batch = dependencies[i:i+batch_size]
            cmd = [sys.executable, '-m', 'pip', 'install'] + batch
            
            try:
                await self._run_command(cmd)
                logger.info(f"Installed batch {i//batch_size + 1}: {batch}")
            except Exception as e:
                logger.error(f"Failed to install batch: {e}")
                return False
        
        return True
    
    async def _run_command(self, cmd: List[str]) -> None:
        """Run command asynchronously"""
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise RuntimeError(f"Command failed: {stderr.decode()}")

# ============================================================================
# UNIFIED STORAGE SETUP
# ============================================================================

class UnifiedStorageManager:
    """Universal storage setup with cross-WebUI compatibility"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.storage_dir = project_root / 'storage'
        self.model_dirs = {
            'checkpoints': self.storage_dir / 'models' / 'Stable-diffusion',
            'vae': self.storage_dir / 'models' / 'VAE',
            'lora': self.storage_dir / 'models' / 'Lora',
            'embeddings': self.storage_dir / 'embeddings',
            'hypernetworks': self.storage_dir / 'models' / 'hypernetworks',
            'controlnet': self.storage_dir / 'models' / 'ControlNet',
            'upscalers': self.storage_dir / 'models' / 'ESRGAN'
        }
        
    def setup_storage_structure(self) -> None:
        """Create unified storage directory structure"""
        logger.info("Setting up unified storage structure...")
        
        for dir_type, dir_path in self.model_dirs.items():
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created {dir_type} directory: {dir_path}")
        
        # Create additional directories
        additional_dirs = [
            self.storage_dir / 'outputs',
            self.storage_dir / 'temp',
            self.storage_dir / 'cache',
            self.storage_dir / 'configs'
        ]
        
        for dir_path in additional_dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    def create_symbolic_links(self, webui_path: Path) -> None:
        """Create symbolic links for WebUI compatibility"""
        webui_model_dir = webui_path / 'models'
        
        if webui_model_dir.exists():
            # Backup existing models directory
            backup_dir = webui_path / 'models_backup'
            if not backup_dir.exists():
                shutil.move(str(webui_model_dir), str(backup_dir))
                logger.info(f"Backed up existing models to {backup_dir}")
        
        # Create symbolic link to unified storage
        try:
            os.symlink(str(self.storage_dir / 'models'), str(webui_model_dir))
            logger.info(f"Created symbolic link: {webui_model_dir} -> {self.storage_dir / 'models'}")
        except Exception as e:
            logger.error(f"Failed to create symbolic link: {e}")

# ============================================================================
# EXTENSION PRE-INSTALLATION
# ============================================================================

class ExtensionManager:
    """Manage extension pre-installation from _extensions.txt"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.extensions_file = project_root / 'scripts' / '_extensions.txt'
        self.extensions = self._load_extensions()
        
    def _load_extensions(self) -> List[str]:
        """Load extensions from _extensions.txt"""
        if not self.extensions_file.exists():
            logger.warning(f"Extensions file not found: {self.extensions_file}")
            return []
        
        with open(self.extensions_file, 'r') as f:
            extensions = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        logger.info(f"Loaded {len(extensions)} extensions for pre-installation")
        return extensions
    
    async def pre_install_extensions(self, webui_path: Path) -> None:
        """Pre-install extensions for WebUI"""
        extensions_dir = webui_path / 'extensions'
        extensions_dir.mkdir(parents=True, exist_ok=True)
        
        for extension_url in self.extensions:
            try:
                extension_name = extension_url.split('/')[-1].replace('.git', '')
                extension_path = extensions_dir / extension_name
                
                if not extension_path.exists():
                    cmd = ['git', 'clone', extension_url, str(extension_path)]
                    process = await asyncio.create_subprocess_exec(
                        *cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    await process.communicate()
                    logger.info(f"Installed extension: {extension_name}")
                else:
                    logger.info(f"Extension already exists: {extension_name}")
                    
            except Exception as e:
                logger.error(f"Failed to install extension {extension_url}: {e}")

# ============================================================================
# CONFIGURATION CREATION
# ============================================================================

class ConfigurationManager:
    """Create and manage configuration files"""
    
    def __init__(self, project_root: Path, platform: str):
        self.project_root = project_root
        self.platform = platform
        self.config_dir = project_root / 'configs'
        
    def create_streamlit_config(self) -> None:
        """Create Streamlit configuration with Dark Mode Pro theme"""
        streamlit_dir = self.config_dir / 'streamlit'
        streamlit_dir.mkdir(parents=True, exist_ok=True)
        
        config_toml = streamlit_dir / 'config.toml'
        config_content = f"""
[theme]
primaryColor = "{DARK_MODE_PRO_THEME['accent']}"
backgroundColor = "{DARK_MODE_PRO_THEME['primary']}"
secondaryBackgroundColor = "{DARK_MODE_PRO_THEME['surface']}"
textColor = "{DARK_MODE_PRO_THEME['text']}"
font = "sans serif"

[server]
port = 8501
enableCORS = true
enableXsrfProtection = true

[browser]
gatherUsageStats = false
"""
        
        with open(config_toml, 'w') as f:
            f.write(config_content)
        
        logger.info(f"Created Streamlit config: {config_toml}")
    
    def create_gradio_config(self) -> None:
        """Create Gradio fallback configuration"""
        gradio_dir = self.config_dir / 'gradio_fallback'
        gradio_dir.mkdir(parents=True, exist_ok=True)
        
        config_json = gradio_dir / 'interface_config.json'
        config_data = {
            'theme': 'dark',
            'primary_color': DARK_MODE_PRO_THEME['accent'],
            'background_color': DARK_MODE_PRO_THEME['primary'],
            'text_color': DARK_MODE_PRO_THEME['text'],
            'enable_queue': True,
            'share': False,
            'server_port': 7860
        }
        
        with open(config_json, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        logger.info(f"Created Gradio config: {config_json}")
    
    def create_environment_config(self) -> None:
        """Create environment configuration with platform data"""
        env_config = self.config_dir / 'environment.json'
        env_data = {
            'platform': self.platform,
            'platform_config': PlatformDetector.get_platform_config(self.platform),
            'optimizations': PlatformDetector.optimize_for_platform(self.platform),
            'gpu_available': PlatformDetector.check_gpu_availability(),
            'theme': DARK_MODE_PRO_THEME,
            'version': VERSION,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(env_config, 'w') as f:
            json.dump(env_data, f, indent=2)
        
        logger.info(f"Created environment config: {env_config}")

# ============================================================================
# TIMER & SESSION TRACKING
# ============================================================================

class SessionManager:
    """Manage session timing and tracking"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.session_file = project_root / 'configs' / 'session.json'
        self.start_time = time.time()
        
    def initialize_session(self) -> None:
        """Initialize session tracking"""
        session_data = {
            'session_id': hashlib.md5(str(time.time()).encode()).hexdigest()[:8],
            'start_time': self.start_time,
            'platform': PlatformDetector.detect_platform(),
            'status': 'initializing'
        }
        
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        logger.info(f"Session initialized: {session_data['session_id']}")
    
    def update_status(self, status: str) -> None:
        """Update session status"""
        if self.session_file.exists():
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            session_data['status'] = status
            session_data['last_update'] = time.time()
            session_data['duration'] = time.time() - self.start_time
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)

# ============================================================================
# MAIN SETUP ORCHESTRATOR
# ============================================================================

class SetupOrchestrator:
    """Main setup orchestrator for SD-DarkMaster-Pro"""
    
    def __init__(self):
        self.platform = PlatformDetector.detect_platform()
        # Handle both script and notebook execution contexts
        try:
            self.project_root = Path(__file__).parent.parent
        except NameError:
            # When executed from notebook via exec()
            if self.platform == 'workspace':
                self.project_root = Path('/workspace/SD-DarkMaster-Pro')
            elif self.platform == 'colab':
                self.project_root = Path('/content/SD-DarkMaster-Pro')
            elif self.platform == 'kaggle':
                self.project_root = Path('/kaggle/working/SD-DarkMaster-Pro')
            else:
                self.project_root = Path.cwd()
        self.dependency_manager = DependencyManager(self.platform)
        self.storage_manager = UnifiedStorageManager(self.project_root)
        self.extension_manager = ExtensionManager(self.project_root)
        self.config_manager = ConfigurationManager(self.project_root, self.platform)
        self.session_manager = SessionManager(self.project_root)
        
    async def run_setup(self) -> None:
        """Run complete setup process"""
        print("\n" + "="*60)
        print(f"🌟 SD-DarkMaster-Pro Setup v{VERSION}")
        print(f"🎨 Dark Mode Pro Theme Activated")
        print(f"🖥️  Platform: {self.platform}")
        print(f"🚀 GPU Available: {PlatformDetector.check_gpu_availability()}")
        print("="*60 + "\n")
        
        try:
            # Initialize session
            self.session_manager.initialize_session()
            
            # Install dependencies
            logger.info("Installing core dependencies...")
            await self.dependency_manager.install_dependencies(CORE_DEPENDENCIES)
            self.session_manager.update_status('dependencies_installed')
            
            # Setup unified storage
            logger.info("Setting up unified storage...")
            self.storage_manager.setup_storage_structure()
            self.session_manager.update_status('storage_configured')
            
            # Create configurations
            logger.info("Creating configuration files...")
            self.config_manager.create_streamlit_config()
            self.config_manager.create_gradio_config()
            self.config_manager.create_environment_config()
            self.session_manager.update_status('configs_created')
            
            # Success message
            self.session_manager.update_status('ready')
            
            print("\n" + "="*60)
            print("✅ Setup Complete!")
            print(f"⏱️  Duration: {time.time() - self.session_manager.start_time:.2f} seconds")
            print(f"📁 Project Root: {self.project_root}")
            print(f"🎨 Theme: Dark Mode Pro")
            print(f"🚀 Status: Ready to launch")
            print("="*60 + "\n")
            
        except Exception as e:
            logger.error(f"Setup failed: {e}")
            self.session_manager.update_status('failed')
            raise

# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Main entry point for setup script"""
    orchestrator = SetupOrchestrator()
    
    # Run setup asynchronously
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Handle both normal execution and notebook context
    try:
        asyncio.run(orchestrator.run_setup())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            # Already in an event loop (e.g., Jupyter notebook)
            import nest_asyncio
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(orchestrator.run_setup())
        else:
            raise

if __name__ == "__main__":
    main()