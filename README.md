# stabilityai_i2i_masking
Generate masked images using the Stability AI API. (SDK / without SDK)

## Summary

 This script generates masked images using the Stability AI API. It sends a POST request to the Stability AI API to generate masked images based on the provided inputs. The program requires the following environment variables to be set:
 - API_HOST: The API host URL.
 - STABILITY_API_KEY: The Stability API key.

 The script defines a function called generate_masked_images that sends a POST request to the Stability AI API to generate masked images based on the provided inputs. The function requires the following parameters:
 - prompt: The prompt for the generation.
 - steps: The number of steps for the generation.
 - cfg_scale: The cfg_scale parameter for the generation.
 - samples: The number of samples for the generation.
 - mask_source: The mask_source parameter for the generation.
 - clip_guidance_preset: The clip_guidance_preset parameter for the generation.
 - style_preset: The style_preset parameter for the generation.
 - seed: The seed parameter for the generation.

https://platform.stability.ai/docs/api-reference#tag/v1generation/operation/masking
https://platform.stability.ai/docs/features/inpainting#Python

## How to use

1. pip install (using SDK only)
    ```console
    pip install stability-sdk
    ```

1. put image and mask image

    * image.png
    ![image](https://platform.stability.ai/Inpainting-C1.png)

    * mask.png
    ![image](https://platform.stability.ai/Inpainting-C2.png)

    * mask.png to feathered mask (using SDK only)
    ![image](https://platform.stability.ai/Inpainting-C3.png)

1. run script
    ```console
    py .\api_image-to-image_masking.py
    ```
    or
    ```console
    py .\sdk_image-to-image_masking.py
    ```

1. resulting image written to <seed>.png
    ![image](https://platform.stability.ai/Inpainting-C4.png)
