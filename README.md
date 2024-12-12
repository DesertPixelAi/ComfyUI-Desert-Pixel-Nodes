# ComfyUI Custom Nodes by Desert Pixel

A collection of custom nodes for ComfyUI focused on animation, image processing, and workflow optimization.

## Features

### Animation & Video
- **Animation Calculator (5 Inputs)**: Complex animation timing calculator
- **Fast/Slow Motion**: Control video playback speed
- **Image Slide Show**: Create blend mode transitions
- **Logo Animator**: Create animated logos
- **Video Effects**: 
  - Sender/Receiver system for effect application
  - Flicker effects
  - Transition effects

### Image Processing
- **Big Letters**: Create text-based images
- **Color Analyzer**: Analyze and generate color palettes
- **Smart Image Saver**: Enhanced image saving with metadata
- **Image Effects**: Various image processing effects
  - Small Loader: Basic effects
  - Medium Loader: Extended effects
  - Big Loader: Full effect suite

### Utility Nodes
- **Random Min/Max**: Generate random numbers with control
- **Random Characters**: Generate random characters/strings
- **Aspect Ratio Picker**: Easy aspect ratio selection
- **Clean Prompt**: Clean and format prompt text
- **Multi Styler**: Apply multiple styles to prompts
- **Zero-One Floats**: Simple float input/output controls
- **Five LoRA**: Load and manage multiple LoRA models
- **Five LoRA Random**: Random strength LoRA loading
- **Empty Latent Switch**: Switch between empty latent and images
- **Quick Link**: Manage model symbolic links
- **Create JSON**: Create formatted JSON files
- **Broken Token**: Analyze and split Flux prompts

## Installation

Clone this repository into your ComfyUI custom_nodes folder:

```bash
git clone https://github.com/DesertPixelAi/ComfyUI-Desert-Pixel-Nodes custom_nodes/desert-pixel-nodes
```

## Node Documentation
For detailed node documentation, see [Documentation](./nodes_documentation/index.md)

### DP_Animation_Calculator_5Inputs
<img src="https://github.com/user-attachments/assets/fa45806e-76f5-4d25-a0a5-8b6d494d9f90" alt="DP_Animation_Calculator_5Inputs_detailed" style="float: left; margin-right: 10px;"/>

A utility node for managing animations with image transitions and prompt scheduling. Helps create timing data for prompt schedules, fade masks, and IP adapter batches. Can generate timing data with or without image inputs, perfect for keyframe-based animations.

### DP_Image_Slide_Show
<img src="https://github.com/user-attachments/assets/c3001c1e-4d57-46fd-9d0f-4a62109a46dd" alt="DP_Image_Slide_Show" style="float: left; margin-right: 10px;"/>

Creates image sequences with customizable blend mode transitions. Supports up to 5 images with various blend modes including Normal Blend, Dissolve, Overlay, Multiply, Screen, and Soft Light. Perfect for creating GIFs and videos with smooth transitions.

### DP_Logo_Animator
<img src="https://github.com/user-attachments/assets/d56d6536-ea7a-4819-98b6-cc5c4b19f5f3" alt="DP_Logo_Animator" style="float: left; margin-right: 10px;"/>

Creates looping animations for logos with smooth scale effects and automatic background handling. Features customizable minimum shrink size and background detection, ideal for creating professional logo animations for video content.

### DP_Video_Effect_Sender & DP_Video_Effect_Receiver
<img src="https://github.com/user-attachments/assets/9b2ef2f5-0888-42c8-8c59-978bd2f43b93" alt="DP_Video_Effect_Sender_reciver" style="float: left; margin-right: 10px;"/>

A paired system for applying effects to specific frames in video sequences. The Sender extracts frames in a pattern for processing, while the Receiver places the processed frames back into their original positions.

### DP_Video_Flicker
<img src="https://github.com/user-attachments/assets/ffe900e0-2cac-445e-8b39-64e77d6f6081" alt="DP_Video_Flicker" style="float: left; margin-right: 10px;"/>

Creates customizable flicker effects for video sequences with up to three flicker points. Features adjustable colors, sizes, and speeds for each flicker effect, perfect for creating dynamic video transitions.

### DP_Video_Transition
<img src="https://github.com/user-attachments/assets/67234ca8-2496-405b-a1a7-3211fb225887" alt="DP_Video_Transition" style="float: left; margin-right: 10px;"/>

Handles video transitions with multiple blend modes and timing controls. Creates smooth transitions between two video sequences with customizable duration and blend effects.

### DP_Smart_Saver
<img src="https://github.com/user-attachments/assets/704ed83f-daa9-46aa-aadc-7e89a3943010" alt="DP_Smart_Saver" style="float: left; margin-right: 10px;"/>

Enhanced image saving with metadata preservation, customizable folder/file naming, and caption text file support. Features preview mode and optional dimension inclusion in filenames.

### DP_Big_Letters
<img src="https://github.com/user-attachments/assets/c40205d0-6327-47f3-b9f0-29fb3d048ef8" alt="DP_Big_Letters" style="float: left; margin-right: 10px;"/>

Creates text-based images by splitting text into individual letters. Features customizable size, padding, font, color, and background settings for each letter.

### DP_Broken_Token
<img src="https://github.com/user-attachments/assets/f9bfacd1-1b87-4225-ab67-12d5804ef2aa" alt="DP_Broken_Token" style="float: left; margin-right: 10px;"/>

Analyzes and splits Flux prompts based on user-defined token counts. Outputs multiple text parts with configurable maximum token limits.

### DP_Clean_Prompt
<img src="https://github.com/user-attachments/assets/678363ab-5a2d-473f-9132-2487152f588b" alt="DP_Clean_Prompt" style="float: left; margin-right: 10px;"/>

