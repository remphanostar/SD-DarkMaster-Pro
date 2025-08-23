#!/usr/bin/env python3
"""
Hybrid Streamlit App Builder
Supports multiple AI backends: Gemini, OpenAI, or Claude (via Cursor)
"""

import streamlit as st
import os
from pathlib import Path
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title='🛠 Hybrid Streamlit Builder',
    page_icon='🚀',
    layout='wide'
)

st.title('🚀 Hybrid Streamlit App Builder')
st.info('Choose your AI backend: **Gemini** (Google), **OpenAI** (GPT-4V), or **Claude** (via Cursor)')

# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    ai_backend = st.selectbox(
        "Select AI Backend",
        ["Claude (Free via Cursor)", "Gemini (Google)", "OpenAI (GPT-4)"]
    )
    
    if ai_backend == "Gemini (Google)":
        gemini_key = st.text_input("Gemini API Key", type="password")
        st.info("Get your key at: https://makersuite.google.com/app/apikey")
    
    elif ai_backend == "OpenAI (GPT-4)":
        openai_key = st.text_input("OpenAI API Key", type="password")
        st.info("Get your key at: https://platform.openai.com/api-keys")
    
    else:  # Claude
        st.success("✅ No API key needed!")
        st.info("Claude works through Cursor - just copy and paste!")
    
    st.markdown("---")
    st.markdown("### 🎨 Quick Templates")
    
    if st.button("📊 Dashboard Template"):
        st.session_state.template = "dashboard"
    if st.button("🤖 Model UI Template"):
        st.session_state.template = "model_ui"
    if st.button("📈 Data Viz Template"):
        st.session_state.template = "data_viz"

# Main tabs
tab1, tab2, tab3 = st.tabs(["📸 From Image", "💬 From Text", "🧪 Examples"])

# Image to Code Tab
with tab1:
    st.header("Generate from Image Mockup")
    
    uploaded_file = st.file_uploader(
        "Upload your mockup image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a screenshot or mockup of your desired app"
    )
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Your Mockup", use_column_width=True)
        
        with col2:
            st.markdown("### 📝 Describe for AI")
            
            layout = st.text_area(
                "Layout",
                placeholder="e.g., 3 columns, sidebar, tabs",
                height=80
            )
            
            components = st.text_area(
                "Components",
                placeholder="e.g., buttons, charts, tables",
                height=80
            )
            
            styling = st.text_area(
                "Styling",
                placeholder="e.g., dark theme, red accents",
                height=80
            )
        
        if st.button("🎯 Generate Code", key="gen_image"):
            
            if ai_backend == "Claude (Free via Cursor)":
                # Generate prompt for Claude
                prompt = f"""
Please generate a complete Streamlit app based on this mockup description:

LAYOUT: {layout}
COMPONENTS: {components}
STYLING: {styling}

Requirements:
1. Complete working code with all imports
2. Mock data where needed
3. Proper styling and layout
4. Error handling
5. Comments explaining the code

Generate the Streamlit code now:
"""
                st.markdown("### 📋 Copy this to Claude in Cursor:")
                st.code(prompt, language="text")
                
                st.markdown("### 📥 Paste Claude's Response:")
                response = st.text_area("Generated Code:", height=400, key="claude_response_img")
                
                if response:
                    st.download_button(
                        "💾 Download Code",
                        response,
                        file_name="generated_app.py",
                        mime="text/plain"
                    )
            
            elif ai_backend == "Gemini (Google)":
                if not gemini_key:
                    st.error("Please provide Gemini API key in sidebar")
                else:
                    with st.spinner("Gemini is generating..."):
                        # Here you'd call Gemini API
                        st.info("Gemini integration code would go here")
            
            else:  # OpenAI
                if not openai_key:
                    st.error("Please provide OpenAI API key in sidebar")
                else:
                    with st.spinner("GPT-4V is generating..."):
                        # Here you'd call OpenAI API
                        st.info("OpenAI integration code would go here")

