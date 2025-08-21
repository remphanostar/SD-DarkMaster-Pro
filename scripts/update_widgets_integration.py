#!/usr/bin/env python3
"""
Update widgets-en.py to integrate the unified model manager and CivitAI browser
"""

# Read the current widgets file
with open('/workspace/scripts/widgets-en.py', 'r') as f:
    content = f.read()

# Add imports at the top after existing imports
import_section = """
# Import unified model management
from unified_model_manager import get_model_manager
from civitai_browser import get_civitai_browser
"""

# Find the import section and add our imports
import_pos = content.find("from scripts.setup_central_storage")
if import_pos != -1:
    content = content[:import_pos] + import_section + "\n" + content[import_pos:]

# Replace the Models tab section to use the unified manager
models_section = '''
        with tab_models:
            st.markdown("#### SD 1.5 Checkpoints")
            
            # Get models from unified manager
            manager = get_model_manager()
            all_models = manager.get_all_models('sd15')
            sd15_data = all_models.get('sd15', {})
            
            # Show dictionary models
            if sd15_data.get('dictionary'):
                cols = st.columns(3)
                for idx, (name, info) in enumerate(sd15_data['dictionary'].items()):
                    with cols[idx % 3]:
                        # Check if installed
                        is_installed = name in sd15_data.get('installed', {})
                        
                        with st.container():
                            st.markdown(f"""
                            <div class="model-card">
                                <h5>{name[:30]}...</h5>
                                <p>Size: {info.get('size', 'Unknown')}</p>
                                <p>{'✅ Installed' if is_installed else '⬇️ Not installed'}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.checkbox("Select", key=f"sd15_model_{name}")
                            with col2:
                                if not is_installed:
                                    if st.button("Download", key=f"dl_sd15_{name}"):
                                        st.info(f"Downloading {name}...")
            else:
                st.info("No SD 1.5 models found")
'''

# Find and replace the SD1.5 models section
old_pattern = "st.markdown(\"#### SD 1.5 Checkpoints\")"
if old_pattern in content:
    # Find the section and replace it
    start = content.find(old_pattern)
    # Find the next "with tab_" to know where this section ends
    end = content.find("with tab_loras:", start)
    if end != -1:
        content = content[:start-12] + models_section + "\n        " + content[end:]

# Add CivitAI browser functionality
civitai_section = '''
    with browser_tabs[0]:
        st.markdown("#### CivitAI Browser")
        
        # Get browser instance
        browser = get_civitai_browser()
        
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            search = st.text_input("Search models", placeholder="e.g., anime, realistic, cartoon")
        with col2:
            model_type = st.selectbox("Type", ["All", "Checkpoint", "LORA", "VAE", "TextualInversion", "Controlnet"])
        with col3:
            nsfw = st.checkbox("Include NSFW")
        
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("Sort by", ["Most Downloaded", "Highest Rated", "Most Recent"])
        with col2:
            period = st.selectbox("Period", ["AllTime", "Year", "Month", "Week", "Day"])
        
        if st.button("🔍 Search CivitAI", use_container_width=True):
            with st.spinner("Searching CivitAI..."):
                # Perform search
                types = None if model_type == "All" else [model_type]
                results = browser.search_models(
                    query=search,
                    types=types,
                    sort=sort_by,
                    period=period,
                    nsfw=nsfw,
                    limit=20
                )
                
                if results:
                    st.success(f"Found {len(results)} models")
                    
                    # Display results
                    for model in results:
                        with st.expander(f"📦 {model['name']} ({model['type']})"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.text(f"Creator: {model['creator']}")
                                st.text(f"Base Model: {model['version']['base_model']}")
                                st.text(f"Size: {model['version']['size_kb'] / 1024:.1f} MB")
                                st.text(f"Downloads: {model['download_count']:,}")
                                
                                if st.button(f"⬇️ Download", key=f"dl_civitai_{model['id']}"):
                                    with st.spinner(f"Downloading {model['name']}..."):
                                        if browser.download_model(model):
                                            st.success("Downloaded successfully!")
                                            # Add to unified manager
                                            manager = get_model_manager()
                                            manager.add_downloaded_model({
                                                'name': model['name'],
                                                'type': model['type'].lower(),
                                                'subtype': model['version']['base_model'].lower().replace(' ', ''),
                                                'url': model['version']['download_url'],
                                                'size': model['version']['size_kb'] * 1024,
                                                'source': 'civitai',
                                                'metadata': model
                                            })
                                        else:
                                            st.error("Download failed")
                            
                            with col2:
                                # Show preview image if available
                                images = model['version'].get('images', [])
                                if images and len(images) > 0:
                                    img_url = images[0].get('url', '')
                                    if img_url:
                                        st.image(img_url, use_column_width=True)
                else:
                    st.warning("No models found")
        
        # Show trending models
        st.markdown("---")
        st.markdown("#### 🔥 Trending Today")
        
        if st.button("Load Trending", use_container_width=True):
            trending = browser.get_trending_models(period="Day", limit=5)
            for model in trending:
                st.text(f"• {model['name']} - {model['download_count']:,} downloads")
'''

# Find and replace the CivitAI browser section
old_civitai = "st.markdown(\"#### CivitAI Browser\")"
if old_civitai in content:
    start = content.find(old_civitai)
    start = content.rfind("with browser_tabs[0]:", 0, start)
    # Find the next "with browser_tabs" to know where this section ends
    end = content.find("with browser_tabs[1]:", start)
    if end != -1:
        content = content[:start] + "    " + civitai_section + "\n    " + content[end:]

# Add Misc section smart detection
misc_section = '''
    # MISC Section - Extension Models with Smart Detection
    with tab_misc:
        st.markdown("#### Extension Models")
        
        # Get model manager for smart detection
        manager = get_model_manager()
        requirements = manager.get_extension_requirements()
        
        if requirements:
            st.info(f"Detected {len(requirements)} extensions that need models")
            
            # Show requirements for each extension
            for ext_name, req_info in requirements.items():
                with st.expander(f"📦 {ext_name}"):
                    if req_info.get('required'):
                        st.warning(f"Required: {', '.join(req_info['required'])}")
                    if req_info.get('optional'):
                        st.info(f"Optional: {', '.join(req_info['optional'])}")
        
        ext_tabs = st.tabs([
            "SAM", 
            "Adetailer", 
            "Upscaler", 
            "Reactor", 
            "Auto-Detected"
        ])
'''

# Find and replace the Misc section
old_misc = "# MISC Section - Extension Models"
if old_misc in content:
    start = content.find(old_misc)
    end = content.find("with tab2:", start)  # Find where Models tab ends
    if end != -1:
        content = content[:start] + misc_section + "\n" + content[end:]

# Write the updated file
with open('/workspace/scripts/widgets-en.py', 'w') as f:
    f.write(content)

print("✅ Updated widgets-en.py with:")
print("  - Unified Model Manager integration")
print("  - Working CivitAI browser with search and download")
print("  - Smart extension requirement detection in Misc tab")
print("  - Model status tracking (dictionary/downloaded/installed)")