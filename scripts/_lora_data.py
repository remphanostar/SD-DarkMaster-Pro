"""
LoRA (Low-Rank Adaptation) model data for SD-DarkMaster-Pro
Popular LoRAs for SD1.5 and SDXL models
"""

# SD1.5 LoRAs
sd15_loras = {
    # Popular Style LoRAs
    "Detail Tweaker LoRA": {
        "url": "https://civitai.com/api/download/models/62833",
        "size": "144MB",
        "base": "SD1.5",
        "trigger": "add_detail, detail_slider",
        "strength": 0.7,
        "description": "Enhance or reduce details in images"
    },
    "Anime Lineart Style": {
        "url": "https://civitai.com/api/download/models/13904",
        "size": "144MB",
        "base": "SD1.5",
        "trigger": "lineart, monochrome",
        "strength": 0.8,
        "description": "Creates clean lineart/manga style"
    },
    "LowRA (Dark Theme)": {
        "url": "https://civitai.com/api/download/models/63006",
        "size": "144MB",
        "base": "SD1.5",
        "trigger": "dark theme",
        "strength": 0.6,
        "description": "Darker, moodier images"
    },
    "Film Grain": {
        "url": "https://civitai.com/api/download/models/89923",
        "size": "144MB",
        "base": "SD1.5",
        "trigger": "film grain",
        "strength": 0.5,
        "description": "Adds realistic film grain"
    },
    "Pixel Art Style": {
        "url": "https://civitai.com/api/download/models/10638",
        "size": "144MB",
        "base": "SD1.5",
        "trigger": "pixel art",
        "strength": 1.0,
        "description": "8-bit/16-bit pixel art style"
    },
    
    # Popular Character LoRAs
    "RPG Character": {
        "url": "https://civitai.com/api/download/models/84576",
        "size": "144MB",
        "base": "SD1.5",
        "trigger": "rpg character",
        "strength": 0.8,
        "description": "Fantasy RPG character styles"
    },
    "Cyberpunk Style": {
        "url": "https://civitai.com/api/download/models/77121",
        "size": "144MB",
        "base": "SD1.5",
        "trigger": "cyberpunk style",
        "strength": 0.7,
        "description": "Cyberpunk aesthetic"
    },
    
    # Utility LoRAs
    "Hands Fix": {
        "url": "https://civitai.com/api/download/models/90872",
        "size": "144MB",
        "base": "SD1.5",
        "trigger": "perfect hands",
        "strength": 0.5,
        "description": "Improves hand generation"
    },
    "Eye Detail": {
        "url": "https://civitai.com/api/download/models/91234",
        "size": "144MB",
        "base": "SD1.5",
        "trigger": "detailed eyes",
        "strength": 0.6,
        "description": "Enhances eye details"
    }
}

# SDXL LoRAs
sdxl_loras = {
    "SDXL Detail Enhancer": {
        "url": "https://civitai.com/api/download/models/135867",
        "size": "198MB",
        "base": "SDXL",
        "trigger": "add detail xl",
        "strength": 0.7,
        "description": "SDXL version of detail enhancer"
    },
    "SDXL Film Photography": {
        "url": "https://civitai.com/api/download/models/182967",
        "size": "198MB",
        "base": "SDXL",
        "trigger": "film photography",
        "strength": 0.6,
        "description": "Cinematic film look for SDXL"
    },
    "SDXL Anime Style": {
        "url": "https://civitai.com/api/download/models/178961",
        "size": "198MB",
        "base": "SDXL",
        "trigger": "anime style xl",
        "strength": 0.8,
        "description": "Anime/manga style for SDXL"
    },
    "SDXL Offset Noise": {
        "url": "https://civitai.com/api/download/models/166373",
        "size": "198MB",
        "base": "SDXL",
        "trigger": "offset noise",
        "strength": 0.4,
        "description": "Better contrast and lighting"
    },
    "SDXL HDR": {
        "url": "https://civitai.com/api/download/models/178123",
        "size": "198MB",
        "base": "SDXL",
        "trigger": "hdr, high dynamic range",
        "strength": 0.5,
        "description": "HDR photography effect"
    }
}

# Pony LoRAs
pony_loras = {
    "Pony Style Enhancer": {
        "url": "https://civitai.com/api/download/models/290640",
        "size": "144MB",
        "base": "Pony",
        "trigger": "score_9, score_8_up",
        "strength": 0.8,
        "description": "Enhances Pony Diffusion outputs"
    },
    "Pony Anime Mix": {
        "url": "https://civitai.com/api/download/models/293991",
        "size": "144MB",
        "base": "Pony",
        "trigger": "anime_style_pony",
        "strength": 0.7,
        "description": "Anime style for Pony models"
    }
}

# All LoRAs combined
lora_list = {
    **{f"sd15_{k}": {**v, "category": "SD1.5"} for k, v in sd15_loras.items()},
    **{f"sdxl_{k}": {**v, "category": "SDXL"} for k, v in sdxl_loras.items()},
    **{f"pony_{k}": {**v, "category": "Pony"} for k, v in pony_loras.items()}
}