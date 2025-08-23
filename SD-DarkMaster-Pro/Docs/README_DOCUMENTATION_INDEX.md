# 📚 SD-DarkMaster-Pro Documentation Index

**Last Updated:** August 23, 2025  
**Version:** 2.0.0  
**Repository:** https://github.com/remphanostar/SD-DarkMaster-Pro

---

## 📋 Documentation Structure

### 🎯 Quick Start Documents
- **[README.md](../README.md)** - Project overview and quick start guide
- **[DYNAMIC_STATE_PROMPT.md](../DYNAMIC_STATE_PROMPT.md)** - Living document with current state
- **[AI_CONTINUITY_CHECKLIST.md](AI_CONTINUITY_CHECKLIST.md)** - Checklist for new AI agents

### 📊 Project Status & Overview
1. **[01_PROJECT_OVERVIEW_AND_STATUS.md](01_PROJECT_OVERVIEW_AND_STATUS.md)**
   - Complete project overview
   - Current implementation status
   - Architecture decisions
   - Component breakdown

2. **[TRIMMED_Phase_2_PROMPT_UPDATED.md](TRIMMED_Phase_2_PROMPT_UPDATED.md)**
   - **LATEST STATUS DOCUMENT**
   - 85% complete status
   - What's working, what's pending
   - Instructions for next agent

### 🛠️ Implementation Guides
3. **[02_IMPLEMENTATION_GUIDE_FOR_NEXT_SESSION.md](02_IMPLEMENTATION_GUIDE_FOR_NEXT_SESSION.md)**
   - Development environment setup
   - Tool usage guidelines
   - Common commands
   - Troubleshooting guide

4. **[03_TECHNICAL_DECISIONS_AND_STRATEGIES.md](03_TECHNICAL_DECISIONS_AND_STRATEGIES.md)**
   - Architecture choices
   - Technology stack decisions
   - Design patterns used
   - Performance optimizations

### 📐 Design & Requirements
5. **[04_ORIGINAL_DESIGN_REQUIREMENTS.md](04_ORIGINAL_DESIGN_REQUIREMENTS.md)**
   - Initial project specifications
   - Feature requirements
   - User stories
   - Success criteria

6. **[08_UI_AND_FEATURES_DOCUMENTATION.md](08_UI_AND_FEATURES_DOCUMENTATION.md)** *(NEW)*
   - Complete UI component documentation
   - Feature descriptions
   - Visual design specifications
   - User interaction flows

### 🔧 Technical Documentation
7. **[05_ANXIETYSOLO_PACKAGE_METHOD_COMPLETE.md](05_ANXIETYSOLO_PACKAGE_METHOD_COMPLETE.md)**
   - Package deployment strategy
   - WebUI integration methods
   - Storage optimization
   - Performance benefits

8. **[06_EXTENSION_COMPATIBILITY_COMPLETE_ANALYSIS.md](06_EXTENSION_COMPATIBILITY_COMPLETE_ANALYSIS.md)**
   - Extension compatibility matrix
   - Model requirements
   - Known limitations
   - Workarounds

### 🧪 Testing & Validation
9. **[09_TESTING_AND_VALIDATION.md](09_TESTING_AND_VALIDATION.md)** *(NEW)*
   - Complete test reports
   - Testing methodologies
   - Platform-specific tests
   - Performance metrics
   - Error scenarios and fixes

10. **[TESTING_HIERARCHY.md](TESTING_HIERARCHY.md)**
    - Testing priorities
    - Test execution order
    - Validation criteria

11. **[WHAT_IS_PAPERMILL.md](WHAT_IS_PAPERMILL.md)**
    - Papermill explanation
    - Usage instructions
    - Benefits for notebook testing

### 📜 History & Updates
12. **[07_IMPLEMENTATION_HISTORY_AND_DECISIONS.md](07_IMPLEMENTATION_HISTORY_AND_DECISIONS.md)**
    - Development timeline
    - Key decisions made
    - Problems encountered
    - Solutions implemented

13. **[PROMPT_UPDATES_NEEDED.md](PROMPT_UPDATES_NEEDED.md)**
    - Changes from original requirements
    - Approved deviations
    - Updated specifications

---

## 🗂️ Document Categories

### For New Developers
Start with these documents in order:
1. README.md
2. AI_CONTINUITY_CHECKLIST.md
3. TRIMMED_Phase_2_PROMPT_UPDATED.md
4. 01_PROJECT_OVERVIEW_AND_STATUS.md

### For UI Development
- 08_UI_AND_FEATURES_DOCUMENTATION.md
- 04_ORIGINAL_DESIGN_REQUIREMENTS.md
- scripts/widgets-en.py (source code)

### For Testing
- 09_TESTING_AND_VALIDATION.md
- TESTING_HIERARCHY.md
- WHAT_IS_PAPERMILL.md

### For Deployment
- 05_ANXIETYSOLO_PACKAGE_METHOD_COMPLETE.md
- 06_EXTENSION_COMPATIBILITY_COMPLETE_ANALYSIS.md
- 02_IMPLEMENTATION_GUIDE_FOR_NEXT_SESSION.md

### For Project History
- 07_IMPLEMENTATION_HISTORY_AND_DECISIONS.md
- PROMPT_UPDATES_NEEDED.md
- DYNAMIC_STATE_PROMPT.md

---

## 📍 Key Files Outside Docs Folder

### Root Directory
- `/README.md` - Main project README
- `/DYNAMIC_STATE_PROMPT.md` - Current state tracking

### Scripts
- `/scripts/widgets-en.py` - Main UI implementation
- `/scripts/setup.py` - Environment setup
- `/scripts/cell2_ngrok_launcher.py` - Colab support
- `/scripts/unified_model_manager.py` - Model management
- `/scripts/civitai_browser.py` - CivitAI integration

### Notebook
- `/notebook/SD-DarkMaster-Pro.ipynb` - Main 5-cell notebook

### Configuration
- `/configs/` - WebUI configurations
- `/storage/storage_metadata.json` - Storage structure

---

## 🔄 Documentation Maintenance

### Update Frequency
- **DYNAMIC_STATE_PROMPT.md** - After every major change
- **Status documents** - After each development session
- **Technical docs** - When implementation changes
- **Test reports** - After test runs

### Version Control
All documentation is version controlled in the main repository.
Check git history for change tracking:
```bash
git log --oneline Docs/
```

### Contributing
When adding new documentation:
1. Use descriptive filenames with number prefix
2. Update this index file
3. Follow existing formatting patterns
4. Include "Last Updated" timestamps

---

## 📞 Quick Reference

### Testing Commands
```bash
# Test notebook
timeout 60 papermill notebook/SD-DarkMaster-Pro.ipynb /tmp/test.ipynb --kernel python3

# Test UI
streamlit run scripts/widgets-en.py --server.port 8501

# Test Colab mode
python3 test_as_colab.py
```

### Git Commands
```bash
# Update documentation
cd /workspace
git add SD-DarkMaster-Pro/Docs/
git commit -m "Update documentation"
git push origin main
```

### Environment Setup
```bash
# Activate environment
source /workspace/ai_tools_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

*This index is the central reference for all project documentation. Keep it updated as new documents are added.*