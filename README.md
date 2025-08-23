# SD-DarkMaster-Pro 🎨

A streamlined Stable Diffusion WebUI launcher for Google Colab, Kaggle, and cloud platforms.

## 🚀 Quick Start

1. **Open the notebook**: `notebook/SD-DarkMaster-Pro.ipynb`
2. **Run the cells in order**:
   - Cell 1: Sets up environment
   - Cell 2: Opens configuration UI (or use Cell 2b as fallback)
   - Cell 3: Downloads selected models
   - Cell 4: Launches your chosen WebUI
   - Cell 5: Manages storage

That's it! No complex setup required.

## 📁 Repository Structure

```
SD-DarkMaster-Pro/
├── notebook/
│   └── SD-DarkMaster-Pro.ipynb    # Main notebook (run this!)
├── scripts/
│   ├── setup.py                   # Environment setup
│   ├── widgets-en.py              # Configuration UI
│   ├── downloading-en.py          # Model downloader
│   ├── launch.py                  # WebUI launcher
│   ├── auto-cleaner.py            # Storage manager
│   ├── _models_data.py            # SD1.5 model data
│   └── _xl_models_data.py         # SDXL model data
├── configs/                       # Configuration files
├── storage/                       # Model storage
└── assets/                        # UI assets
```

## 🎯 Features

- **Multi-WebUI Support**: A1111, Forge, ComfyUI, SD.Next, Fooocus, InvokeAI
- **Integrated Model Browser**: CivitAI search and download
- **Smart Downloads**: aria2c acceleration with fallback
- **Unified Storage**: Share models across all WebUIs
- **Platform Detection**: Auto-optimizes for Colab/Kaggle/Cloud

## 🛠️ Two Installation Methods

1. **Git Clone** (Standard): Fresh installation each time
2. **Package Method** (Fast): Pre-configured WebUI packages

Choose in Cell 2's UI based on your needs.

## 📝 Notes

- Designed for notebook environments (Colab, Kaggle, etc.)
- All output is verbose - see exactly what's happening
- Cell 2b provides a simpler UI if Cell 2 has issues

## 🔗 Links

- [Original Repository](https://github.com/remphanostar/SD-DarkMaster-Pro)

---

**Made with ❤️ for the Stable Diffusion community**