"""
VAE (Variational Autoencoder) model data for SD-DarkMaster-Pro
Popular VAEs for better color and detail reproduction
"""

# SD1.5 VAEs
sd15_vaes = {
    "vae-ft-mse-840000-ema-pruned": {
        "url": "https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors",
        "size": "335MB",
        "base": "SD1.5",
        "description": "Standard VAE, good color reproduction",
        "recommended": True
    },
    "kl-f8-anime2": {
        "url": "https://huggingface.co/hakurei/waifu-diffusion-v1-4/resolve/main/vae/kl-f8-anime2.ckpt",
        "size": "395MB",
        "base": "SD1.5",
        "description": "Anime-focused VAE, vibrant colors",
        "recommended": False
    },
    "blessed2.vae": {
        "url": "https://huggingface.co/NoCrypt/blessed_vae/resolve/main/blessed2.vae.safetensors",
        "size": "335MB",
        "base": "SD1.5",
        "description": "Enhanced contrast and saturation",
        "recommended": False
    },
    "ClearVAE": {
        "url": "https://civitai.com/api/download/models/88156",
        "size": "335MB",
        "base": "SD1.5",
        "description": "Cleaner outputs, less artifacts",
        "recommended": True
    },
    "Anything-V3.0-vae": {
        "url": "https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/Anything-V3.0.vae.pt",
        "size": "335MB",
        "base": "SD1.5",
        "description": "Optimized for Anything model series",
        "recommended": False
    }
}

# SDXL VAEs
sdxl_vaes = {
    "sdxl-vae-fp16-fix": {
        "url": "https://huggingface.co/madebyollin/sdxl-vae-fp16-fix/resolve/main/sdxl_vae.safetensors",
        "size": "335MB",
        "base": "SDXL",
        "description": "Fixed FP16 VAE for SDXL, prevents NaN errors",
        "recommended": True
    },
    "sdxl-vae": {
        "url": "https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors",
        "size": "335MB",
        "base": "SDXL",
        "description": "Original SDXL VAE",
        "recommended": False
    }
}

# All VAEs combined
vae_list = {
    "None (Use Model's VAE)": {
        "url": None,
        "size": "0MB",
        "base": "All",
        "description": "Use the VAE included with the model",
        "recommended": True
    },
    **{f"sd15_{k}": {**v, "category": "SD1.5"} for k, v in sd15_vaes.items()},
    **{f"sdxl_{k}": {**v, "category": "SDXL"} for k, v in sdxl_vaes.items()}
}