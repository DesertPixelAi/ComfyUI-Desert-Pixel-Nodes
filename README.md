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
