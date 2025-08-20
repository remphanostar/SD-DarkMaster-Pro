# 🌟 SD-DarkMaster-Pro

[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)](https://github.com/anxietysolo/SD-DarkMaster-Pro)
[![Platform](https://img.shields.io/badge/platform-12%2B%20supported-blue)](https://github.com/anxietysolo/SD-DarkMaster-Pro)
[![Theme](https://img.shields.io/badge/theme-Dark%20Mode%20Pro-black)](https://github.com/anxietysolo/SD-DarkMaster-Pro)

## 🎨 The Ultimate Stable Diffusion WebUI Platform

SD-DarkMaster-Pro is an enterprise-grade AI generation platform that combines the simplicity of a 5-cell notebook with sophisticated backend capabilities. Experience the power of multiple WebUIs, native CivitAI integration, and unified storage management - all wrapped in a stunning Dark Mode Pro aesthetic.

---

## ✨ Key Features

### 🚀 **5-Cell Simplicity**
- **Cell 1:** Setup Environment - Auto-detects 12+ platforms
- **Cell 2:** Hybrid Dashboard & Native CivitAI Browser
- **Cell 3:** Intelligent Downloads & Storage Management
- **Cell 4:** Multi-Platform WebUI Launch
- **Cell 5:** Advanced Storage Cleanup & Optimization

### 🌐 **Multi-Platform Support**
- Google Colab
- Kaggle
- Lightning AI
- Paperspace Gradient
- RunPod
- Vast.ai
- SageMaker
- Azure ML
- Google Cloud Platform
- Lambda Labs
- Modal
- Local environments

### 🎯 **Enterprise Features**
- **Native CivitAI Browser:** Search and download models directly
- **LoRA Main Interface:** Integrated LoRA selection (not in custom downloads)
- **Multi-Select Everything:** Checkboxes replace all dropdowns
- **Unified Storage:** Single storage system across all WebUIs
- **Dual Framework:** Streamlit primary with Gradio fallback
- **Dark Mode Pro:** Professional dark theme throughout

### 🔧 **WebUI Support**
- AUTOMATIC1111
- ComfyUI
- Forge
- ReForge
- SD.Next
- SD-UX

---

## 🚀 Quick Start

### 1. **Open in Your Platform**
Simply open the notebook in any supported platform (Colab, Kaggle, etc.)

### 2. **Run the 5 Cells**
```python
# Cell 1: Setup Environment ⚙️
# Cell 2: Hybrid Dashboard & CivitAI Browser 🌟
# Cell 3: Intelligent Downloads & Storage 📦
# Cell 4: Multi-Platform WebUI Launch 🚀
# Cell 5: Advanced Storage Management 🧹
```

### 3. **Enjoy!**
The platform auto-detects your environment and optimizes everything automatically.

---

## 📦 Installation

### **Option 1: Direct Notebook**
1. Download `SD-DarkMaster-Pro.ipynb`
2. Upload to your platform
3. Run all cells

### **Option 2: Git Clone**
```bash
git clone https://github.com/anxietysolo/SD-DarkMaster-Pro.git
cd SD-DarkMaster-Pro
python scripts/setup.py
```

### **Option 3: One-Line Install**
```bash
curl -sL https://raw.githubusercontent.com/anxietysolo/SD-DarkMaster-Pro/main/install.sh | bash
```

---

## 🎨 Dark Mode Pro Theme

The Dark Mode Pro aesthetic features:
- **Primary:** Deep black (#111827)
- **Accent:** Electric green (#10B981)
- **Text:** Cool gray (#6B7280)
- **Surfaces:** Elevated dark (#1F2937)
- **Borders:** Subtle gray (#374151)

All interfaces automatically apply this theme for a consistent, professional experience.

---

## 🔧 Configuration

### **Session Configuration**
The platform saves your preferences automatically:
- Selected models
- LoRA configurations
- Extension preferences
- WebUI settings

### **Import/Export Settings**
```python
# Export your configuration
Download Config → sd_darkmaster_config.json

# Import on another machine
Upload Config → Restore all settings
```

---

## 📊 Storage Management

### **Unified Storage Structure**
```
storage/
├── models/
│   ├── Stable-diffusion/
│   ├── Lora/
│   ├── VAE/
│   └── ControlNet/
├── outputs/
├── cache/
└── configs/
```

### **Automatic Cleanup**
- Remove duplicates
- Clean old files (>30 days)
- Clear temporary files
- Optimize cache

---

## 🌟 Advanced Features

### **Native CivitAI Browser**
- Search models directly in the interface
- Preview images and metadata
- One-click downloads to unified storage
- NSFW filtering options

### **Multi-Select System**
- Checkbox grids for all selections
- Batch operations (Select All, Clear All)
- Visual selection counters
- Download queue management

### **Platform Optimizations**
- Automatic GPU detection
- VRAM-based optimization
- xformers auto-enable
- Mixed precision settings
- Attention slicing for low VRAM

### **Tunnel Services**
- Cloudflare (default)
- ngrok
- localtunnel
- bore
- zrok
- serveo

---

## 📱 Mobile Support

SD-DarkMaster-Pro is fully responsive:
- Touch-optimized controls
- Swipe navigation
- Mobile-friendly layouts
- OLED-optimized dark theme

---

## 🔐 Security

- Local storage only (no external data transmission)
- Secure API key management
- Optional authentication
- Audit logging

---

## 🛠️ Troubleshooting

### **Framework Issues**
If Streamlit fails, the system automatically falls back to Gradio.

### **GPU Not Detected**
The platform automatically switches to CPU mode with optimized settings.

### **Storage Issues**
Run Cell 5 to analyze and clean storage.

### **Extension Conflicts**
Disable conflicting extensions in the dashboard.

---

## 📚 Documentation

- [User Manual](documentation/User_Manual.md)
- [API Reference](documentation/API_Reference.md)
- [Theme Customization](documentation/Dark_Mode_Pro_Guide.md)
- [Platform Guide](documentation/Platform_Guide.md)

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- AUTOMATIC1111 for the original WebUI
- ComfyUI team for the node-based interface
- CivitAI for the model repository
- All extension developers
- The Stable Diffusion community

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/anxietysolo/SD-DarkMaster-Pro/issues)
- **Discussions:** [GitHub Discussions](https://github.com/anxietysolo/SD-DarkMaster-Pro/discussions)
- **Wiki:** [Project Wiki](https://github.com/anxietysolo/SD-DarkMaster-Pro/wiki)

---

## 🚀 Roadmap

- [ ] Mobile app
- [ ] Cloud sync
- [ ] Model training interface
- [ ] Advanced workflow automation
- [ ] Community model hub
- [ ] Real-time collaboration

---

<div align="center">
  
**Built with ❤️ by the SD-DarkMaster-Pro Team**

[Website](https://darkmaster.pro) | [Twitter](https://twitter.com/darkmaster) | [Discord](https://discord.gg/darkmaster)

</div>