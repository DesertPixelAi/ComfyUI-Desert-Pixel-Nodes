@echo off
mkdir animation
mkdir image_processing
mkdir text_prompt
mkdir utility
mkdir switch
mkdir generators
mkdir lora
mkdir models

:: Animation & Transition Nodes
echo # Animation Calculator > animation/animation_calculator.md
echo # Fast/Slow Motion > animation/fast_slow_motion.md
echo # Image Slide Show > animation/image_slide_show.md
echo # Logo Animator > animation/logo_animator.md
echo # Video Effects Sender/Receiver > animation/video_effects_sender_receiver.md
echo # Video Flicker > animation/video_flicker.md
echo # Video Transition > animation/video_transition.md

:: Image Processing Nodes
echo # Add Background To PNG > image_processing/add_background_to_png.md
echo # Big Letters > image_processing/big_letters.md
echo # Color Analyzer > image_processing/color_analyzer.md
echo # Image Color Effect > image_processing/image_color_effect.md
echo # Image Effect Processor > image_processing/image_effect_processor.md
echo # Image Loaders > image_processing/image_loaders.md
echo # Image Strip > image_processing/image_strip.md
echo # Mask Settings > image_processing/mask_settings.md
echo # Save Preview Image > image_processing/save_preview_image.md
echo # Strip Edge Masks > image_processing/strip_edge_masks.md

:: Text & Prompt Nodes
echo # Add Weight To String SDXL > text_prompt/add_weight_string_sdxl.md
echo # Advanced Weight String SDXL > text_prompt/advanced_weight_string_sdxl.md
echo # Broken Token > text_prompt/broken_token.md
echo # Clean Prompt > text_prompt/clean_prompt.md
echo # Line Cycler > text_prompt/line_cycler.md
echo # Prompt Inverter > text_prompt/prompt_inverter.md
echo # Prompt Manager > text_prompt/prompt_manager.md
echo # Prompt Mode Controller > text_prompt/prompt_mode_controller.md
echo # Prompt Styler > text_prompt/prompt_styler.md
echo # Prompt Token Compressor > text_prompt/prompt_token_compressor.md
echo # Text Preview > text_prompt/text_preview.md

:: Control & Utility Nodes
echo # Aspect Ratio Picker > utility/aspect_ratio.md
echo # Combo Controller > utility/combo_controller.md
echo # Condition Switch > utility/condition_switch.md
echo # Create JSON > utility/create_json.md
echo # Custom Aspect Ratio > utility/custom_aspect_ratio.md
echo # Draggable Floats > utility/float_controls.md
echo # Empty Latent Switch > utility/empty_latent_switch.md
echo # Latent Split > utility/latent_split.md
echo # Quick Link > utility/quick_link.md
echo # Random Min/Max > utility/random_minmax.md
echo # Switch Controller > utility/switch_controller.md

:: String & Image Switch Nodes
echo # 2/3/5/10 String Switch > switch/string_switch.md
echo # 3/5/10 Images Switch > switch/image_switch.md
echo # Image And String Pairs Switch > switch/image_string_pairs_switch.md
echo # String Text With SDXL Weight > switch/string_text_sdxl_weight.md

:: Generator Nodes
echo # Art Style Generator > generators/art_style_generator.md
echo # Crazy Prompt Generator > generators/crazy_prompt_generator.md
echo # Random Character > generators/random_char.md
echo # Random Logo Style > generators/random_logo_style.md
echo # Random Psychedelic Punk > generators/random_psychedelic_punk.md
echo # Random Superhero > generators/random_superhero.md
echo # Random Vehicle > generators/random_vehicle.md

:: LoRA & Model Nodes
echo # Five LoRA > lora/five_lora.md
echo # Five LoRA Random > lora/five_lora_random.md
echo # LoRA Strength Controller > lora/lora_strength_controller.md
echo # Load Checkpoint With Info > models/load_checkpoint.md
echo # Load ControlNet Model > models/load_controlnet.md
echo # Load Dual CLIP > models/load_dual_clip.md
echo # Load UNET > models/load_unet.md

echo Documentation structure created successfully!
pause