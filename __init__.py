"""
Optimized nodes for ComfyUI
"""

import os
import sys
import folder_paths
import torch

def cleanup():
    try:
        # Clear CUDA cache
        torch.cuda.empty_cache()
        
        # Clear model caches
        DP_UNET_Loader_Optimized.cleanup_cache()
        DP_VAE_Loader_Optimized.cleanup_cache()
        DP_Dual_CLIP_Loader_Optimized.cleanup_cache()
    except:
        pass

if hasattr(sys, 'cleanup_handlers'):
    sys.cleanup_handlers.append(cleanup)

class PreloadManager:
    @staticmethod
    async def preload_models(unet_name=None, vae_name=None, clip_names=None):
        if unet_name:
            DP_UNET_Loader_Optimized.preload_weights(unet_name)
        if vae_name:
            DP_VAE_Loader_Optimized.preload_weights(vae_name)
        if clip_names:
            DP_Dual_CLIP_Loader_Optimized.preload_weights(*clip_names)

# Apply global PyTorch optimizations
if torch.cuda.is_available():
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    torch.backends.cudnn.benchmark = True

from .nodes.dp_big_letter import DP_Big_Letters
from .nodes.dp_broken_token import DPBrokenToken
from .nodes.dp_clean_prompt import DP_clean_prompt
from .nodes.dp_create_simple_json import DP_create_json_file
from .nodes.dp_fast_slow_motion import DP_FastSlowMotion
from .nodes.dp_image_color_analyzer import DP_Image_Color_Analyzer
from .nodes.dp_image_empty_latent_switch import DP_Image_Empty_Latent_Switch
from .nodes.dp_load_image_kit import DP_Image_Loader_Medium, DP_Image_Loader_Big, DP_Image_Loader_Small
from .nodes.dp_multi_styler import DpPromptStyler
from .nodes.dp_quick_model_link import DP_symlink
from .nodes.dp_randomals import DP_Random_Char
from .nodes.dp_simple_width_height import DPAspectRatioPicker
from .nodes.dp_smart_image_saver import DP_smart_saver
from .nodes.dp_video_effect_sender_receiver import DPVideoEffectSender, DPVideoEffectReceiver
from .nodes.dp_video_flicker import DPVideoFlicker
from .nodes.dp_video_transition import DP_Video_Transition
from .nodes.dp_zero_one_floats import DP_float_0_1, DP_2floats_0_1, DP_3floats_0_1
from .nodes.dp_animation_calculator_5inputs import DP_Animation_Calculator_5Inputs
from .nodes.dp_random_min_max import DP_random_min_max
from .nodes.dp_logo_animator import DPLogoAnimator
from .nodes.dp_crazy_random_prompt_generator import Dp_Random_Crazy_Prompt_Generator as DPCrazyPromptGenerator
from .nodes.dp_image_slide_show import DP_Image_Slide_Show
from .nodes.dp_five_lora_loader import DP_Five_Lora
from .nodes.dp_five_lora_loader_random import DP_Five_Lora_Random
from .nodes.dp_prompt_random_switch import DP_Prompt_Random_Switch
from .nodes.dp_optimized_vae_decode import DP_VAE_Decode_Optimized
from .nodes.dp_optimized_vae_encode import DP_VAE_Encode_Optimized
from .nodes.dp_optimized_unet_loader import DP_UNET_Loader_Optimized
from .nodes.dp_optimized_vae_loader import DP_VAE_Loader_Optimized
from .nodes.dp_optimized_dual_clip_loader import DP_Dual_CLIP_Loader_Optimized

