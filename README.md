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
- **Image Effects**: Various image processing effects including:
  - Sepia
  - Vignette
  - Edge detection
  - Sketch effects
  - Relief shadows
  - And more...

### Utility Nodes
- **Random Min/Max**: Generate random numbers with control
- **Random Characters**: Generate random characters/strings
- **Aspect Ratio Picker**: Easy aspect ratio selection
- **Clean Prompt**: Clean and format prompt text
- **Broken Token**: Analyze and split Flux prompts
- **Quick Model Link**: Manage symbolic links for models
- **Multi Styler**: Apply multiple styles to prompts
- **Zero-One Floats**: Simple float input/output controls

Full nodes list:

## DP_Animation_Calculator_5Inputs
![DP_Animation_Calculator_5Inputs_detailed](https://github.com/user-attachments/assets/fa45806e-76f5-4d25-a0a5-8b6d494d9f90)

## DP_Image_Slide_Show
![DP_Image_Slide_Show](https://github.com/user-attachments/assets/c3001c1e-4d57-46fd-9d0f-4a62109a46dd)

## DP_Logo_Animator
![DP_Logo_Animator](https://github.com/user-attachments/assets/d56d6536-ea7a-4819-98b6-cc5c4b19f5f3)

## DP_Video_Effect_Sender & DP_Video_Effect_Receiver
![DP_Video_Effect_Sender_reciver](https://github.com/user-attachments/assets/9b2ef2f5-0888-42c8-8c59-978bd2f43b93)

## DP_Video_Flicker
![DP_Video_Flicker](https://github.com/user-attachments/assets/ffe900e0-2cac-445e-8b39-64e77d6f6081)

## DP_Video_Transition
![DP_Video_Transition](https://github.com/user-attachments/assets/67234ca8-2496-405b-a1a7-3211fb225887)

DP_Smart_Saver
![DP_Smart_Saver](https://github.com/user-attachments/assets/704ed83f-daa9-46aa-aadc-7e89a3943010)

DP_Big_Letters
![DP_Big_Letters](https://github.com/user-attachments/assets/c40205d0-6327-47f3-b9f0-29fb3d048ef8)

## DP_Broken_Token
![DP_Broken_Token](https://github.com/user-attachments/assets/f9bfacd1-1b87-4225-ab67-12d5804ef2aa)

## DP_Clean_Prompt
![DP_Clean_Prompt](https://github.com/user-attachments/assets/678363ab-5a2d-473f-9132-2487152f588b)

## DP_Create_JSON
![DP_Create_JSON](https://github.com/user-attachments/assets/e3c210b5-d718-4b8b-8e9b-c0963497b22b)

## DP_Crazy_Prompt
![DPImageColorAnalyzer](https://github.com/user-attachments/assets/b25e622d-151a-4a9f-9275-86398d7ea7f3)

## DP_Image_Color_Analyzer
![DPImageColorAnalyzer](https://github.com/user-attachments/assets/bf90ffac-3925-40ed-9873-2ea3a7d42d1c)

## DP_Fast_Slow_Motion
![DP_Fast_Slow_Motion](https://github.com/user-attachments/assets/b64a26ea-54ad-421a-a8bf-a573389fbae9)

## DP_Five_Lora:
![DP_Five_Lora](https://github.com/user-attachments/assets/7de97607-c5cc-4186-a9c0-250ee55548b4)

## DP_Five_Lora_Random
![DP Five LoRA Loader (Random)](https://github.com/user-attachments/assets/1a0fcc29-de16-4efc-bc96-f3d51e94352a)

## DP_Float_0_1 | DP_2Floats_0_1 | DP_3Floats_0_1
![DP_Float_0_1](https://github.com/user-attachments/assets/64a249c6-4c48-4dcf-a4ba-ddcb6e70736c)

## DP_Image_Empty_Latent_Switch
![DP_Image_Empty_Latent_Switch](https://github.com/user-attachments/assets/04c21510-a1d2-41d6-901c-ad70dd4f8ec6)

DP_Image_Loader_Small
![DP_Image_Loader_Small](https://github.com/user-attachments/assets/14545cb5-6868-4446-b6ec-711bed60c956)

DP_Image_Loader_Medium
![DP_Image_Loader_Medium](https://github.com/user-attachments/assets/5ab0c438-8841-4e1f-b7e2-23ac449d7475)

## DP_Image_Loader_Big
![DP_Image_Loader_Big](https://github.com/user-attachments/assets/c76ec189-1634-4972-bdc4-81f32167abe9)

## DP_Prompt_Styler
![DP_Prompt_Styler](https://github.com/user-attachments/assets/5a2eec5a-000d-4837-aaf5-f098273d1e2d)

## DP_Quick_Link
![DP_Quick_Link](https://github.com/user-attachments/assets/b58b9557-e3be-4639-9958-ea0a901210e8)

## DP_Random_Char
![DP_Random_Char](https://github.com/user-attachments/assets/414bfb42-9cef-4aed-afa4-7938449ae6e8)

## DP_Random_MinMax
![DP_Random_MinMax](https://github.com/user-attachments/assets/99bb875f-3d9b-462c-b781-0c179077af6c)

## DP_Aspect_Ratio
![DP_Aspect_Ratio](https://github.com/user-attachments/assets/514f81d2-3b50-442c-b9e1-d95f93647747)


## Installation

1. Clone this repository into your ComfyUI custom_nodes folder:

```

# Standard library imports
import os

# Third-party imports
import numpy as np
import torch
from PIL import Image

# Local imports
from .image_effects import ImageEffects
