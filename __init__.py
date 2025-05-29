"""
Optimized nodes for ComfyUI
"""

import os
import sys
import logging
from typing import Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dp_nodes_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DP_Nodes')

# Initialize empty mappings
NODE_CLASS_MAPPINGS: Dict[str, Any] = {}
NODE_DISPLAY_NAME_MAPPINGS: Dict[str, Any] = {}

try:
    logger.info("Starting DP Nodes initialization...")
    
    # Core dependencies
    try:
        import folder_paths
        import torch
        from PIL import Image, ImageDraw, ImageFont
        import numpy as np
        logger.info("Core dependencies loaded successfully")
    except ImportError as e:
        logger.error(f"Failed to import core dependencies: {str(e)}")
        raise

    # Import all nodes from the nodes folder
    from .nodes.dp_5_find_and_replace import DP_5_Find_And_Replace
    from .nodes.dp_5_image_and_mask_switch import DP_5_Image_And_Mask_Switch
    from .nodes.dp_add_background_to_png import DP_Add_Background_To_Png
    from .nodes.dp_add_weight_to_string_sdxl import DP_Add_Weight_To_String_Sdxl
    from .nodes.dp_advanced_sampler import DP_Advanced_Sampler
    from .nodes.dp_advanced_weight_string_sdxl import DP_Advanced_Weight_String_Sdxl
    from .nodes.dp_animation_calculator_10inputs import DP_Animation_Calculator_10_Inputs
    from .nodes.dp_animation_calculator_5inputs import DP_Animation_Calculator_5_Inputs
    from .nodes.dp_animation_int_selectors import (
        DP_Transition_Frames_Selector,
        DP_Diff_Int_8step_selector,
        DP_Int_0_1000,
        DP_Draggable_Int_1step,
        DP_Draggable_Int_4step,
        DP_Draggable_Int_8step
    )
    from .nodes.dp_art_style_generator import DP_Art_Style_Generator
    from .nodes.dp_big_letters import DP_Big_Letters
    from .nodes.dp_broken_token import DP_Broken_Token
    from .nodes.dp_checkpoint_loader import DP_Load_Checkpoint_With_Info
    from .nodes.dp_clean_prompt import DP_clean_prompt
    from .nodes.dp_clean_prompt_travel import DP_Clean_Prompt_Travel
    from .nodes.dp_condition_mixer import DP_Condition_Switch
    from .nodes.dp_controlnet import DP_ControlNetApplyAdvanced, DP_Load_Controlnet_Model_With_Name
    from .nodes.dp_crazy_prompt_mixer import DP_Crazy_Prompt_Mixer
    from .nodes.dp_crazy_random_prompt_generator import DP_Random_Crazy_Prompt_Generator
    from .nodes.dp_create_simple_json import DP_create_json_file
    from .nodes.dp_custom_aspect_ratio import DP_Custom_Aspect_Ratio
    from .nodes.dp_draggable_floats import (
        DP_Draggable_Floats_1,
        DP_Draggable_Floats_2,
        DP_Draggable_Floats_3
    )
    from .nodes.dp_extract_mask import DP_Extract_Mask
    from .nodes.dp_fast_slow_motion import DP_FastSlowMotion
    from .nodes.dp_five_lora_loader import DP_Five_Lora
    from .nodes.dp_five_lora_loader_random import DP_Five_Lora_Random
    from .nodes.dp_float_stepper import DP_Float_Stepper
    from .nodes.dp_get_seed_from_image import DP_Get_Seed_From_Image
    from .nodes.dp_Image_Grid_To_Image import DP_Image_Grid_To_Image
    from .nodes.dp_Image_Slice_To_Grid import DP_Image_Slice_To_Grid
    from .nodes.dp_if_int_condition import DP_IF_INT_CONDITION
    from .nodes.dp_image_color_analyzer import DP_Image_Color_Analyzer
    from .nodes.dp_image_color_analyzer_small import DP_Image_Color_Analyzer_Small
    from .nodes.dp_image_color_effect import DP_Image_Color_Effect
    from .nodes.dp_image_effect_processor import DP_Image_Effect_Processor
    from .nodes.dp_image_effect_processor_small import DP_Image_Effect_Processor_Small
    from .nodes.dp_image_empty_latent_switch_flux import DP_Image_Empty_Latent_Switch_Flux
    from .nodes.dp_image_empty_latent_switch_sdxl import DP_Image_Empty_Latent_Switch_SDXL
    from .nodes.dp_image_slide_show import DP_Image_Slide_Show
    from .nodes.dp_image_strip import DP_Image_Strip
    from .nodes.dp_image_strip_edege_mask import DP_Strip_Edge_Masks
    from .nodes.dp_image_switch import (
        DP_Image_And_String_Pairs_Switch,
        DP_3_Images_Switch_Or_Batch,
        DP_5_Images_Switch_Or_Batch,
        DP_10_Images_Switch_Or_Batch
    )
    from .nodes.dp_image_to_pixelgrid import DP_Image_To_Pixelgrid
    from .nodes.dp_latent_split import DP_Latent_Split
    from .nodes.dp_line_cycler import DP_Line_Cycler
    from .nodes.dp_load_image import DP_Load_Image_Effects
    from .nodes.dp_load_image_folder import DP_Load_Image_Folder
    from .nodes.dp_load_image_minimal import DP_Load_Image_Minimal
    from .nodes.dp_load_image_small import DP_Load_Image_Effects_Small
    from .nodes.dp_load_image_v2 import DP_Load_Image_V2
    from .nodes.dp_load_image_with_seed import DP_Load_Image_With_Seed
    from .nodes.dp_logo_animator import DP_Logo_Animator
    from .nodes.dp_lora_random_strength_controller import DP_Lora_Random_Strength_Controller
    from .nodes.dp_lora_strength_controller import DP_Lora_Strength_Controller
    from .nodes.dp_mask_settings import DP_Mask_Settings
    from .nodes.dp_model_loaders import DP_Load_UNET_With_Info, DP_Load_Dual_CLIP_With_Info
    from .nodes.dp_place_image import DP_Place_Image
    from .nodes.dp_prompt_inverter import DP_Prompt_Inverter
    from .nodes.dp_prompt_manager_small import DP_Prompt_Manager_Small, DP_Prompt_Mode_Controller
    from .nodes.dp_prompt_styler import DP_Prompt_Styler
    from .nodes.dp_prompt_token_compressor import DP_SmartPromptCompressor
    from .nodes.dp_prompt_travel_prompt import DP_Prompt_Travel_Prompt
    from .nodes.dp_quick_model_link import DP_symlink
    from .nodes.dp_random_character import DP_Random_Character
    from .nodes.dp_random_logo_style_generator import DP_Random_Logo_Style_Generator
    from .nodes.dp_random_min_max import DP_random_min_max
    from .nodes.dp_random_mode_controller import DP_Random_Mode_Switch, DP_Random_Mode_Controller
    from .nodes.dp_random_psychedelic_punk_generator import DP_Random_Psychedelic_Punk_Generator
    from .nodes.dp_randon_superhero_prompt_generator import DP_Random_Superhero_Prompt_Generator
    from .nodes.dp_random_vehicle_generator import DP_Random_Vehicle_Generator
    from .nodes.dp_resize_image_and_mask import DP_Resize_Image_And_Mask
    from .nodes.dp_sampler_with_info import DP_Sampler_With_Info
    from .nodes.dp_save_image_v2 import DP_Save_Image_V2
    from .nodes.dp_save_preview_image import DP_Save_Preview_Image
    from .nodes.dp_simple_width_height import DP_Aspect_Ratio_Picker
    from .nodes.dp_stitch_2_images import DP_Stitch_2_Images
    from .nodes.dp_string_switches import (
        DP_10_String_Switch_Or_Connect,
        DP_3_String_Switch_Or_Connect,
        DP_5_String_Switch_Or_Connect
    )
    from .nodes.dp_string_with_switch import (
        DP_2_String_Switch,
        DP_String_Text,
        DP_String_Text_With_Sdxl_Weight
    )
    from .nodes.dp_switch_controller import DP_Switch_Controller
    from .nodes.dp_text_preview import DP_Text_Preview
    from .nodes.dp_versatile_prompt_subjects_generator import DP_Versatile_Prompt_Subjects_Generator
    from .nodes.dp_video_effect_sender_receiver import DP_Video_Effect_Sender, DP_Video_Effect_Receiver
    from .nodes.dp_video_flicker import DP_Video_Flicker
    from .nodes.dp_video_looper import DP_Video_Looper
    from .nodes.dp_video_transition import DP_Video_Transition
    from .nodes.dp_words import DP_Words

    # Update NODE_CLASS_MAPPINGS with all nodes
    NODE_CLASS_MAPPINGS.update({
        "DP 5 Find And Replace": DP_5_Find_And_Replace,
        "DP 5 Image And Mask Switch": DP_5_Image_And_Mask_Switch,
        "DP 10 String Switch Or Connect": DP_10_String_Switch_Or_Connect,
        "DP 3 String Switch Or Connect": DP_3_String_Switch_Or_Connect,
        "DP 5 String Switch Or Connect": DP_5_String_Switch_Or_Connect,
        "DP Add Background To Png": DP_Add_Background_To_Png,
        "DP Add Weight To String Sdxl": DP_Add_Weight_To_String_Sdxl,
        "DP Advanced Sampler": DP_Advanced_Sampler,
        "DP Advanced Weight String Sdxl": DP_Advanced_Weight_String_Sdxl,
        "DP Animation Calculator 10 Inputs": DP_Animation_Calculator_10_Inputs,
        "DP Animation Calculator 5 Inputs": DP_Animation_Calculator_5_Inputs,
        "DP Art Style Generator": DP_Art_Style_Generator,
        "DP Big Letters": DP_Big_Letters,
        "DP Broken Token": DP_Broken_Token,
        "DP Clean Prompt": DP_clean_prompt,
        "DP Clean Prompt Travel": DP_Clean_Prompt_Travel,
        "DP Condition Switch": DP_Condition_Switch,
        "DP ControlNet Apply Advanced": DP_ControlNetApplyAdvanced,
        "DP Crazy Prompt Mixer": DP_Crazy_Prompt_Mixer,
        "DP Create Json File": DP_create_json_file,
        "DP Custom Aspect Ratio": DP_Custom_Aspect_Ratio,
        "DP Diff Int 8step Selector": DP_Diff_Int_8step_selector,
        "DP Draggable Floats 1": DP_Draggable_Floats_1,
        "DP Draggable Floats 2": DP_Draggable_Floats_2,
        "DP Draggable Floats 3": DP_Draggable_Floats_3,
        "DP Draggable Int 1step": DP_Draggable_Int_1step,
        "DP Draggable Int 4step": DP_Draggable_Int_4step,
        "DP Draggable Int 8step": DP_Draggable_Int_8step,
        "DP Extract Mask": DP_Extract_Mask,
        "DP Fast Slow Motion": DP_FastSlowMotion,
        "DP Five Lora": DP_Five_Lora,
        "DP Five Lora Random": DP_Five_Lora_Random,
        "DP Float Stepper": DP_Float_Stepper,
        "DP Get Seed From Image": DP_Get_Seed_From_Image,
        "DP Image And String Pairs Switch": DP_Image_And_String_Pairs_Switch,
        "DP Image Color Analyzer": DP_Image_Color_Analyzer,
        "DP Image Color Analyzer Small": DP_Image_Color_Analyzer_Small,
        "DP Image Color Effect": DP_Image_Color_Effect,
        "DP Image Effect Processor": DP_Image_Effect_Processor,
        "DP Image Effect Processor Small": DP_Image_Effect_Processor_Small,
        "DP Image Empty Latent Switch Flux": DP_Image_Empty_Latent_Switch_Flux,
        "DP Image Empty Latent Switch SDXL": DP_Image_Empty_Latent_Switch_SDXL,
        "DP Image Grid To Image": DP_Image_Grid_To_Image,
        "DP Image Slide Show": DP_Image_Slide_Show,
        "DP Image Slice To Grid": DP_Image_Slice_To_Grid,
        "DP Image Strip": DP_Image_Strip,
        "DP Image To Pixelgrid": DP_Image_To_Pixelgrid,
        "DP Latent Split": DP_Latent_Split,
        "DP Line Cycler": DP_Line_Cycler,
        "DP Load Checkpoint With Info": DP_Load_Checkpoint_With_Info,
        "DP Load Controlnet Model With Name": DP_Load_Controlnet_Model_With_Name,
        "DP Load Dual CLIP With Info": DP_Load_Dual_CLIP_With_Info,
        "DP Load Image Effects": DP_Load_Image_Effects,
        "DP Load Image Effects Small": DP_Load_Image_Effects_Small,
        "DP Load Image Folder": DP_Load_Image_Folder,
        "DP Load Image Minimal": DP_Load_Image_Minimal,
        "DP Load Image V2": DP_Load_Image_V2,
        "DP Load Image With Seed": DP_Load_Image_With_Seed,
        "DP Load UNET With Info": DP_Load_UNET_With_Info,
        "DP Logo Animator": DP_Logo_Animator,
        "DP Lora Random Strength Controller": DP_Lora_Random_Strength_Controller,
        "DP Lora Strength Controller": DP_Lora_Strength_Controller,
        "DP Mask Settings": DP_Mask_Settings,
        "DP Place Image": DP_Place_Image,
        "DP Prompt Inverter": DP_Prompt_Inverter,
        "DP Prompt Manager Small": DP_Prompt_Manager_Small,
        "DP Prompt Mode Controller": DP_Prompt_Mode_Controller,
        "DP Prompt Styler": DP_Prompt_Styler,
        "DP Prompt Token Compressor": DP_SmartPromptCompressor,
        "DP Prompt Travel Prompt": DP_Prompt_Travel_Prompt,
        "DP Random Character": DP_Random_Character,
        "DP Random Crazy Prompt Generator": DP_Random_Crazy_Prompt_Generator,
        "DP Random Logo Style Generator": DP_Random_Logo_Style_Generator,
        "DP Random Min Max": DP_random_min_max,
        "DP Random Mode Controller": DP_Random_Mode_Controller,
        "DP Random Mode Switch": DP_Random_Mode_Switch,
        "DP Random Psychedelic Punk Generator": DP_Random_Psychedelic_Punk_Generator,
        "DP Random Superhero Prompt Generator": DP_Random_Superhero_Prompt_Generator,
        "DP Random Vehicle Generator": DP_Random_Vehicle_Generator,
        "DP Resize Image And Mask": DP_Resize_Image_And_Mask,
        "DP Sampler With Info": DP_Sampler_With_Info,
        "DP Save Image V2": DP_Save_Image_V2,
        "DP Save Preview Image": DP_Save_Preview_Image,
        "DP Aspect Ratio Picker": DP_Aspect_Ratio_Picker,
        "DP Stitch 2 Images": DP_Stitch_2_Images,
        "DP Strip Edge Masks": DP_Strip_Edge_Masks,
        "DP String Text": DP_String_Text,
        "DP String Text With Sdxl Weight": DP_String_Text_With_Sdxl_Weight,
        "DP Switch Controller": DP_Switch_Controller,
        "DP Text Preview": DP_Text_Preview,
        "DP Transition Frames Selector": DP_Transition_Frames_Selector,
        "DP Versatile Prompt Subjects Generator": DP_Versatile_Prompt_Subjects_Generator,
        "DP Video Effect Receiver": DP_Video_Effect_Receiver,
        "DP Video Effect Sender": DP_Video_Effect_Sender,
        "DP Video Flicker": DP_Video_Flicker,
        "DP Video Looper": DP_Video_Looper,
        "DP Video Transition": DP_Video_Transition,
        "DP Words": DP_Words,
        "DP Int 0 1000": DP_Int_0_1000,
        "DP 2 String Switch": DP_2_String_Switch,
        "DP 3 Images Switch Or Batch": DP_3_Images_Switch_Or_Batch,
        "DP 5 Images Switch Or Batch": DP_5_Images_Switch_Or_Batch,
        "DP 10 Images Switch Or Batch": DP_10_Images_Switch_Or_Batch,
        "DP Quick Model Link": DP_symlink,
        "DP IF Int Condition": DP_IF_INT_CONDITION,
    })

    # Update NODE_DISPLAY_NAME_MAPPINGS with all nodes
    NODE_DISPLAY_NAME_MAPPINGS.update({
        "DP 5 Find And Replace": "DP 5 Find And Replace",
        "DP 5 Image And Mask Switch": "DP 5 Image And Mask Switch",
        "DP 10 String Switch Or Connect": "DP 10 String Switch Or Connect",
        "DP 3 String Switch Or Connect": "DP 3 String Switch Or Connect",
        "DP 5 String Switch Or Connect": "DP 5 String Switch Or Connect",
        "DP Add Background To Png": "DP Add Background To PNG",
        "DP Add Weight To String Sdxl": "DP Add Weight To String SDXL",
        "DP Advanced Sampler": "DP Advanced Sampler",
        "DP Advanced Weight String Sdxl": "DP Advanced Weight String SDXL",
        "DP Animation Calculator 10 Inputs": "DP Animation Calculator 10 Inputs",
        "DP Animation Calculator 5 Inputs": "DP Animation Calculator 5 Inputs",
        "DP Art Style Generator": "DP Art Style Generator",
        "DP Big Letters": "DP Big Letters",
        "DP Broken Token": "DP Broken Token",
        "DP Clean Prompt": "DP Clean Prompt",
        "DP Clean Prompt Travel": "DP Clean Prompt Travel",
        "DP Condition Switch": "DP Condition Switch",
        "DP ControlNet Apply Advanced": "DP ControlNet Apply Advanced",
        "DP Crazy Prompt Mixer": "DP Crazy Prompt Mixer",
        "DP Create Json File": "DP Create JSON File",
        "DP Custom Aspect Ratio": "DP Custom Aspect Ratio",
        "DP Diff Int 8step Selector": "DP Diff Int 8step Selector",
        "DP Draggable Floats 1": "DP Draggable Floats 1",
        "DP Draggable Floats 2": "DP Draggable Floats 2",
        "DP Draggable Floats 3": "DP Draggable Floats 3",
        "DP Draggable Int 1step": "DP Draggable Int 1step",
        "DP Draggable Int 4step": "DP Draggable Int 4step",
        "DP Draggable Int 8step": "DP Draggable Int 8step",
        "DP Extract Mask": "DP Extract Mask",
        "DP Fast Slow Motion": "DP Fast Slow Motion",
        "DP Five Lora": "DP Five Lora",
        "DP Five Lora Random": "DP Five Lora Random",
        "DP Float Stepper": "DP Float Stepper",
        "DP Get Seed From Image": "DP Get Seed From Image",
        "DP Image And String Pairs Switch": "DP Image And String Pairs Switch",
        "DP Image Color Analyzer": "DP Image Color Analyzer",
        "DP Image Color Analyzer Small": "DP Image Color Analyzer Small",
        "DP Image Color Effect": "DP Image Color Effect",
        "DP Image Effect Processor": "DP Image Effect Processor",
        "DP Image Effect Processor Small": "DP Image Effect Processor Small",
        "DP Image Empty Latent Switch Flux": "DP Image Empty Latent Switch Flux",
        "DP Image Empty Latent Switch SDXL": "DP Image Empty Latent Switch SDXL",
        "DP Image Grid To Image": "DP Image Grid To Image",
        "DP Image Slide Show": "DP Image Slide Show",
        "DP Image Slice To Grid": "DP Image Slice To Grid",
        "DP Image Strip": "DP Image Strip",
        "DP Image To Pixelgrid": "DP Image To Pixelgrid",
        "DP Latent Split": "DP Latent Split",
        "DP Line Cycler": "DP Line Cycler",
        "DP Load Checkpoint With Info": "DP Load Checkpoint With Info",
        "DP Load Controlnet Model With Name": "DP Load ControlNet Model With Name",
        "DP Load Dual CLIP With Info": "DP Load Dual CLIP With Info",
        "DP Load Image Effects": "DP Load Image Effects",
        "DP Load Image Effects Small": "DP Load Image Effects Small",
        "DP Load Image Folder": "DP Load Image Folder",
        "DP Load Image Minimal": "DP Load Image Minimal",
        "DP Load Image V2": "DP Load Image V2",
        "DP Load Image With Seed": "DP Load Image With Seed",
        "DP Load UNET With Info": "DP Load UNET With Info",
        "DP Logo Animator": "DP Logo Animator",
        "DP Lora Random Strength Controller": "DP Lora Random Strength Controller",
        "DP Lora Strength Controller": "DP Lora Strength Controller",
        "DP Mask Settings": "DP Mask Settings",
        "DP Place Image": "DP Place Image",
        "DP Prompt Inverter": "DP Prompt Inverter",
        "DP Prompt Manager Small": "DP Prompt Manager Small",
        "DP Prompt Mode Controller": "DP Prompt Mode Controller",
        "DP Prompt Styler": "DP Prompt Styler",
        "DP Prompt Token Compressor": "DP Prompt Token Compressor",
        "DP Prompt Travel Prompt": "DP Prompt Travel Prompt",
        "DP Random Character": "DP Random Character",
        "DP Random Crazy Prompt Generator": "DP Random Crazy Prompt Generator",
        "DP Random Logo Style Generator": "DP Random Logo Style Generator",
        "DP Random Min Max": "DP Random Min Max",
        "DP Random Mode Controller": "DP Random Mode Controller",
        "DP Random Mode Switch": "DP Random Mode Switch",
        "DP Random Psychedelic Punk Generator": "DP Random Psychedelic Punk Generator",
        "DP Random Superhero Prompt Generator": "DP Random Superhero Prompt Generator",
        "DP Random Vehicle Generator": "DP Random Vehicle Generator",
        "DP Resize Image And Mask": "DP Resize Image And Mask",
        "DP Sampler With Info": "DP Sampler With Info",
        "DP Save Image V2": "DP Save Image V2",
        "DP Save Preview Image": "DP Save Preview Image",
        "DP Aspect Ratio Picker": "DP Aspect Ratio Picker",
        "DP Stitch 2 Images": "DP Stitch 2 Images",
        "DP Strip Edge Masks": "DP Strip Edge Masks",
        "DP String Text": "DP String Text",
        "DP String Text With Sdxl Weight": "DP String Text With SDXL Weight",
        "DP Switch Controller": "DP Switch Controller",
        "DP Text Preview": "DP Text Preview",
        "DP Transition Frames Selector": "DP Transition Frames Selector",
        "DP Versatile Prompt Subjects Generator": "DP Versatile Prompt Subjects Generator",
        "DP Video Effect Receiver": "DP Video Effect Receiver",
        "DP Video Effect Sender": "DP Video Effect Sender",
        "DP Video Flicker": "DP Video Flicker",
        "DP Video Looper": "DP Video Looper",
        "DP Video Transition": "DP Video Transition",
        "DP Words": "DP Words",
        "DP Int 0 1000": "DP Int 0 1000",
        "DP 2 String Switch": "DP 2 String Switch",
        "DP 3 Images Switch Or Batch": "DP 3 Images Switch Or Batch",
        "DP 5 Images Switch Or Batch": "DP 5 Images Switch Or Batch",
        "DP 10 Images Switch Or Batch": "DP 10 Images Switch Or Batch",
        "DP Quick Model Link": "DP Quick Model Link",
        "DP IF Int Condition": "IF Int Condition",
    })

    # Set web directory
    WEB_DIRECTORY = "js"
    logger.info(f"Web directory set to: {WEB_DIRECTORY}")
    
    # Log successful initialization
    logger.info(f"Successfully loaded {len(NODE_CLASS_MAPPINGS)} nodes")
    logger.debug(f"Loaded nodes: {list(NODE_CLASS_MAPPINGS.keys())}")

except Exception as e:
    logger.critical(f"Critical error initializing DP_Nodes: {str(e)}", exc_info=True)
    logger.critical(f"Stack trace:", exc_info=True)
    # Provide minimal valid node mappings even in case of error
    NODE_CLASS_MAPPINGS = {}
    NODE_DISPLAY_NAME_MAPPINGS = {}
    WEB_DIRECTORY = "./js"

# Make sure these are always defined
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']