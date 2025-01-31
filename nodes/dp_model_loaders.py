import torch
import folder_paths
import os
import comfy.sd
import comfy.utils

class DP_Load_UNET_With_Info:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { 
            "unet_name": (folder_paths.get_filename_list("diffusion_models"), ),
            "weight_dtype": (["default", "fp8_e4m3fn", "fp8_e4m3fn_fast", "fp8_e5m2"],)
        }}
    RETURN_TYPES = ("MODEL", "STRING")
    RETURN_NAMES = ("model", "model_info")
    FUNCTION = "load_unet"

    CATEGORY = "Desert Pixel/loaders"

    def load_unet(self, unet_name, weight_dtype):
        model_options = {}
        if weight_dtype == "fp8_e4m3fn":
            model_options["dtype"] = torch.float8_e4m3fn
        elif weight_dtype == "fp8_e4m3fn_fast":
            model_options["dtype"] = torch.float8_e4m3fn
            model_options["fp8_optimizations"] = True
        elif weight_dtype == "fp8_e5m2":
            model_options["dtype"] = torch.float8_e5m2

        unet_path = folder_paths.get_full_path_or_raise("diffusion_models", unet_name)
        model = comfy.sd.load_diffusion_model(unet_path, model_options=model_options)
        
        # Get model name without extension
        model_name = os.path.splitext(unet_name)[0]
        info = f"unet name: {model_name}"
        
        return (model, info)

class DP_Load_Dual_CLIP_With_Info:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { 
            "clip_name1": (folder_paths.get_filename_list("text_encoders"), ),
            "clip_name2": (folder_paths.get_filename_list("text_encoders"), ),
            "type": (["sdxl", "sd3", "flux", "hunyuan_video"], ),
        },
        "optional": {
            "device": (["default", "cpu"], {"advanced": True}),
        }}
    RETURN_TYPES = ("CLIP", "STRING")
    RETURN_NAMES = ("clip", "model_info")
    FUNCTION = "load_clip"

    CATEGORY = "Desert Pixel/loaders"

    DESCRIPTION = "[Recipes]\n\nsdxl: clip-l, clip-g\nsd3: clip-l, clip-g / clip-l, t5 / clip-g, t5\nflux: clip-l, t5"

    def load_clip(self, clip_name1, clip_name2, type, device="default"):
        clip_path1 = folder_paths.get_full_path_or_raise("text_encoders", clip_name1)
        clip_path2 = folder_paths.get_full_path_or_raise("text_encoders", clip_name2)
        
        if type == "sdxl":
            clip_type = comfy.sd.CLIPType.STABLE_DIFFUSION
        elif type == "sd3":
            clip_type = comfy.sd.CLIPType.SD3
        elif type == "flux":
            clip_type = comfy.sd.CLIPType.FLUX
        elif type == "hunyuan_video":
            clip_type = comfy.sd.CLIPType.HUNYUAN_VIDEO

        model_options = {}
        if device == "cpu":
            model_options["load_device"] = model_options["offload_device"] = torch.device("cpu")

        clip = comfy.sd.load_clip(ckpt_paths=[clip_path1, clip_path2], embedding_directory=folder_paths.get_folder_paths("embeddings"), clip_type=clip_type, model_options=model_options)
        
        # Get model names without extensions
        clip1_name = os.path.splitext(clip_name1)[0]
        clip2_name = os.path.splitext(clip_name2)[0]
        info = f"clip1: {clip1_name}\nclip2: {clip2_name}"
        
        return (clip, info) 