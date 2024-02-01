"""
This script uses the Stability SDK to generate an image based on a given prompt and mask.
The generated image is saved as a PNG file.

The script performs the following steps:
0. `pip install stability-sdk`
1. Set the environment variables for the Stability host and key.
2. Create an instance of the StabilityInference class.
3. Open the original image and the blurred mask image using PIL.
4. Apply Gaussian blur to the mask image.
5. Generate the image using the Stability API with the specified parameters.
6. Iterate over the generated responses and artifacts.
7. If the finish reason is FILTER, raise a warning indicating that the request could not be processed.
8. If the artifact type is IMAGE, save the image as a PNG file using the artifact's seed as the filename.

The generated image is saved as a PNG file in the current working directory.

https://platform.stability.ai/docs/features/inpainting#Python
"""

import os
import io
import warnings

from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from torchvision.transforms import GaussianBlur

# set the Stability key
STABILITY_KEY = 'sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# set the parameters for the generation
prompt = "woman's face, asian, not ugly"  
start_schedule = 0.8
steps = 60
seed = 44332211
cfg_scale = 7

# set the environment variables for the Stability host and key
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
os.environ['STABILITY_KEY'] = STABILITY_KEY

# create an instance of the StabilityInference class
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], 
    verbose=False, 
    engine="stable-diffusion-xl-1024-v1-0", 
)

# open the original image and the blurred mask image
img = Image.open('./image.png')
mask_i = Image.open('./mask.png')

blur = GaussianBlur(11,20)
mask = blur(mask_i)

# generate the image using the Stability API
answers = stability_api.generate(
    prompt=prompt,
    init_image=img,
    mask_image=mask,
    start_schedule=start_schedule,
    seed=seed,
    steps=steps, 
    cfg_scale=cfg_scale, 
    width=1024, #fixed width and height
    height=1024, 
    sampler=generation.SAMPLER_K_EULER_ANCESTRAL 
)

# iterate over the generated responses and artifacts
for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            warnings.warn(
                "Your request activated the API's safety filters and could not be processed."
                "Please modify the prompt and try again.")
        if artifact.type == generation.ARTIFACT_IMAGE:
            global img2
            img2 = Image.open(io.BytesIO(artifact.binary))
            img2.save(str(artifact.seed)+ ".png") 
