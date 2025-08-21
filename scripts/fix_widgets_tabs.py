#!/usr/bin/env python3
"""
Fix widgets-en.py to reorganize tabs properly
"""

# Read the original file
with open('/workspace/scripts/widgets-en-backup.py', 'r') as f:
    content = f.read()

# Find and replace the tab creation section
# Original has tabs within Models tab for sam/adetailer/etc
# We want Models to have SD1.5/SDXL/Pony tabs
# And a separate Extensions tab for sam/adetailer/etc

# Replace the main tabs line
old_tabs = '''        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📦 Models",
            "🎨 LoRA",
            "🔍 CivitAI Browser",
            "⚙️ Settings",
            "📊 Status"
        ])'''

new_tabs = '''        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📦 Models",
            "🎨 LoRA",
            "🔍 CivitAI Browser",
            "🔧 Extensions",
            "⚙️ Settings",
            "📊 Status"
        ])'''

content = content.replace(old_tabs, new_tabs)

# Now find the model tabs section and replace it
old_model_tabs = '''            # Create tabs for model categories
            model_tabs = st.tabs(list(model_options.keys()))
            
            selected_models = []
            for idx, (category, models) in enumerate(model_options.items()):
                with model_tabs[idx]:
                    st.markdown(f"#### {category.upper()} Models")'''

new_model_tabs = '''            # Create tabs for model types
            model_type_tabs = st.tabs(["🎨 SD 1.5", "🚀 SDXL", "🦄 Pony/Illustrious"])
            
            selected_models = []
            
            with model_type_tabs[0]:
                st.markdown("#### SD 1.5 Models")
                # Display SD 1.5 models from dictionary
                from scripts._models_data import model_list as sd15_models
                cols = st.columns(3)
                for idx, (name, info) in enumerate(sd15_models.items()):
                    with cols[idx % 3]:
                        if st.checkbox(name[:30], key=f"sd15_{name}"):
                            selected_models.append(f"sd15/{name}")
                        st.caption(f"Size: {info.get('size', 'Unknown')}")
            
            with model_type_tabs[1]:
                st.markdown("#### SDXL Models")
                # Display SDXL models from dictionary
                from scripts._xl_models_data import model_list as sdxl_models
                cols = st.columns(3)
                for idx, (name, info) in enumerate(sdxl_models.items()):
                    with cols[idx % 3]:
                        if st.checkbox(name[:30], key=f"sdxl_{name}"):
                            selected_models.append(f"sdxl/{name}")
                        st.caption(f"Size: {info.get('size', 'Unknown')}")
            
            with model_type_tabs[2]:
                st.markdown("#### Pony/Illustrious Models")
                # Filter for Pony/Illustrious models
                pony_models = {k: v for k, v in sdxl_models.items() 
                              if 'pony' in k.lower() or 'illustrious' in k.lower()}
                if pony_models:
                    cols = st.columns(3)
                    for idx, (name, info) in enumerate(pony_models.items()):
                        with cols[idx % 3]:
                            if st.checkbox(name[:30], key=f"pony_{name}"):
                                selected_models.append(f"pony/{name}")
                            st.caption(f"Size: {info.get('size', 'Unknown')}")
                else:
                    st.info("No Pony/Illustrious models found")'''

content = content.replace(old_model_tabs, new_model_tabs)