# Text to Code Tab
with tab2:
    st.header("Generate from Text Description")
    
    # Template selector
    if 'template' in st.session_state:
        if st.session_state.template == "dashboard":
            default_text = """Create a dark-themed dashboard with:
- Header with title and date selector
- 4 metric cards showing KPIs
- Line chart for trends
- Data table at bottom"""
        elif st.session_state.template == "model_ui":
            default_text = """Create a model management UI with:
- Dark theme (#0e0e0e background)
- Toggle buttons for model selection (gray/red)
- Nested tabs for categories
- Download queue
- Output console"""
        else:
            default_text = ""
    else:
        default_text = ""
    
    description = st.text_area(
        "Describe your app",
        value=default_text,
        height=200,
        placeholder="Describe the Streamlit app you want..."
    )
    
    # Advanced options
    with st.expander("🎨 Advanced Options"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            theme = st.selectbox("Theme", ["Dark", "Light", "Custom"])
            layout_type = st.selectbox("Layout", ["Wide", "Centered"])
        
        with col2:
            include_sidebar = st.checkbox("Include Sidebar")
            include_auth = st.checkbox("Include Authentication")
        
        with col3:
            include_db = st.checkbox("Include Database")
            include_api = st.checkbox("Include API calls")
    
    if st.button("🎯 Generate Code", key="gen_text"):
        
        # Build comprehensive prompt
        full_prompt = f"""
Create a Streamlit app with these specifications:

DESCRIPTION: {description}

SETTINGS:
- Theme: {theme}
- Layout: {layout_type}
- Sidebar: {'Yes' if include_sidebar else 'No'}
- Authentication: {'Yes' if include_auth else 'No'}
- Database: {'Yes' if include_db else 'No'}
- API Integration: {'Yes' if include_api else 'No'}

Please generate complete, working Streamlit code.
"""
        
        if ai_backend == "Claude (Free via Cursor)":
            st.markdown("### 📋 Copy to Claude:")
            st.code(full_prompt, language="text")
            
            st.markdown("### 📥 Paste Response:")
            response = st.text_area("Generated Code:", height=400, key="claude_response_text")
            
            if response:
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "💾 Download Code",
                        response,
                        file_name="app.py"
                    )
                with col2:
                    if st.button("🔄 Request Improvements"):
                        st.code("Please improve the code with better error handling and comments", language="text")

# Examples Tab
with tab3:
    st.header("📚 Example Templates")
    
    example = st.selectbox(
        "Choose an example",
        ["SD-DarkMaster-Pro UI", "Data Dashboard", "ML Model Interface", "CRUD App"]
    )
    
    if example == "SD-DarkMaster-Pro UI":
        st.code("""
import streamlit as st

# Dark theme configuration
st.set_page_config(page_title="SD-DarkMaster-Pro", layout="wide")

st.markdown('''
<style>
.stApp { background: #0e0e0e; }
.model-button {
    background: #1a1a1a;
    border: 2px solid #2a2a2a;
    padding: 12px;
    margin: 4px;
    border-radius: 8px;
}
.model-button-selected {
    background: #ef4444 !important;
}
</style>
''', unsafe_allow_html=True)

# Title
st.title("🌟 SD-DarkMaster-Pro Dashboard")

# Tabs
tab1, tab2 = st.tabs(["Models", "Model Search"])

with tab1:
    # Nested tabs
    sdxl, etc = st.tabs(["SDXL", "etc"])
    
    with sdxl:
        models, loras, vae = st.tabs(["Models", "Loras", "VAE"])
        
        with models:
            # Model grid
            cols = st.columns(2)
            for i in range(6):
                with cols[i % 2]:
                    if st.button(f"Model {i+1}", key=f"m{i}"):
                        st.session_state[f'selected_{i}'] = True

# Download section
if st.button("📥 Download All", type="primary"):
    st.success("Downloading...")
    
# Output console
st.text_area("Output Console", value="System ready...", height=100)
""", language="python")
        
        if st.button("Use This Template"):
            st.session_state.template_code = True
            st.success("Template loaded! Modify as needed.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🤝 Powered by Claude (via Cursor) | Gemini | OpenAI</p>
    <p>No API keys needed with Claude!</p>
</div>
""", unsafe_allow_html=True)