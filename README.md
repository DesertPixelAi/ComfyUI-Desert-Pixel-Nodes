# ComfyUI Custom Nodes by Desert Pixel

A collection of custom nodes for ComfyUI focused on animation, image processing, and workflow optimization.

## Features

### Animation & Video
- **Animation Calculator (5 Inputs)**: Complex animation timing calculator
- **Fast/Slow Motion**: Control video playback speed
- **Video Effects**: 
  - Sender/Receiver system for effect application
  - Flicker effects
  - Transition effects

### Image Processing
- **Big Letters**: Create text-based images
- **Color Analyzer**: Analyze and generate color palettes
- **Logo Animator**: Create animated logos
- **Smart Image Saver**: Enhanced image saving with metadata
- **Image Effects**: Various image processing effects

### Utility Nodes
- **Random Min/Max**: Generate random numbers with control
- **Random Characters**: Generate random characters/strings
- **Aspect Ratio Picker**: Easy aspect ratio selection
- **Clean Prompt**: Clean and format prompt text
- **Multi Styler**: Apply multiple styles to prompts
- **Zero-One Floats**: Simple float input/output controls

## Installation

Clone this repository into your ComfyUI custom_nodes folder:

```bash
git clone [your-repo-url] custom_nodes/desert-pixel-nodes
```

## Node Documentation


