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

Full nodes list
1. DP_Animation_Calculator_5Inputs
2. DP_Aspect_Ratio
3. DP_Big_Letters
4. DP_Broken_Token
5. DP_Clean_Prompt
6. DP_Create_JSON
7. DP_Crazy_Prompt
8. DP_Image_Color_Analyzer
9. DP_Fast_Slow_Motion
10. DP_Five_Lora
11. DP_Five_Lora_Random
12. DP_Float_0_1
13. DP_2Floats_0_1
14. DP_3Floats_0_1
15. DP_Image_Empty_Latent_Switch
16. DP_Image_Loader_Big
17. DP_Image_Loader_Medium
18. DP_Image_Loader_Small
19. DP_Image_Slide_Show
20. DP_Logo_Animator
21. DP_Prompt_Styler
22. DP_Quick_Link
23. DP_Random_Char
24. DP_Random_MinMax
25. DP_Smart_Saver
26. DP_Video_Effect_Receiver
27. DP_Video_Effect_Sender
28. DP_Video_Flicker
29. DP_Video_Transition

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