# Add the Extensions tab content after tab3 (CivitAI)
extensions_tab_content = '''
        with tab4:
            # Extensions tab - SAM, ADetailer, ControlNet, etc.
            st.markdown("### 🔧 Extension Models")
            
            # Get extension models from MODEL_REGISTRY
            from setup_central_storage import MODEL_REGISTRY
            
            ext_tabs = st.tabs(["🎯 SAM", "👁️ ADetailer", "🎮 ControlNet", "🔍 Upscalers", "🔄 Reactor"])
            
            with ext_tabs[0]:
                st.markdown("#### SAM Models")
                for name, info in MODEL_REGISTRY.get('sam', {}).items():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        if st.checkbox(name, key=f"sam_{name}"):
                            if 'selected_extensions' not in st.session_state:
                                st.session_state['selected_extensions'] = []
                            st.session_state['selected_extensions'].append(f"sam/{name}")
                    with col2:
                        st.caption(info.get('size', ''))
                    with col3:
                        model_path = Path('/workspace/SD-DarkMaster-Pro/storage/sam') / name
                        st.success("✅") if model_path.exists() else st.text("⬇️")
            
            with ext_tabs[1]:
                st.markdown("#### ADetailer Models")
                for name, info in MODEL_REGISTRY.get('adetailer', {}).items():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        if st.checkbox(name, key=f"adet_{name}"):
                            if 'selected_extensions' not in st.session_state:
                                st.session_state['selected_extensions'] = []
                            st.session_state['selected_extensions'].append(f"adetailer/{name}")
                    with col2:
                        st.caption(info.get('size', ''))
                    with col3:
                        model_path = Path('/workspace/SD-DarkMaster-Pro/storage/adetailer') / name
                        st.success("✅") if model_path.exists() else st.text("⬇️")
            
            with ext_tabs[2]:
                st.markdown("#### ControlNet Models")
                for name, info in MODEL_REGISTRY.get('controlnet', {}).items():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        if st.checkbox(name, key=f"cn_{name}"):
                            if 'selected_extensions' not in st.session_state:
                                st.session_state['selected_extensions'] = []
                            st.session_state['selected_extensions'].append(f"controlnet/{name}")
                    with col2:
                        st.caption(info.get('size', ''))
                    with col3:
                        model_path = Path('/workspace/SD-DarkMaster-Pro/storage/controlnet') / name
                        st.success("✅") if model_path.exists() else st.text("⬇️")
            
            with ext_tabs[3]:
                st.markdown("#### Upscaler Models")
                for name, info in MODEL_REGISTRY.get('upscalers', {}).items():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        if st.checkbox(name, key=f"up_{name}"):
                            if 'selected_extensions' not in st.session_state:
                                st.session_state['selected_extensions'] = []
                            st.session_state['selected_extensions'].append(f"upscalers/{name}")
                    with col2:
                        st.caption(info.get('size', ''))
                    with col3:
                        model_path = Path('/workspace/SD-DarkMaster-Pro/storage/upscalers') / name
                        st.success("✅") if model_path.exists() else st.text("⬇️")
            
            with ext_tabs[4]:
                st.markdown("#### Reactor Models")
                for name, info in MODEL_REGISTRY.get('reactor', {}).items():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        if st.checkbox(name, key=f"react_{name}"):
                            if 'selected_extensions' not in st.session_state:
                                st.session_state['selected_extensions'] = []
                            st.session_state['selected_extensions'].append(f"reactor/{name}")
                    with col2:
                        st.caption(info.get('size', ''))
                    with col3:
                        model_path = Path('/workspace/SD-DarkMaster-Pro/storage/reactor') / name
                        st.success("✅") if model_path.exists() else st.text("⬇️")
'''

# Find where to insert the Extensions tab (after CivitAI tab)
insert_pos = content.find("        with tab4:")
if insert_pos != -1:
    # Replace tab4 with tab5 and tab5 with tab6
    content = content.replace("with tab4:", "with tab5:")
    content = content.replace("with tab5:", "with tab6:", 1)  # Only replace first occurrence
    
    # Insert the new tab4 (Extensions)
    content = content[:insert_pos] + extensions_tab_content + "\n" + content[insert_pos:]

# Add Path import if not present
if "from pathlib import Path" not in content:
    content = "from pathlib import Path\n" + content

# Write the fixed version
with open('/workspace/scripts/widgets-en.py', 'w') as f:
    f.write(content)

print("✅ Fixed widgets-en.py with reorganized tabs:")
print("  - Models tab now has: SD1.5 | SDXL | Pony/Illustrious")
print("  - New Extensions tab has: SAM | ADetailer | ControlNet | Upscalers | Reactor")
print("  - Model dictionaries are now properly integrated")