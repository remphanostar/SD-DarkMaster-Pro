# Original Design Requirements & Specifications

## 📋 From SD-DarkMaster-Pro Final Design

### Core Philosophy:
- **Exactly 5 code cells** in notebook
- **#@title format only** (no ##, ###, or decorators)
- **All complex logic** offloaded to `/scripts`
- **Zero debugging** user experience

### Mandatory Repository Structure:
```
SD-DarkMaster-Pro/
├── notebook/
│   └── SD-DarkMaster-Pro.ipynb      # 5 cells, #@title only
├── scripts/
│   ├── setup.py                     # Platform detection & setup
│   ├── widgets-en.py                # UI components
│   ├── downloading-en.py            # Download management
│   ├── launch.py                    # WebUI launcher
│   └── auto-cleaner.py              # Storage management
├── modules/
│   ├── core/                        # Core functionality
│   ├── enterprise/                  # Enterprise features
│   ├── performance/                 # Optimization
│   ├── accessibility/               # Accessibility
│   └── hybrid/                      # Framework detection
├── assets/
│   ├── themes/                      # Dark Mode Pro theme
│   ├── icons/                       # UI icons
│   └── audio/                       # Notifications
├── configs/                         # Configurations
├── storage/                         # Universal storage
├── README.md
└── AI_Implementation_Log.md
```

### Cell 1 Requirements (Bootstrap):
1. Self-contained snippet (zero dependencies)
2. Dynamic clone path determination
3. Git clone as FIRST action
4. System path update
5. Script execution

### Dark Mode Pro Theme Specification:
```css
Primary Background: #0a0a0a to #1a1a1a
Secondary Background: #1e1e1e to #2a2a2a
Accent Green: #00ff88 (success/primary actions)
Accent Blue: #00aaff (links/secondary actions)
Warning: #ffaa00
Error: #ff3366
Text Primary: #e0e0e0
Text Secondary: #a0a0a0
```

### UI Requirements:
- **Dual Framework:** Streamlit primary, Gradio fallback
- **Native CivitAI Browser:** Full integration
- **Progressive Disclosure:** Hide complexity
- **Multi-Select Components:** Checkboxes for batch operations
- **Tabbed Interface:** Organized sections

### Storage Requirements:
- **Universal `/storage`:** All WebUIs share
- **Symbolic Links:** For efficiency
- **Auto-Organization:** By model type
- **Version Control:** Track changes

### WebUI Support Matrix:
- A1111 (Automatic1111)
- Forge (lllyasviel)
- SD.Next
- ComfyUI
- Fooocus
- InvokeAI

### Extension System:
- Pre-installation from `_extensions.txt`
- Per-WebUI compatibility checking
- Dependency resolution
- Conflict prevention

## 📋 From Phase 1 & Phase 2 Prompts

### Development Rules:
1. **No Manual Steps** - Everything automated
2. **Platform Agnostic** - Works on all cloud platforms
3. **Error Recovery** - Graceful fallbacks
4. **Audio Feedback** - For long operations
5. **Progress Tracking** - Visual feedback

### Success Metrics:
- User runs 5 cells → Gets enterprise platform
- Zero configuration required
- Zero debugging needed
- Works first time, every time

### Implementation Requirements:
- Use nbformat for notebook creation
- Test in JupyterLab
- Follow all design specifications
- Document all decisions
- No placeholders or TODOs

## 📋 From UI Guide

### Widget Requirements:
- **Model Selection:** SD1.5, SDXL, LoRA, VAE
- **Download Manager:** Progress bars, batch operations
- **CivitAI Integration:** Search, filter, download
- **Session Management:** Save/load configurations
- **Resource Monitor:** GPU, RAM, disk usage

### Interface Standards:
- Consistent color scheme
- Responsive layout
- Keyboard navigation
- Screen reader support
- Mobile compatibility

## 📋 Extension List (_extensions.txt)

### Required Extensions (31 total):
```
# Core functionality
https://github.com/Mikubill/sd-webui-controlnet
https://github.com/Bing-su/adetailer
https://github.com/hako-mikan/sd-webui-regional-prompter
https://github.com/Haoming02/sd-forge-couple

# UI/UX improvements
https://github.com/thomasasfk/sd-webui-aspect-ratio-helper
https://github.com/zanllp/sd-webui-infinite-image-browsing
https://github.com/ilian6806/stable-diffusion-webui-state
https://github.com/DominikDoom/a1111-sd-webui-tagcomplete

# Advanced features
https://github.com/continue-revolution/sd-webui-segment-anything
https://github.com/Uminosachi/sd-webui-inpaint-anything
https://github.com/light-and-ray/sd-webui-replacer
https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111

# NSFW specific
https://github.com/kainatquaderee/sd-webui-reactor-Nsfw_freedom
https://github.com/redmercy69/sd-webui-stripper
https://github.com/graemeniedermayer/clothseg

[+ 16 more extensions...]
```

## 📋 Model Lists

### SD 1.5 Models (_models_data.py):
- 10 models including NSFW variants
- 2 VAE models
- 16 ControlNet configurations
- 30+ LoRA models

### SDXL Models (_xl_models_data.py):
- 7 SDXL models (NSFW-focused)
- 3 SDXL VAE models
- 8 SDXL ControlNet configurations

## 📋 From AnxietySolo Wiki

### Package Structure:
```
WebUI.zip contents:
├── models/
│   └── ESRGAN/        # Pre-downloaded upscalers
├── repositories/       # Core repos pre-cloned
├── extensions/         # Pre-installed extensions
└── config.json        # Pre-configured settings
```

### Venv Structure:
- Python 3.10 for most WebUIs
- Python 3.11 for Forge Classic
- PyTorch 2.6.0+cu124
- All dependencies pre-installed

## 🎯 Design Principles

### User Experience:
1. **Simplicity First** - 5 cells, that's it
2. **Hide Complexity** - Scripts handle everything
3. **Fast Setup** - Under 10 minutes
4. **No Surprises** - Predictable behavior
5. **Professional Feel** - Enterprise-grade

### Technical Excellence:
1. **Modular Architecture** - Clear separation
2. **Reusable Components** - DRY principle
3. **Performance Optimized** - aria2c, symlinks
4. **Error Resilient** - Graceful fallbacks
5. **Well Documented** - Clear code, good comments

### Visual Design:
1. **Dark Mode Pro** - Consistent theme
2. **Clean Interface** - No clutter
3. **Clear Hierarchy** - Important things prominent
4. **Responsive** - Works on all screens
5. **Accessible** - Screen reader friendly

## 📊 Compliance Check

### Original Requirements Met: ✅
- 5-cell notebook structure ✅
- All mandatory scripts ✅
- Dark Mode Pro theme ✅
- CivitAI integration ✅
- Multi-WebUI support ✅
- Extension system ✅
- Universal storage ✅

### Enhancements Added:
- aria2c integration (6x faster)
- Central storage deduplication
- AnxietySolo package method
- Storage UI integration
- Bug fixes and optimizations

This document preserves all original design requirements and specifications for reference.