import base64
import os
import requests

"""
Generate masked images using the Stability AI API.
How to directly hit the API without using the SDK.

This function sends a POST request to the Stability AI API to generate masked images based on the provided inputs.
It requires the following environment variables to be set:
- API_HOST: The API host URL.
- STABILITY_API_KEY: The Stability API key.

Returns:
None
"""

# set the Stability key
STABILITY_KEY = 'sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# set the parameters for the generation
prompt = "woman's face, asian, not ugly"  
steps = 50
cfg_scale = 7
samples = 10
mask_source = "MASK_IMAGE_BLACK"
    # MASK_IMAGE_WHITE | MASK_IMAGE_BLACK | INIT_IMAGE_ALPHA
clip_guidance_preset = "NONE"
    # NONE | FAST_BLUE | FAST_GREEN | NONE | SIMPLE | SLOW | SLOWER | SLOWEST
style_preset = "photographic"
    # 3d-model, analog-film, anime, cinematic, comic-book, digital-art 
    # enhance, fantasy-art, isometric, line-art, low-poly, modeling-compound 
    # neon-punk, origami, photographic, pixel-art, tile-texture
seed = 44332211

# Function to generate masked images
def generate_masked_images():
    engine_id = "stable-diffusion-xl-1024-v1-0"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    api_key = os.getenv("STABILITY_API_KEY", STABILITY_KEY)

    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/image-to-image/masking",
        headers={
            "Accept": 'application/json',
            "Authorization": f"Bearer {api_key}"
        },
        files={
            'init_image': open("./original.png", 'rb'),
            'mask_image': open("./blurred_mask.png", 'rb'),
        },
        data={
            "text_prompts[0][text]": prompt,
            "cfg_scale": cfg_scale,
            "samples": samples,
            "steps": steps,
            "mask_source": mask_source,
            "clip_guidance_preset": clip_guidance_preset,
            "style_preset": style_preset,
            "seed": seed,
        }
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    for i, image in enumerate(data["artifacts"]):
        with open(f"./{seed}_{i}.png", "wb") as f:
            f.write(base64.b64decode(image["base64"]))

# Call the function to generate the masked images
generate_masked_images()