Cleans and formats prompt text by removing unnecessary characters and fixing formatting issues for consistent results.

### DP_Create_JSON
<img src="https://github.com/user-attachments/assets/e3c210b5-d718-4b8b-8e9b-c0963497b22b" alt="DP_Create_JSON" style="float: left; margin-right: 10px;"/>

Creates JSON files from structured data with customizable formatting, file naming, and save options. Supports data separation and file overwrite controls.

### DP_Crazy_Prompt
<img src="https://github.com/user-attachments/assets/d5d970b6-0db3-4f02-9769-194807547d52" alt="DP_Crazy_Prompt" style="float: left; margin-right: 10px;"/>

Generates creative prompt combinations from predefined categories including styles, subjects, composition, lighting, color palettes, and atmospheres.

### DP_Image_Color_Analyzer
<img src="https://github.com/user-attachments/assets/bf90ffac-3925-40ed-9873-2ea3a7d42d1c" alt="DP_Image_Color_Analyzer" style="float: left; margin-right: 10px;"/>

Analyzes image colors and generates detailed color descriptions including RGB values, hex codes, and overall theme detection. Creates color palettes with customizable number of colors.

### DP_Fast_Slow_Motion
<img src="https://github.com/user-attachments/assets/b64a26ea-54ad-421a-a8bf-a573389fbae9" alt="DP_Fast_Slow_Motion" style="float: left; margin-right: 10px;"/>

Controls video playback speed by manipulating frame sequences. Features adjustable speed factors for creating fast or slow motion effects within specified frame ranges.

### DP_Five_Lora
<img src="https://github.com/user-attachments/assets/7de97607-c5cc-4186-a9c0-250ee55548b4" alt="DP_Five_Lora" style="float: left; margin-right: 10px;"/>

Loads up to five LoRA models with individual strength control. Provides detailed information about applied LoRAs and their settings.

### DP_Five_Lora_Random
<img src="https://github.com/user-attachments/assets/1a0fcc29-de16-4efc-bc96-f3d51e94352a" alt="DP_Five_Lora_Random" style="float: left; margin-right: 10px;"/>

Loads LoRA models with randomized strength values within specified ranges. Features individual min/max controls for each LoRA's strength.

### DP_Float_0_1 | DP_2Floats_0_1 | DP_3Floats_0_1
<img src="https://github.com/user-attachments/assets/64a249c6-4c48-4dcf-a4ba-ddcb6e70736c" alt="DP_Float_0_1" style="float: left; margin-right: 10px;"/>

Simple float input/output controls with customizable ranges, defaults, and slider appearance. Available in single, double, and triple float variants.

### DP_Image_Empty_Latent_Switch
<img src="https://github.com/user-attachments/assets/04c21510-a1d2-41d6-901c-ad70dd4f8ec6" alt="DP_Image_Empty_Latent_Switch" style="float: left; margin-right: 10px;"/>

Switches between empty latent (for txt2img) and up to 5 input images (for img2img). Automatically adjusts strength and denoise settings based on mode.

### DP_Image_Loader_Small
<img src="https://github.com/user-attachments/assets/14545cb5-6868-4446-b6ec-711bed60c956" alt="DP_Image_Loader_Small" style="float: left; margin-right: 10px;"/>

Basic image loader with essential effects including grayscale, enhance, flip, and posterize.

### DP_Image_Loader_Medium
<img src="https://github.com/user-attachments/assets/5ab0c438-8841-4e1f-b7e2-23ac449d7475" alt="DP_Image_Loader_Medium" style="float: left; margin-right: 10px;"/>

Image loader with expanded effect options including artistic effects like sepia, emboss, and lineart.

### DP_Image_Loader_Big
<img src="https://github.com/user-attachments/assets/c76ec189-1634-4972-bdc4-81f32167abe9" alt="DP_Image_Loader_Big" style="float: left; margin-right: 10px;"/>

Comprehensive image loader with full effect suite including technical and enhancement options.

### DP_Prompt_Styler
<img src="https://github.com/user-attachments/assets/5a2eec5a-000d-4837-aaf5-f098273d1e2d" alt="DP_Prompt_Styler" style="float: left; margin-right: 10px;"/>

Applies multiple style modifiers to prompts with customizable categories including depth, camera angles, color themes, moods, and effects.

### DP_Quick_Link
<img src="https://github.com/user-attachments/assets/b58b9557-e3be-4639-9958-ea0a901210e8" alt="DP_Quick_Link" style="float: left; margin-right: 10px;"/>

Manages symbolic links for model organization. Creates shortcuts to external model folders without copying files, saving disk space.

### DP_Random_Char
<img src="https://github.com/user-attachments/assets/414bfb42-9cef-4aed-afa4-7938449ae6e8" alt="DP_Random_Char" style="float: left; margin-right: 10px;"/>

Generates random characters with intelligent selection to avoid similar-looking characters and recent repetitions. Perfect for creating readable random strings and passwords.

### DP_Random_MinMax
<img src="https://github.com/user-attachments/assets/99bb875f-3d9b-462c-b781-0c179077af6c" alt="DP_Random_MinMax" style="float: left; margin-right: 10px;"/>

Generates random numbers within specified ranges with configurable step sizes. Provides both float and integer outputs.

### DP_Aspect_Ratio
<img src="https://github.com/user-attachments/assets/514f81d2-3b50-442c-b9e1-d95f93647747" alt="DP_Aspect_Ratio" style="float: left; margin-right: 10px;"/>

Quick aspect ratio selection for common image sizes. Supports custom ratios through configuration file and provides standard presets.
