#!/usr/bin/env python3
"""
Streamlit App Builder - Claude-Powered Version
Uses Claude (via Cursor) as the brain for code generation
Can work with image descriptions or direct text prompts
"""

import streamlit as st
import base64
import time
from tempfile import NamedTemporaryFile

# App title
st.set_page_config(page_title='🛠 Claude-Powered Streamlit Builder', page_icon='🤖')
st.title('🤖 Claude-Powered Streamlit App Builder')
st.info('**Show** me an image (I\'ll help describe it) or **Tell** me what you want, and I\'ll generate the Streamlit code!')

tabs = st.tabs(['Show (Image)', 'Tell (Text)', 'Claude Interface'])

# ============================================
# SHOW TAB - Image Input
# ============================================
with tabs[0]:
    st.subheader('📸 Upload Your Mockup')
    
    # Upload image
    image_upload = st.file_uploader('Upload a mockup image', type=['png', 'jpg', 'jpeg'])
    
    if image_upload:
        st.image(image_upload, use_column_width=True)
        
        # Image description helper
        st.markdown("---")
        st.markdown("### 🎨 Describe This Image for Claude")
        st.info("""
        Since Claude can't directly see images in this environment, 
        please describe what you see. Be specific about:
        - Layout (columns, rows, tabs)
        - Components (buttons, sliders, charts)
        - Colors and styling
        - Text content
        """)
        
        # Guided description fields
        col1, col2 = st.columns(2)
        
        with col1:
            layout_desc = st.text_area(
                "Layout Structure",
                placeholder="e.g., 3 columns, sidebar, main area",
                height=100
            )
            
            components_desc = st.text_area(
                "UI Components",
                placeholder="e.g., dropdown, metric cards, charts",
                height=100
            )
        
        with col2:
            styling_desc = st.text_area(
                "Colors & Styling",
                placeholder="e.g., dark theme, red accents",
                height=100
            )
            
            data_desc = st.text_area(
                "Data/Content",
                placeholder="e.g., model names, statistics",
                height=100
            )
        
        if st.button('🤖 Generate Prompt for Claude'):
            full_description = f"""
Create a Streamlit app based on this mockup:
Layout: {layout_desc}
Components: {components_desc}
Styling: {styling_desc}
Data: {data_desc}
            """
            st.code(full_description, language='text')
            st.success("Copy this to Claude in Cursor!")

# ============================================
# TELL TAB - Text Prompt
# ============================================
with tabs[1]:
    st.subheader('💬 Describe What You Want')
    
    text_prompt = st.text_area(
        "Describe the Streamlit app:",
        height=200,
        placeholder="Create a dark-themed dashboard with..."
    )
    
    if st.button('🤖 Format for Claude'):
        prompt = f"""
Generate a complete Streamlit app with:
{text_prompt}

Include all imports, mock data, and styling.
        """
        st.code(prompt, language='text')
        st.success("Copy this to Claude!")

# ============================================
# CLAUDE INTERFACE TAB
# ============================================
with tabs[2]:
    st.subheader('🔌 Direct Claude Interface')
    
    st.markdown("""
    ### Workflow:
    1. Describe what you want
    2. Copy the formatted prompt
    3. Paste to Claude in Cursor
    4. Claude generates the code
    5. Paste back here to save
    """)
    
    # Quick templates
    if st.button("📱 Our Model UI Template"):
        st.code("""
Generate SD-DarkMaster-Pro UI with:
- Dark theme (#0e0e0e)
- Toggle buttons (gray/red)
- Nested tabs structure
- Single download button
- Output console
        """, language='text')
    
    # Code response area
    st.markdown("### 📥 Paste Claude's Code:")
    code_response = st.text_area("Generated code:", height=400)
    
    if code_response and st.button("💾 Save"):
        with open('/workspace/generated_app.py', 'w') as f:
            f.write(code_response)
        st.success("Saved to generated_app.py!")