### DP_Animation_Calculator_5Inputs
![DP_Animation_Calculator_5Inputs_detailed](https://github.com/user-attachments/assets/fa45806e-76f5-4d25-a0a5-8b6d494d9f90)
Animation calculator helper for switching between images/styles with img2video & video2video using AnimateDiff. Creates timing data for prompt scheduling, fade masks, and IP Adapter batch processing.

Each image has a keyframe start point and associated prompt text. The node can be used with or without image inputs to generate scheduling prompts or fade mask timing.

### Inputs:
- **Image Inputs (Optional, 5 slots)**
  - When connected, creates an image batch sized to Total_Frames for IP Adapter
  - Includes crossfade transitions controlled by Transition_Frames parameter

- **Total_Frames** (INT)
  - Defines total number of frames to process
  - Default: 96, Range: 16-2000

- **Image_startPoint_XX** (INT, XX: 01-05)
  - Keyframe starting point for each image/style
  - Image_01_startPoint fixed at 0
  - Each keyframe must be larger than previous ones
  - Range: 0-1000

- **Prompt_Image_XX** (STRING, XX: 01-05)
  - Prompt text for each image/keyframe
  - Used in prompt scheduling

- **Transition_Frames** (INT)
  - Controls transition length between images
  - Affects fade mask timing and image batch output
  - Does not affect prompt timing
  - Default: 8, Range: 0-32, Step: 4
  - Creates pre & post transition points:
    - Pre-transition: Transition_Frames/2 frames before keyframe
    - Post-transition: Transition_Frames/2 frames after keyframe
  - Allows control of ControlNet & IP Adapter strength during transitions

- **Fade Mask Controls** (6x FLOAT)
  - fade_mask_XX_Min (XX: 01-03)
    - Minimum weight for fade mask
    - Range: 0.0-1.0, Step: 0.1
  - fade_mask_XX_Max (XX: 01-03)
    - Maximum weight for fade mask
    - Range: 0.0-1.0, Step: 0.1
  - Set Min > Max to invert mask

### Outputs:
- **Image_Batch_Output** (IMAGE)
  - Generated when images are connected
  - Batch sized to Total_Frames
  - Each image spans its keyframe duration
  - Includes crossfade transitions between images

- **Text_Prompt_Timing** (STRING)
  - Formatted timing string for prompt schedule node

- **fade_mask_timing_XX** (3x STRING, XX: 01-03)
  - Formatted timing strings for fade mask advanced node
  - Controls transition strength and mask behavior

### Creating Loops:
For img2video loops:
1. Set last Image_startPoint equal to Total_Frames
2. Use identical first and last Prompt_Image and Image inputs

### Note:
Transition system uses three control points (Pre-transition, Keyframe, Post-transition) for smooth blending of ControlNet and IP Adapter weights during transitions.

### DP_Image_Slide_Show
![DP_Image_Slide_Show](https://github.com/user-attachments/assets/c3001c1e-4d57-46fd-9d0f-4a62109a46dd)

Creates image sequences with blend mode transitions. Perfect for GIFs and videos.

**Inputs:**
- 5 optional image inputs
- Total_Frames (16-2000)
- Image start points (5)
- Transition_Frames (0-32)
- Blend modes

**Output:**
- Image batch with transitions

### DP_Logo_Animator
![DP_Logo_Animator](https://github.com/user-attachments/assets/d56d6536-ea7a-4819-98b6-cc5c4b19f5f3)

Animates logos with scale effects and background handling. Create professional logo animations for video content.

### DP_Video_Effect_Sender & DP_Video_Effect_Receiver
![DP_Video_Effect_Sender_reciver](https://github.com/user-attachments/assets/9b2ef2f5-0888-42c8-8c59-978bd2f43b93)

System for applying effects to specific frames in a video sequence, with separate sender and receiver nodes.

### DP_Video_Flicker
![DP_Video_Flicker](https://github.com/user-attachments/assets/ffe900e0-2cac-445e-8b39-64e77d6f6081)

Creates customizable flicker effects for video sequences with color and timing control.

### DP_Video_Transition
![DP_Video_Transition](https://github.com/user-attachments/assets/67234ca8-2496-405b-a1a7-3211fb225887)

Handles video transitions with multiple blend modes and timing controls.

### DP_Smart_Saver
![DP_Smart_Saver](https://github.com/user-attachments/assets/704ed83f-daa9-46aa-aadc-7e89a3943010)

Enhanced image saving with metadata preservation and naming automation.

### DP_Big_Letters
![DP_Big_Letters](https://github.com/user-attachments/assets/c40205d0-6327-47f3-b9f0-29fb3d048ef8)

Creates text-based images with customizable fonts and styling.

### DP_Broken_Token
![DP_Broken_Token](https://github.com/user-attachments/assets/f9bfacd1-1b87-4225-ab67-12d5804ef2aa)

Analyzes and splits Flux prompts based on token count.

### DP_Clean_Prompt
![DP_Clean_Prompt](https://github.com/user-attachments/assets/678363ab-5a2d-473f-9132-2487152f588b)

Cleans and formats prompt text for consistent results.

### DP_Create_JSON
![DP_Create_JSON](https://github.com/user-attachments/assets/e3c210b5-d718-4b8b-8e9b-c0963497b22b)

Creates JSON files from structured data with customizable formatting.

### DP_Crazy_Prompt
![DPImageColorAnalyzer](https://github.com/user-attachments/assets/b25e622d-151a-4a9f-9275-86398d7ea7f3)

Generates creative prompt combinations from predefined categories.

### DP_Image_Color_Analyzer
![DPImageColorAnalyzer](https://github.com/user-attachments/assets/bf90ffac-3925-40ed-9873-2ea3a7d42d1c)

Analyzes image colors and generates SD-friendly color descriptions.

### DP_Fast_Slow_Motion
![DP_Fast_Slow_Motion](https://github.com/user-attachments/assets/b64a26ea-54ad-421a-a8bf-a573389fbae9)

Controls video playback speed with customizable ranges.

### DP_Five_Lora:
![DP_Five_Lora](https://github.com/user-attachments/assets/7de97607-c5cc-4186-a9c0-250ee55548b4)

Loads up to five LoRA models with strength control.

### DP_Five_Lora_Random
![DP Five LoRA Loader (Random)](https://github.com/user-attachments/assets/1a0fcc29-de16-4efc-bc96-f3d51e94352a)

Loads LoRA models with randomized strength values.

### DP_Float_0_1 | DP_2Floats_0_1 | DP_3Floats_0_1
![DP_Float_0_1](https://github.com/user-attachments/assets/64a249c6-4c48-4dcf-a4ba-ddcb6e70736c)

Simple float input/output nodes with customizable ranges.

### DP_Image_Empty_Latent_Switch
![DP_Image_Empty_Latent_Switch](https://github.com/user-attachments/assets/04c21510-a1d2-41d6-901c-ad70dd4f8ec6)

Switches between empty latent and image inputs for flexible workflows.

### DP_Image_Loader_Small
![DP_Image_Loader_Small](https://github.com/user-attachments/assets/14545cb5-6868-4446-b6ec-711bed60c956)

Basic image loader with essential effects.

### DP_Image_Loader_Medium
![DP_Image_Loader_Medium](https://github.com/user-attachments/assets/5ab0c438-8841-4e1f-b7e2-23ac449d7475)

Image loader with expanded effect options.

### DP_Image_Loader_Big
![DP_Image_Loader_Big](https://github.com/user-attachments/assets/c76ec189-1634-4972-bdc4-81f32167abe9)

Comprehensive image loader with full effect suite.

### DP_Prompt_Styler
![DP_Prompt_Styler](https://github.com/user-attachments/assets/5a2eec5a-000d-4837-aaf5-f098273d1e2d)

Applies multiple style modifiers to prompts.

### DP_Quick_Link
![DP_Quick_Link](https://github.com/user-attachments/assets/b58b9557-e3be-4639-9958-ea0a901210e8)

Manages symbolic links for model organization.

### DP_Random_Char
![DP_Random_Char](https://github.com/user-attachments/assets/414bfb42-9cef-4aed-afa4-7938449ae6e8)

Generates random characters with customizable options.

### DP_Random_MinMax
![DP_Random_MinMax](https://github.com/user-attachments/assets/99bb875f-3d9b-462c-b781-0c179077af6c)

Generates random numbers within specified ranges.

### DP_Aspect_Ratio
![DP_Aspect_Ratio](https://github.com/user-attachments/assets/514f81d2-3b50-442c-b9e1-d95f93647747)

Quick aspect ratio selection for common image sizes.
