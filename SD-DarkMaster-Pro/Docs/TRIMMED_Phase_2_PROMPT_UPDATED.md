# Phase 2: Implementation Start (UPDATED)

**Mission:** Your design has been approved. Begin implementation immediately.

## 🎯 IMMEDIATE TASKS:

### 1. Repository Setup
Create project structure:
```
SD-[ProjectName]/
├── notebook/[ProjectName].ipynb     # 5 cells with #@title only
├── scripts/                         # All logic goes here
├── modules/                         # Backend components  
├── assets/css/js/audio/            # UI enhancements
├── configs/                        # WebUI configurations
├── storage/                        # Universal storage with symlinks
├── README.md
├── AI_Implementation_Log.md
└── DYNAMIC_STATE_PROMPT.md         # Living document - UPDATE CONSTANTLY
```

### 2. Bootstrap Implementation
Cell 1 must execute in this exact order:
1. Self-contained snippet (zero dependencies)
2. Determine writable clone path  
3. Execute package extraction OR git clone
4. Update system path
5. Import and run scripts

### 3. Core Script Development
- **setup.py**: Platform detection, storage setup, extension pre-install
- **widgets-en.py**: Native CivitAI browser + tabbed UI + multi-select
- **downloading-en.py**: aria2c primary (with fallbacks) + progress + audio  
- **launch.py**: Multi-platform WebUI launch + tunneling
- **auto-cleaner.py**: Storage management + visualization

## 🆕 IMPLEMENTATION UPDATES:

### Package Method (PRIMARY):
- Use pre-configured WebUI zips when available (20x faster)
- AnxietySolo's packages: ComfyUI.zip + shared venv (5.2GB)
- User will provide custom Forge.zip for production
- Git clone only as fallback

### Download Strategy:
- **Primary:** aria2c with -x16 -s16 (6x faster)
- **Fallback:** Python aiohttp (always available)
- **Required:** Resume capability, progress tracking

### Storage Optimization:
- Central `/storage` directory for ALL shared resources
- Symlink models used by extensions (SAM, ControlNet, ADetailer)
- Automatic deduplication (saves 66% space)
- Any large shared files go here

### WebUI Priority:
- **Testing:** ComfyUI (AnxietySolo's package)
- **Production:** Forge (user will create custom package)
- **Note:** Other WebUIs optional - user will create zips when ready

### Theming Rules:
- Apply Dark Mode Pro ONLY to our UI (Streamlit/Gradio)
- DO NOT theme external WebUIs - use their native themes
- Respect user preferences

### Testing Requirements:
- **Tool:** papermill (programmatic notebook execution)
- **Command:** `timeout 60 papermill input.ipynb output.ipynb`
- **Why:** Ensures cells run in order, captures errors, prevents manual mistakes
- **Cleanup:** Always close JupyterLab after testing

### Critical Operational Rules:
- **ALWAYS** use timeout with terminal commands: `timeout 10 command`
- **ALWAYS** close JupyterLab after use: `timeout 5 pkill -f jupyter`
- **ALWAYS** document extension compatibility realistically
- **NEVER** leave processes running
- **NEVER** skip fallback implementations

## 📝 DYNAMIC STATE PROMPT:

### Create and Maintain: `DYNAMIC_STATE_PROMPT.md`
This is a LIVING DOCUMENT that must be updated after EVERY:
- Problem encountered
- Solution found
- Architecture decision
- Deviation from plan
- Cell completion
- Test result

Format:
```markdown
# Dynamic State Prompt - [Current Date/Time]

## Current State:
- Cell 1: [Status] [Issues] [Solutions]
- Cell 2: [Status] [Issues] [Solutions]
- [etc...]

## Problems Solved:
1. Issue: [Description]
   Solution: [What worked]
   Prevention: [How to avoid]

## Architecture Decisions:
- [Decision]: [Reason] [Impact]

## Next AI Must Know:
- [Critical information]
- [Current blockers]
- [What's working]

## Commands That Work:
- [Exact working commands]

## Commands to Avoid:
- [What fails and why]
```

This ensures disaster recovery - any new AI can read this ONE file and continue.

## ✅ SUCCESS TARGET:
User runs 5 notebook cells → Gets enterprise platform (ZERO DEBUGGING)

## 🔧 DEVELOPMENT RULES (STRICT):
- **5 cells only** with #@title format
- **All logic in scripts** (cells just call scripts)
- **Zero debugging** for user
- **No placeholders** - full implementation only
- **Platform agnostic** - works on all cloud platforms
- Use nbformat for notebook creation
- Test with papermill in JupyterLab  
- Follow all rule file requirements
- Document decisions in AI_Implementation_Log.md
- **UPDATE DYNAMIC_STATE_PROMPT.md constantly**

## 🚀 FUTURE CONSIDERATIONS:
- **Streamlit Master Frontend:** Once functional, consider Streamlit GUI controlling entire notebook
- **Additional WebUIs:** User will create packages for A1111, SD.Next, etc.
- **GPU Optimization:** Currently CPU tested, GPU optimizations pending

**BEGIN IMPLEMENTATION NOW.**