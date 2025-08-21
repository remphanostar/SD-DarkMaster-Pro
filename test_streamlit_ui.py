import streamlit as st

# Page config
st.set_page_config(page_title="SD-DarkMaster-Pro", layout="wide")

# Custom CSS for compact toggles
st.markdown("""
<style>
.stApp { background: #0a0a0a; }
.main .block-container { padding: 1rem; max-width: 100%; }

/* Style toggles to look like buttons */
.stToggle > label {
    background: #1a1a2e !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 6px !important;
    padding: 6px 12px !important;
    width: 100% !important;
    text-align: left !important;
    font-size: 13px !important;
    margin: 2px 0 !important;
}

.stToggle > label:hover {
    background: #2a2a3e !important;
    border-color: #10B981 !important;
}

/* When toggle is on */
.stToggle > label[data-baseweb="checkbox"]:has(input:checked) {
    background: #10B981 !important;
    border-color: #10B981 !important;
}

/* Hide the actual toggle switch */
.stToggle > label > div { display: none !important; }

/* Compact tabs */
.stTabs [data-baseweb="tab"] {
    height: 32px;
    padding: 4px 12px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🌟 SD-DarkMaster-Pro Dashboard")

# Initialize session state
if 'selected_models' not in st.session_state:
    st.session_state.selected_models = []

# Main tabs
tab1, tab2, tab3 = st.tabs(["Models", "Model Browser", "Settings"])

with tab1:
    # Model type tabs
    tab_sd15, tab_sdxl, tab_pony, tab_misc = st.tabs(["SD-1.5", "SDXL", "PONY", "Misc"])
    
    with tab_sd15:
        # Sub tabs
        sub1, sub2, sub3, sub4 = st.tabs(["Models", "Loras", "Vae", "Controlnet"])
        
        with sub1:
            st.markdown("##### SD 1.5 Checkpoints")
            
            # Sample models - replace with your actual model list
            models = [
                "D5K6.0",
                "PornMaster-Pro V10.1-VAE-inpainting", 
                "Merged amateurs - Mixed Amateurs",
                "epicRealism pureEvolution InPainting - v1.0",
                "PornMaster-Pro FULL-V4-inpainting",
                "PornMaster-Pro FULL-V5-inpainting",
                "Merged Amateurs - Mixed Amateurs | Inpainting Model - v1.0",
                "fuego_v2_tk14_fp26(1)",
                "LazyMix+ (Real Amateur Nudes) - v4.0",
                "SD.15-AcornMoarMindBreak"
            ]
            
            # Create 2 columns for compact display
            col1, col2 = st.columns(2)
            
            for idx, model in enumerate(models):
                with col1 if idx % 2 == 0 else col2:
                    # Toggle button for each model
                    selected = st.toggle(
                        label=model,
                        value=False,
                        key=f"sd15_{model}"
                    )
                    if selected and model not in st.session_state.selected_models:
                        st.session_state.selected_models.append(model)
                    elif not selected and model in st.session_state.selected_models:
                        st.session_state.selected_models.remove(model)
        
        with sub2:
            st.info("SD 1.5 LoRAs")
        
        with sub3:
            st.info("SD 1.5 VAE")
        
        with sub4:
            st.info("SD 1.5 ControlNet")
    
    with tab_sdxl:
        sub1, sub2, sub3, sub4 = st.tabs(["Models", "Loras", "Vae", "Controlnet"])
        
        with sub1:
            st.markdown("##### SDXL Checkpoints")
            
            sdxl_models = [
                "realvisxlV40_v40Bakedvae",
                "sd_xl_base_1.0",
                "DreamShaperXL",
                "JuggernautXL",
                "RealismEngineSDXL"
            ]
            
            col1, col2 = st.columns(2)
            
            for idx, model in enumerate(sdxl_models):
                with col1 if idx % 2 == 0 else col2:
                    selected = st.toggle(
                        label=model,
                        value=False,
                        key=f"sdxl_{model}"
                    )
                    if selected and model not in st.session_state.selected_models:
                        st.session_state.selected_models.append(model)
                    elif not selected and model in st.session_state.selected_models:
                        st.session_state.selected_models.remove(model)
    
    with tab_pony:
        sub1, sub2 = st.tabs(["Models", "Loras"])
        
        with sub1:
            st.markdown("##### Pony Checkpoints")
            
            pony_models = ["ponyDiffusionV6XL"]
            
            for model in pony_models:
                selected = st.toggle(
                    label=model,
                    value=False,
                    key=f"pony_{model}"
                )
    
    with tab_misc:
        ext1, ext2, ext3, ext4 = st.tabs(["SAM", "ADetailer", "Upscaler", "Reactor"])
        
        with ext1:
            st.markdown("##### SAM Models")
            sam_models = [
                "sam_vit_h_4b8939.pth",
                "sam_vit_l_0b3195.pth",
                "sam_vit_b_01ec64.pth"
            ]
            
            for model in sam_models:
                st.toggle(label=model, value=False, key=f"sam_{model}")
        
        with ext2:
            st.markdown("##### ADetailer Models")
            adet_models = [
                "face_yolov8n.pt",
                "face_yolov8s.pt",
                "hand_yolov8n.pt"
            ]
            
            for model in adet_models:
                st.toggle(label=model, value=False, key=f"adet_{model}")

with tab2:
    st.markdown("### Model Browser")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        search = st.text_input("Search", placeholder="Search models...")
    with col2:
        model_type = st.selectbox("Type", ["All", "Checkpoint", "LORA"])
    with col3:
        if st.button("Search"):
            st.info(f"Searching for: {search}")

with tab3:
    st.markdown("### Settings")
    
    webui = st.radio("WebUI Type", ["Forge", "ComfyUI", "A1111"], horizontal=True)
    port = st.number_input("Port", value=7860, min_value=1000, max_value=65535)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        api_enabled = st.toggle("Enable API", value=False)
    with col2:
        auto_launch = st.toggle("Auto-launch", value=True)
    with col3:
        share = st.toggle("Share", value=False)

# Download section
st.markdown("---")
col1, col2 = st.columns([1, 5])

with col1:
    count = len(st.session_state.selected_models)
    if st.button(f"📥 Download ({count})"):
        if count > 0:
            st.success(f"Downloading {count} models...")
        else:
            st.warning("No models selected")

with col2:
    # Progress bar
    progress = st.progress(0)

# Output area
st.markdown("---")
st.text_area("Output Console", value="Ready...", height=100)

# Quick actions
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🚀 Launch WebUI"):
        st.success("Launching...")
with col2:
    if st.button("🔄 Refresh"):
        st.rerun()
with col3:
    if st.button("📊 Stats"):
        st.info(f"Selected: {count} models")
with col4:
    if st.button("🧹 Clear"):
        st.session_state.selected_models = []
        st.rerun()