NODE_CLASS_MAPPINGS = {
    # DP/image category
    "DP_Image_Loader_Big": DP_Image_Loader_Big,
    "DP_Image_Loader_Medium": DP_Image_Loader_Medium,
    "DP_Image_Loader_Small": DP_Image_Loader_Small,
    "DP_Big_Letters": DP_Big_Letters,
    "DP_Image_Empty_Latent_Switch": DP_Image_Empty_Latent_Switch,
    "DP_Smart_Saver": DP_smart_saver,
    "DP_Image_Color_Analyzer": DP_Image_Color_Analyzer,

    # DP/animation category
    "DP_Logo_Animator": DPLogoAnimator,
    "DP_Video_Effect_Sender": DPVideoEffectSender,
    "DP_Video_Effect_Receiver": DPVideoEffectReceiver,
    "DP_Video_Flicker": DPVideoFlicker,
    "DP_Video_Transition": DP_Video_Transition,
    "DP_Animation_Calculator_5Inputs": DP_Animation_Calculator_5Inputs,
    "DP_Fast_Slow_Motion": DP_FastSlowMotion,

    # DP/text category
    "DP_Prompt_Styler": DpPromptStyler,
    "DP_Clean_Prompt": DP_clean_prompt,
    "DP_Broken_Token": DPBrokenToken,
    "DP_Random_Char": DP_Random_Char,

    # DP/utils category
    "DP_Float_0_1": DP_float_0_1,
    "DP_2Floats_0_1": DP_2floats_0_1,
    "DP_3Floats_0_1": DP_3floats_0_1,
    "DP_Create_JSON": DP_create_json_file,
    "DP_Quick_Link": DP_symlink,
    "DP_Aspect_Ratio": DPAspectRatioPicker,
    "DP_Random_MinMax": DP_random_min_max,
    "DP_Prompt_Random_Switch": DP_Prompt_Random_Switch,

    # DP/prompt category (new category for prompt-related nodes)
    "DP_Crazy_Prompt": DPCrazyPromptGenerator,
    "DP_Image_Slide_Show": DP_Image_Slide_Show,

    # DP/loaders category
    "DP_Five_Lora": DP_Five_Lora,
    "DP_Five_Lora_Random": DP_Five_Lora_Random,

    # DP/optimized category
    "DP_VAE_Decode_Optimized": DP_VAE_Decode_Optimized,
    "DP_VAE_Encode_Optimized": DP_VAE_Encode_Optimized,
    "DP_UNET_Loader_Optimized": DP_UNET_Loader_Optimized,
    "DP_VAE_Loader_Optimized": DP_VAE_Loader_Optimized,
    "DP_Dual_CLIP_Loader_Optimized": DP_Dual_CLIP_Loader_Optimized,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # DP/image category
    "DP_Image_Loader_Big": "DP Image Loader (Big)",
    "DP_Image_Loader_Medium": "DP Image Loader (Medium)",
    "DP_Image_Loader_Small": "DP Image Loader (Small)",
    "DP_Big_Letters": "DP Big Letters",
    "DP_Image_Empty_Latent_Switch": "DP Image/Empty Latent Switch",
    "DP_Smart_Saver": "DP Smart Image Saver",
    "DP_Image_Color_Analyzer": "DP Image Color Analyzer",

    # DP/animation category
    "DP_Logo_Animator": "DP Logo Animator",
    "DP_Video_Effect_Sender": "DP Video Effect Sender",
    "DP_Video_Effect_Receiver": "DP Video Effect Receiver",
    "DP_Video_Flicker": "DP Video Flicker",
    "DP_Video_Transition": "DP Video Transition",
    "DP_Animation_Calculator_5Inputs": "DP Animation Calculator (5 Inputs)",
    "DP_Fast_Slow_Motion": "DP Fast/Slow Motion",

    # DP/text category
    "DP_Prompt_Styler": "DP Prompt Styler",
    "DP_Clean_Prompt": "DP Clean Prompt",
    "DP_Broken_Token": "DP Broken Token",
    "DP_Random_Char": "DP Random Character",

    # DP/utils category
    "DP_Float_0_1": "DP Float 0-1",
    "DP_2Floats_0_1": "DP 2 Floats 0-1",
    "DP_3Floats_0_1": "DP 3 Floats 0-1",
    "DP_Create_JSON": "DP Create JSON",
    "DP_Quick_Link": "DP Quick Model Link",
    "DP_Aspect_Ratio": "DP Aspect Ratio Picker",
    "DP_Random_MinMax": "DP Random Min/Max",
    "DP_Prompt_Random_Switch": "DP Prompt Random Switch",

    # DP/prompt category
    "DP_Crazy_Prompt": "DP Crazy Prompt Generator",
    "DP_Image_Slide_Show": "DP Image Slide Show",

    # DP/loaders category
    "DP_Five_Lora": "DP Five LoRA Loader",
    "DP_Five_Lora_Random": "DP Five LoRA Loader (Random)",

    # DP/optimized category
    "DP_VAE_Decode_Optimized": "DP VAE Decode (Optimized)",
    "DP_VAE_Encode_Optimized": "DP VAE Encode (Optimized)",
    "DP_UNET_Loader_Optimized": "DP Load UNET (Optimized)",
    "DP_VAE_Loader_Optimized": "DP Load VAE (Optimized)",
    "DP_Dual_CLIP_Loader_Optimized": "DP Load Dual CLIP (Optimized)",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']