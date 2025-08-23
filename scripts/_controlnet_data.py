"""
ControlNet model data for SD-DarkMaster-Pro
Popular ControlNet models for pose, depth, and style control
"""

# SD1.5 ControlNets
sd15_controlnets = {
    "OpenPose": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "pose",
        "description": "Human pose detection and control"
    },
    "Canny": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "edge",
        "description": "Edge detection for structure control"
    },
    "Depth": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "depth",
        "description": "Depth map control"
    },
    "LineArt": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "line",
        "description": "Line art extraction and control"
    },
    "LineArt Anime": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "line",
        "description": "Anime-style line art control"
    },
    "SoftEdge": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "edge",
        "description": "Soft edge detection"
    },
    "Scribble": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "scribble",
        "description": "Rough sketch control"
    },
    "MLSD": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "line",
        "description": "Straight line detection"
    },
    "Normal": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "normal",
        "description": "Normal map control"
    },
    "Tile": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "tile",
        "description": "Detail enhancement and upscaling"
    },
    "Inpaint": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "inpaint",
        "description": "Inpainting control"
    },
    "IP2P": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "ip2p",
        "description": "Image-to-image prompting"
    },
    "Shuffle": {
        "url": "https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle.pth",
        "size": "1.45GB",
        "base": "SD1.5",
        "type": "shuffle",
        "description": "Style transfer via shuffling"
    }
}

# SDXL ControlNets
sdxl_controlnets = {
    "SDXL Canny": {
        "url": "https://huggingface.co/diffusers/controlnet-canny-sdxl-1.0/resolve/main/diffusion_pytorch_model.fp16.safetensors",
        "size": "2.5GB",
        "base": "SDXL",
        "type": "edge",
        "description": "Canny edge control for SDXL"
    },
    "SDXL Depth": {
        "url": "https://huggingface.co/diffusers/controlnet-depth-sdxl-1.0/resolve/main/diffusion_pytorch_model.fp16.safetensors",
        "size": "2.5GB",
        "base": "SDXL",
        "type": "depth",
        "description": "Depth control for SDXL"
    },
    "SDXL OpenPose": {
        "url": "https://huggingface.co/thibaud/controlnet-openpose-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors",
        "size": "2.5GB",
        "base": "SDXL",
        "type": "pose",
        "description": "OpenPose control for SDXL"
    }
}

# All ControlNets combined
controlnet_list = {
    **{f"sd15_{k}": {**v, "category": "SD1.5"} for k, v in sd15_controlnets.items()},
    **{f"sdxl_{k}": {**v, "category": "SDXL"} for k, v in sdxl_controlnets.items()}
}