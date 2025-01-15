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

    # First import the Big Letters node as it's a base for others
    from .nodes.dp_big_letters import DP_Big_Letters
    logger.info("Successfully imported DP_Big_Letters")

    # Then import the rest of the nodes
    # Animation nodes
    from .nodes.dp_animation_calculator_5inputs import DP_Animation_Calculator_5_Inputs
    from .nodes.dp_animation_calculator_10inputs import DP_Animation_Calculator_10_Inputs
    from .nodes.dp_animation_int_selectors import (
        DP_Transition_Frames_Selector, 
        DP_Diff_Int_8step_selector,
        DP_Int_0_1000,
        DP_Int_0_1000_4_Step,
        DP_Int_0_1000_8_Step
    )
    
    # Image processing nodes
    from .nodes.dp_image_color_analyzer import DP_Image_Color_Analyzer
    from .nodes.dp_image_color_effect import DP_Image_Color_Effect
    from .nodes.dp_image_effect_processor import DP_Image_Effect_Processor
    from .nodes.dp_image_empty_latent_switch_flux import DP_Image_Empty_Latent_Switch_Flux
    from .nodes.dp_image_empty_latent_switch_sdxl import DP_Image_Empty_Latent_Switch_SDXL
    from .nodes.dp_image_slide_show import DP_Image_Slide_Show
    from .nodes.dp_image_strip import DP_Image_Strip
    from .nodes.dp_image_strip_edege_mask import DP_Strip_Edge_Masks
    from .nodes.dp_load_image import DP_Load_Image_Effects
    from .nodes.dp_load_image_small import DP_Load_Image_Effects_Small
    from .nodes.dp_save_preview_image import DP_Save_Preview_Image
    from .nodes.dp_load_image_minimal import DP_Load_Image_Minimal
    
    # Text and prompt nodes
    from .nodes.dp_prompt_inverter import DP_Prompt_Inverter
    from .nodes.dp_broken_token import DP_Broken_Token
    from .nodes.dp_clean_prompt import DP_clean_prompt
    from .nodes.dp_prompt_styler import DP_Prompt_Styler
    from .nodes.dp_prompt_manager import DP_Prompt_Manager, DP_Prompt_Mode_Controller
    from .nodes.dp_prompt_token_compressor import DP_SmartPromptCompressor
    from .nodes.dp_text_preview import DP_Text_Preview
    from .nodes.dp_strings_connector import DP_Strings_Connector
    
    # Control and utility nodes
    from .nodes.dp_combo_controller import DP_Combo_Controller
    from .nodes.dp_create_simple_json import DP_create_json_file
    from .nodes.dp_draggable_floats import (
        DP_Draggable_Floats_1, 
        DP_Draggable_Floats_2, 
        DP_Draggable_Floats_3
    )
    from .nodes.dp_lora_strength_controller import DP_Lora_Strength_Controller
    from .nodes.dp_lora_random_strength_controller import DP_Lora_Random_Strength_Controller
    from .nodes.dp_quick_model_link import DP_symlink
    from .nodes.dp_random_min_max import DP_random_min_max
    from .nodes.dp_simple_width_height import DP_Aspect_Ratio_Picker
    from .nodes.dp_string_with_switch import (
        DP_String_With_Switch, 
        DP_2_String_Switch, 
        DP_String_Text,
        DP_String_Text_With_Weight,
        DP_5_String_Switch,
        DP_10_String_Switch
    )
    from .nodes.dp_switch_controller import DP_Switch_Controller
    
    # Video nodes
    from .nodes.dp_fast_slow_motion import DP_FastSlowMotion
    from .nodes.dp_video_effect_sender_receiver import DP_Video_Effect_Sender, DP_Video_Effect_Receiver
    from .nodes.dp_video_flicker import DP_Video_Flicker
    from .nodes.dp_video_looper import DP_Video_Looper
    from .nodes.dp_video_transition import DP_Video_Transition
    
    # Logo and animation nodes
    from .nodes.dp_logo_animator import DP_Logo_Animator
    from .nodes.dp_logo_animator_advanced import DP_Logo_Animator_Advanced
    
    # Generator nodes
    from .nodes.dp_crazy_random_prompt_generator import DP_Random_Crazy_Prompt_Generator
    from .nodes.dp_random_character import DP_Random_Character
    from .nodes.dp_random_logo_style_generator import DP_Random_Logo_Style_Generator
    from .nodes.dp_randon_superhero_prompt_generator import DP_Random_Superhero_Prompt_Generator
    
    # LoRA nodes
    from .nodes.dp_five_lora_loader import DP_Five_Lora
    from .nodes.dp_five_lora_loader_random import DP_Five_Lora_Random

    # Import the new generator
    from .nodes.dp_random_psychedelic_punk_generator import DP_Random_Psychedelic_Punk_Generator

    # Import the crazy prompt mixer
    from .nodes.dp_crazy_prompt_mixer import DP_Crazy_Prompt_Mixer

    # In the imports section, add:
    from .nodes.dp_prompt_manager_small import DP_Prompt_Manager_Small
    from .nodes.dp_lora_strength_stepper import DP_Lora_Strength_Stepper

    # Add this import near the other imports:
    from .nodes.dp_random_mode_controller import DP_Random_Mode_Switch, DP_Random_Mode_Controller

    # Add this import near the other imports:
    from .nodes.dp_custom_aspect_ratio import DP_Custom_Aspect_Ratio

    # Add this import near the other imports:
    from .nodes.dp_condition_mixer import DP_Condition_Mixer

    # Add this import near the other imports:
    from .nodes.dp_image_color_analyzer_small import DP_Image_Color_Analyzer_Small

    # Add this import near the other imports:
    from .nodes.dp_image_switch import (
        DP_Image_Switch_3_Inputs,
        DP_Image_Switch_5_Inputs,
        DP_Image_Switch_10_Inputs,
        DP_Image_And_String_Pairs_Switch
    )

    # Add import near the other imports (around line 115):
    from .nodes.dp_art_style_generator import DP_Art_Style_Generator

    # Add this import near the other imports:
    from .nodes.dp_add_weight_to_string_sdxl import DP_Add_Weight_To_String_Sdxl

    # Add this import near the other imports:
    from .nodes.dp_advanced_weight_string_sdxl import DP_Advanced_Weight_String_Sdxl

    # Add this import near the other generator nodes (around line 116):
    from .nodes.dp_random_vehicle_generator import DP_Random_Vehicle_Generator

    # Add this import near the other imports:
    from .nodes.dp_clean_prompt_travel import DP_Clean_Prompt_Travel

    # Add this import near the other imports:
    from .nodes.dp_image_effect_processor_small import DP_Image_Effect_Processor_Small

    # Add these imports near the other imports:
    from .nodes.dp_line_cycler import DP_Line_Cycler
    from .nodes.dp_5_find_and_replace import DP_5_Find_And_Replace

    # Add this import near the other imports:
    from .nodes.dp_mask_settings import DP_Mask_Settings

    # Add this import near the other imports:
    from .nodes.dp_sampler import DP_Sampler

    # Add this import near the other imports:
    from .nodes.dp_controlnet import DP_ControlNetApplyAdvanced, DP_Load_Controlnet_Model_With_Name

    # Add this import near the other imports:
    from .nodes.dp_checkpoint_loader import DP_Load_Checkpoint_With_Info

    # Add this import near the other imports:
    from .nodes.dp_model_loaders import DP_Load_UNET_With_Info, DP_Load_Dual_CLIP_With_Info

    # Add this to the NODE_CLASS_MAPPINGS dictionary:
    NODE_CLASS_MAPPINGS.update({
        "DP ControlNet Apply Advanced": DP_ControlNetApplyAdvanced,
        "DP Load Controlnet Model With Name": DP_Load_Controlnet_Model_With_Name,
        "DP Load Checkpoint With Info": DP_Load_Checkpoint_With_Info,
        "DP Load UNET With Info": DP_Load_UNET_With_Info,
        "DP Load Dual CLIP With Info": DP_Load_Dual_CLIP_With_Info,
    })

    # Add this to NODE_DISPLAY_NAME_MAPPINGS:
    NODE_DISPLAY_NAME_MAPPINGS["DP Load Controlnet Model With Name"] = "DP Load ControlNet Model With Name"
    NODE_DISPLAY_NAME_MAPPINGS["DP Load Checkpoint With Info"] = "DP Load Checkpoint With Info"
    NODE_DISPLAY_NAME_MAPPINGS["DP Load UNET With Info"] = "DP Load UNET With Info"
    NODE_DISPLAY_NAME_MAPPINGS["DP Load Dual CLIP With Info"] = "DP Load Dual CLIP With Info"

    # Add all nodes to the mappings
    NODE_CLASS_MAPPINGS = {
        "DP Big Letters": DP_Big_Letters,
        "DP Animation Calculator 5 Inputs": DP_Animation_Calculator_5_Inputs,
        "DP Transition Frames Selector": DP_Transition_Frames_Selector,
        "DP Diff Int 8step Selector": DP_Diff_Int_8step_selector,
        "DP Broken Token": DP_Broken_Token,
        "DP Clean Prompt": DP_clean_prompt,
        "DP Clean Prompt Travel": DP_Clean_Prompt_Travel,
        "DP Combo Controller": DP_Combo_Controller,
        "DP Create Json File": DP_create_json_file,
        "DP Random Crazy Prompt Generator": DP_Random_Crazy_Prompt_Generator,
        "DP Draggable Floats 1": DP_Draggable_Floats_1,
        "DP Draggable Floats 2": DP_Draggable_Floats_2,
        "DP Draggable Floats 3": DP_Draggable_Floats_3,
        "DP Fast Slow Motion": DP_FastSlowMotion,
        "DP Five Lora": DP_Five_Lora,
        "DP Five Lora Random": DP_Five_Lora_Random,
        "DP Image Color Analyzer": DP_Image_Color_Analyzer,
        "DP Image Color Effect": DP_Image_Color_Effect,
        "DP Image Effect Processor": DP_Image_Effect_Processor,
        "DP Image Empty Latent Switch Flux": DP_Image_Empty_Latent_Switch_Flux,
        "DP Image Empty Latent Switch SDXL": DP_Image_Empty_Latent_Switch_SDXL,
        "DP Image Slide Show": DP_Image_Slide_Show,
        "DP Load Image Effects": DP_Load_Image_Effects,
        "DP Load Image Effects Small": DP_Load_Image_Effects_Small,
        "DP Logo Animator": DP_Logo_Animator,
        "DP Logo Animator Advanced": DP_Logo_Animator_Advanced,
        "DP Lora Strength Controller": DP_Lora_Strength_Controller,
        "DP Lora Random Strength Controller": DP_Lora_Random_Strength_Controller,
        "DP Prompt Styler": DP_Prompt_Styler,
        "DP Prompt Manager": DP_Prompt_Manager,
        "DP Prompt Mode Controller": DP_Prompt_Mode_Controller,
        "DP Set New Model Folder Link": DP_symlink,
        "DP Random Character": DP_Random_Character,
        "DP Random Min Max": DP_random_min_max,
        "DP Save Preview Image": DP_Save_Preview_Image,
        "DP Aspect Ratio Picker": DP_Aspect_Ratio_Picker,
        "DP String With Switch": DP_String_With_Switch,
        "DP 2 String Switch": DP_2_String_Switch,
        "DP String Text": DP_String_Text,
        "DP String Text With Weight": DP_String_Text_With_Weight,
        "DP 5 String Switch": DP_5_String_Switch,
        "DP 10 String Switch": DP_10_String_Switch,
        "DP Switch Controller": DP_Switch_Controller,
        "DP Text Preview": DP_Text_Preview,
        "DP Video Effect Sender": DP_Video_Effect_Sender,
        "DP Video Effect Receiver": DP_Video_Effect_Receiver,
        "DP Video Flicker": DP_Video_Flicker,
        "DP Video Looper": DP_Video_Looper,
        "DP Video Transition": DP_Video_Transition,
        "DP Animation Calculator 10 Inputs": DP_Animation_Calculator_10_Inputs,
        "DP Int 0-1000": DP_Int_0_1000,
        "DP Int 0-1000 4 Step": DP_Int_0_1000_4_Step,
        "DP Int 0-1000 8 Step": DP_Int_0_1000_8_Step,
        "DP Image Strip": DP_Image_Strip,
        "DP Strip Edge Masks": DP_Strip_Edge_Masks,
        "DP Prompt Token Compressor": DP_SmartPromptCompressor,
        "DP Random Logo Style Generator": DP_Random_Logo_Style_Generator,
        "DP Random Superhero Prompt Generator": DP_Random_Superhero_Prompt_Generator,
        "DP Random Psychedelic Punk Generator": DP_Random_Psychedelic_Punk_Generator,
        "DP Crazy Prompt Mixer": DP_Crazy_Prompt_Mixer,
        "DP Prompt Inverter": DP_Prompt_Inverter,
        "DP Strings Connector": DP_Strings_Connector,
        "DP Prompt Manager Small": DP_Prompt_Manager_Small,
        "DP Lora Strength Stepper": DP_Lora_Strength_Stepper,
        "DP Random Mode Switch": DP_Random_Mode_Switch,
        "DP Random Mode Controller": DP_Random_Mode_Controller,
        "DP Custom Aspect Ratio": DP_Custom_Aspect_Ratio,
        "DP Condition Mixer": DP_Condition_Mixer,
        "DP Image Color Analyzer Small": DP_Image_Color_Analyzer_Small,
        "DP Image Switch 3": DP_Image_Switch_3_Inputs,
        "DP Image Switch 5": DP_Image_Switch_5_Inputs,
        "DP Image Switch 10": DP_Image_Switch_10_Inputs,
        "DP Art Style Generator": DP_Art_Style_Generator,
        "DP Add Weight To String Sdxl": DP_Add_Weight_To_String_Sdxl,
        "DP Advanced Weight String Sdxl": DP_Advanced_Weight_String_Sdxl,
        "DP Random Vehicle Generator": DP_Random_Vehicle_Generator,
        "DP Load Image Minimal": DP_Load_Image_Minimal,
        "DP Image Effect Processor Small": DP_Image_Effect_Processor_Small,
        "DP Line Cycler": DP_Line_Cycler,
        "DP 5 Find And Replace": DP_5_Find_And_Replace,
        "DP Mask Settings": DP_Mask_Settings,
        "DP Image And String Pairs Switch": DP_Image_And_String_Pairs_Switch,
        "DP Sampler": DP_Sampler,
        "DP ControlNet Apply Advanced": DP_ControlNetApplyAdvanced,
        "DP Load Controlnet Model With Name": DP_Load_Controlnet_Model_With_Name,
        "DP Load Checkpoint With Info": DP_Load_Checkpoint_With_Info,
        "DP Load UNET With Info": DP_Load_UNET_With_Info,
        "DP Load Dual CLIP With Info": DP_Load_Dual_CLIP_With_Info,
    }

    # Create display names
    for key in NODE_CLASS_MAPPINGS:
        display_name = key.replace("Dp ", "DP ")
        NODE_DISPLAY_NAME_MAPPINGS[key] = display_name

    # Update display names
    NODE_DISPLAY_NAME_MAPPINGS["DP Prompt Token Compressor"] = "DP Prompt Token Compressor"
    NODE_DISPLAY_NAME_MAPPINGS["DP Random Psychedelic Punk Generator"] = "DP Random Psychedelic Punk Generator"
    NODE_DISPLAY_NAME_MAPPINGS["DP Crazy Prompt Mixer"] = "DP Crazy Prompt Mixer"
    NODE_DISPLAY_NAME_MAPPINGS["DP Prompt Inverter"] = "DP Prompt Inverter"
    NODE_DISPLAY_NAME_MAPPINGS["DP Strings Connector"] = "DP Strings Connector"
    NODE_DISPLAY_NAME_MAPPINGS["DP 5 String Switch"] = "DP 5 String Switch"
    NODE_DISPLAY_NAME_MAPPINGS["DP 10 String Switch"] = "DP 10 String Switch"
    NODE_DISPLAY_NAME_MAPPINGS["DP Random Mode Switch"] = "DP Random Mode Switch"
    NODE_DISPLAY_NAME_MAPPINGS["DP Random Mode Controller"] = "DP Random Mode Controller"
    NODE_DISPLAY_NAME_MAPPINGS["DP Custom Aspect Ratio"] = "DP Custom Aspect Ratio"
    NODE_DISPLAY_NAME_MAPPINGS["DP Condition Mixer"] = "DP Condition Mixer"
    NODE_DISPLAY_NAME_MAPPINGS["DP Image Color Analyzer Small"] = "DP Image Color Analyzer Small"
    NODE_DISPLAY_NAME_MAPPINGS["DP Image Switch 3"] = "DP Image Switch 3"
    NODE_DISPLAY_NAME_MAPPINGS["DP Image Switch 5"] = "DP Image Switch 5"
    NODE_DISPLAY_NAME_MAPPINGS["DP Image Switch 10"] = "DP Image Switch 10"
    NODE_DISPLAY_NAME_MAPPINGS["DP Art Style Generator"] = "DP Art Style Generator"
    NODE_DISPLAY_NAME_MAPPINGS["DP Add Weight To String Sdxl"] = "DP Add Weight To String SDXL"
    NODE_DISPLAY_NAME_MAPPINGS["DP Advanced Weight String Sdxl"] = "DP Advanced Weight String SDXL"
    NODE_DISPLAY_NAME_MAPPINGS["DP Random Vehicle Generator"] = "DP Random Vehicle Generator"
    NODE_DISPLAY_NAME_MAPPINGS["DP String Text With Weight"] = "DP String Text With Weight"
    NODE_DISPLAY_NAME_MAPPINGS["DP Load Image Minimal"] = "DP Load Image Minimal"
    NODE_DISPLAY_NAME_MAPPINGS["DP Image Effect Processor Small"] = "DP Image Effect Processor Small"
    NODE_DISPLAY_NAME_MAPPINGS["DP Line Cycler"] = "DP Line Cycler"
    NODE_DISPLAY_NAME_MAPPINGS["DP 5 Find And Replace"] = "DP 5 Find And Replace"
    NODE_DISPLAY_NAME_MAPPINGS["DP Mask Settings"] = "DP Mask Settings"
    NODE_DISPLAY_NAME_MAPPINGS["DP Image And String Pairs Switch"] = "DP Image And String Pairs Switch"
    NODE_DISPLAY_NAME_MAPPINGS["DP Sampler"] = "DP Sampler"

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