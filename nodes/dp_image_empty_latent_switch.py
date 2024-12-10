# ComfyUI custom nodes by DreamProphet
# DP Image or Empty Latent Switch Node implementation

import torch
from nodes import EmptyLatentImage, VAEEncode

class DP_Image_Empty_Latent_Switch:
    def __init__(self):
        self.vae_encode = VAEEncode()
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": (["empty_latent_image", "image_input_1", "image_input_2", "image_input_3", "image_input_4", "image_input_5"], {"default": "empty_latent_image"}),
                "img2img_strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "width": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 8192}),
            },
            "optional": {
                "Image_Input_01": ("IMAGE",),
                "Image_Input_02": ("IMAGE",),
                "Image_Input_03": ("IMAGE",),
                "Image_Input_04": ("IMAGE",),
                "Image_Input_05": ("IMAGE",),
                "vae": ("VAE",),
            }
        }

    RETURN_TYPES = ("LATENT", "FLOAT", "FLOAT", "INT")
    RETURN_NAMES = ("LATENT", "img2img_strength", "denoise", "selected_switch")
    FUNCTION = "switch"
    CATEGORY = "DP/utils"

    def switch(self, switch, img2img_strength, denoise, width, height, 
               Image_Input_01=None, Image_Input_02=None,
               Image_Input_03=None, Image_Input_04=None,
               Image_Input_05=None, vae=None):
        
        # Initialize outputs
        selected_image = None
        output_strength = img2img_strength
        output_denoise = denoise
        output_latent = None
        
        # Convert switch value to number for return value
        switch_mapping = {
            "empty_latent_image": 1,
            "image_input_1": 2,
            "image_input_2": 3,
            "image_input_3": 4,
            "image_input_4": 5,
            "image_input_5": 6
        }
        switch_number = switch_mapping[switch]
        
        # Handle switch cases
        if switch == "empty_latent_image":
            # Text to image mode - empty latent only
            output_strength = 0.0
            output_denoise = 1.0  # Force denoise to 1.0 in txt2img mode
            output_latent = EmptyLatentImage().generate(width, height, 1)[0]
        else:
            # Image to image mode - select appropriate image and encode it
            if switch == "image_input_1" and Image_Input_01 is not None:
                selected_image = Image_Input_01
            elif switch == "image_input_2" and Image_Input_02 is not None:
                selected_image = Image_Input_02
            elif switch == "image_input_3" and Image_Input_03 is not None:
                selected_image = Image_Input_03
            elif switch == "image_input_4" and Image_Input_04 is not None:
                selected_image = Image_Input_04
            elif switch == "image_input_5" and Image_Input_05 is not None:
                selected_image = Image_Input_05
            
            # If we have a selected image and VAE, encode it
            if selected_image is not None and vae is not None:
                output_latent = self.vae_encode.encode(vae, selected_image)[0]
            else:
                # Fallback to empty latent if no image selected or no VAE
                output_latent = EmptyLatentImage().generate(width, height, 1)[0]
            
        return (output_latent, output_strength, output_denoise, switch_number)

NODE_CLASS_MAPPINGS = {
    "DP_Image_Empty_Latent_Switch": DP_Image_Empty_Latent_Switch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_Image_Empty_Latent_Switch": "DP Image Empty Latent Switch"
}