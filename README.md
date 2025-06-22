# 🌵 ComfyUI Desert Pixel Nodes - Complete Documentation

A comprehensive collection of 105+ custom nodes for ComfyUI, designed to enhance your image generation and processing workflows with advanced features, utilities, and specialized tools.

## 📚 Table of Contents

- [Installation & Setup](#-installation--setup)
- [🎨 Theming System](#-theming-system)
- [📝 Node Categories](#-node-categories)
  - [🖼️ Image Processing & Analysis](#️-image-processing--analysis)
  - [🎬 Animation & Video](#-animation--video)
  - [📝 Text & Prompt Management](#-text--prompt-management)
  - [🔄 Switches & Controllers](#-switches--controllers)
  - [🎯 Loaders & Models](#-loaders--models)
  - [🔧 Utilities & Tools](#-utilities--tools)
  - [🎲 Random Generators](#-random-generators)
  - [🎪 Creative Effects](#-creative-effects)

---

## 🚀 Installation & Setup

1. Clone or download this repository to your ComfyUI custom_nodes folder
2. Install required dependencies (if any)
3. Restart ComfyUI
4. Find nodes under the "DP" category in your node browser

---

## 🎨 Theming System

### Overview
The Desert Pixel node pack includes a comprehensive theming system that allows you to customize the appearance of ALL ComfyUI nodes (not just DP nodes). Each node gets a unique icon and custom colors for better workflow organization.

### Features
- **Universal Node Theming**: Apply custom colors to any ComfyUI node
- **Preset Themes**: 22+ built-in color themes including Ocean, Purple, Forest, etc.
- **Custom Colors**: Individual title and body color selection
- **Favorite Themes**: Save and apply your preferred color combinations
- **Automatic Icons**: DP nodes get random emoji icons for visual identification
- **Theme Persistence**: Colors are saved with your workflow

### How to Use Themes
1. **Right-click any node** in ComfyUI
2. Navigate to **"DP Color Themes"** in the context menu
3. Choose from:
   - **Preset Themes**: Pre-configured color combinations
   - **Title Color**: Change just the node title color
   - **Body Color**: Change just the node body color
   - **Save As Favorite**: Save current colors as your favorite
   - **Apply Favorite Theme**: Apply your saved favorite
   - **Reset to Default**: Return to default colors

### Available Preset Themes
- **DP Ocean** (Default): Dark gray title with ocean blue body
- **Black**: Charcoal and dark gray combination
- **Purple**: Deep purple variations
- **Royal Blue**: Bright blue styling
- **Forest**: Nature-inspired greens
- **Golden**: Warm gold tones
- **Burgundy**: Rich wine colors
- **Emerald**: Vibrant green shades
- **Midnight**: Deep navy blues
- **And many more...**

---

## 📝 Node Categories

### 🖼️ Image Processing & Analysis

#### **DP_Image_Color_Analyzer**
Advanced image color analysis tool that extracts dominant colors, generates color palettes, and provides detailed color information including theme detection and SD-friendly color descriptions.

#### **DP_Image_Color_Analyzer_Small**
Simplified version of the color analyzer with streamlined interface for basic color extraction and analysis tasks.
![image](https://github.com/user-attachments/assets/725f01e6-af77-4180-aaca-aec363790f6e)


#### **DP_Image_Color_Effect**
Apply various color effects and transformations to images with customizable parameters for artistic and stylistic modifications.

#### **DP_Image_Effect_Processor**
Comprehensive image effects processor with multiple effect types, blend modes, and intensity controls for advanced image manipulation.

#### **DP_Image_Effect_Processor_Small**
Lightweight version of the image effect processor with essential effects and simplified controls.

#### **DP_Load_Image_V2**
Enhanced image loader with built-in resizing, alpha channel preservation, metadata extraction, and format conversion capabilities.

#### **DP_Load_Image_Effects**
Load images with simultaneous effect application, combining loading and processing in a single efficient node.

#### **DP_Load_Image_Effects_Small**
Streamlined image loader with basic effect applications and optimized performance.

#### **DP_Load_Image_Minimal**
Minimal image loader focused on speed and simplicity with essential loading features only.

#### **DP_Load_Image_With_Seed**
Load images with seed-based random selection and processing, useful for controlled randomization in workflows.

#### **DP_Load_Image_Folder**
Batch load multiple images from a folder with filtering, sorting, and batch processing capabilities.

#### **DP_Save_Image_V2**
Advanced image saving with metadata preservation, custom formatting, and batch processing support.

#### **DP_Save_Preview_Image**
Save images with preview generation and metadata embedding for workflow documentation.

#### **DP_Get_Seed_From_Image**
Extract seed information from image metadata for workflow reproducibility and debugging.

#### **DP_Image_Grid_To_Image**
Convert image grids back to individual images with automatic detection and separation.

#### **DP_Image_Slice_To_Grid**
Slice images into grids with customizable dimensions and spacing for tiling effects.

#### **DP_Image_Slide_Show**
Create animated slideshows from multiple images with transition effects and timing controls.

#### **DP_Image_Strip**
Create horizontal or vertical image strips from multiple inputs with alignment options.

#### **DP_Strip_Edge_Masks**
Generate edge masks for image strips to create seamless blending and transition effects.

#### **DP_Image_To_Pixelgrid**
Convert images to pixel grid format with customizable pixel sizes and grid arrangements.

#### **DP_Stitch_2_Images**
Intelligently stitch two images together with blending and alignment options.

#### **DP_Add_Background_To_Png**
Add solid or gradient backgrounds to PNG images with transparency handling.

#### **DP_Resize_Image_And_Mask**
Resize images and their corresponding masks simultaneously while maintaining proper alignment.

#### **DP_Place_Image**
Precisely place images on canvases with position, scale, and blend mode controls.

#### **DP_Extract_Mask**
Extract masks from images using various methods including alpha channels and color thresholds.

### 🎬 Animation & Video

#### **DP_Gif_Maker**
Professional GIF creation tool with frame control, transition effects, quality settings, and optimization options.

#### **DP_Video_Flicker**
Add realistic flicker effects to video sequences with customizable intensity and patterns.

#### **DP_Video_Looper**
Create seamless video loops with crossfade transitions and perfect loop point detection.

#### **DP_Video_Transition**
Apply smooth transitions between video clips with various blend modes and timing controls.

#### **DP_Video_Effect_Sender** / **DP_Video_Effect_Receiver**
Network-based video effect transmission system for distributed processing workflows.

#### **DP_FastSlowMotion**
Apply variable speed effects to video sequences with smooth interpolation and timing controls.

#### **DP_Logo_Animator**
Animate logos and text with built-in effects, transitions, and customizable motion paths.

#### **DP_Animation_Calculator_5_Inputs** / **DP_Animation_Calculator_10_Inputs**
Advanced animation calculators for complex motion interpolation with multiple input parameters.

#### **DP_Big_Letters**
Generate large animated text with font selection, effects, and batch processing capabilities.

### 📝 Text & Prompt Management

#### **DP_Words**
Advanced text rendering with font selection, formatting, and layout controls for creating text images.

#### **DP_Text_Preview**
Preview and format text with various styling options before using in other nodes.

#### **DP_Prompt_Styler**
Apply consistent styling to prompts with categorized style options including depth, camera angles, lighting, and mood.

#### **DP_Prompt_Manager_Small**
Streamlined prompt management with organization, tagging, and quick access features.

#### **DP_Prompt_Mode_Controller**
Control prompt generation modes with conditional logic and parameter switching.

#### **DP_SmartPromptCompressor**
Intelligently compress prompts while maintaining meaning and important keywords for token optimization.

#### **DP_Prompt_Inverter**
Reverse engineer prompts from images or generate negative prompts from positive ones.

#### **DP_Prompt_Travel_Prompt**
Create smooth prompt transitions for prompt travel animations and morphing effects.

#### **DP_clean_prompt**
Clean and optimize prompts by removing redundant words, fixing formatting, and standardizing syntax.

#### **DP_Clean_Prompt_Travel**
Specialized prompt cleaning for prompt travel workflows with transition-aware optimization.

#### **DP_Broken_Token**
Handle and repair broken tokens in prompts with automatic detection and correction.

#### **DP_5_Find_And_Replace**
Perform multiple find and replace operations on text with regex support and batch processing.

### 🔄 Switches & Controllers

#### **DP_Image_And_String_Pairs_Switch**
Switch between paired image and text combinations with cycle modes and index control.

#### **DP_10_Images_Switch_Or_Batch** / **DP_3_Images_Switch_Or_Batch** / **DP_5_Images_Switch_Or_Batch**
Flexible image switching with batch mode support for multiple input handling.

#### **DP_5_Image_And_Mask_Switch**
Switch between image and mask pairs with synchronized control and batch processing.

#### **DP_10_String_Switch_Or_Connect** / **DP_3_String_Switch_Or_Connect** / **DP_5_String_Switch_Or_Connect**
String switching nodes with connection and concatenation modes for text management.

#### **DP_2_String_Switch**
Simple two-way string switch with toggle functionality.

#### **DP_String_Text** / **DP_String_Text_With_Sdxl_Weight**
Text input nodes with optional SDXL weight formatting for prompt enhancement.

#### **DP_Switch_Controller**
Universal switch controller for managing multiple switch states across complex workflows.

#### **DP_Condition_Switch**
Conditional switching based on boolean logic and comparison operations.

#### **DP_Random_Mode_Switch** / **DP_Random_Mode_Controller**
Random-based switching with controllable probability and mode selection.

### 🎯 Loaders & Models

#### **DP_Five_Lora** / **DP_Five_Lora_Random**
Load up to five LoRA models simultaneously with strength control and random selection options.

#### **DP_Lora_Strength_Controller** / **DP_Lora_Random_Strength_Controller**
Precise control over LoRA strength parameters with random and fixed value options.

#### **DP_Load_Checkpoint_With_Info**
Load checkpoints with detailed information display and metadata extraction.

#### **DP_Load_UNET_With_Info** / **DP_Load_Dual_CLIP_With_Info**
Load UNET and CLIP models with comprehensive information and version details.

#### **DP_ControlNetApplyAdvanced** / **DP_Load_Controlnet_Model_With_Name**
Advanced ControlNet loading and application with detailed parameter control.

#### **DP_Quick_Model_Link**
Create symbolic links for quick model access and organization.

### 🔧 Utilities & Tools

#### **DP_Aspect_Ratio_Picker**
Select from predefined aspect ratios with custom ratio support for consistent sizing.

#### **DP_Custom_Aspect_Ratio**
Define custom aspect ratios with calculation and preview features.

#### **DP_Draggable_Floats_1** / **DP_Draggable_Floats_2** / **DP_Draggable_Floats_3**
Interactive float value controls with draggable interfaces and precision settings.

#### **DP_Float_Stepper**
Step through float values with increment/decrement controls and range limiting.

#### **DP_Transition_Frames_Selector** / **DP_Diff_Int_8step_selector**
Specialized selectors for animation frame counts and stepped integer values.

#### **DP_Draggable_Int_1step** / **DP_Draggable_Int_4step** / **DP_Draggable_Int_8step**
Integer value controls with different step sizes and draggable interfaces.

#### **DP_Int_0_1000**
Simple integer selector with 0-1000 range for common parameter needs.

#### **DP_Mask_Settings**
Configure mask parameters with feathering, inversion, and adjustment options.

#### **DP_Latent_Split**
Split latent tensors for parallel processing and advanced workflow architectures.

#### **DP_Line_Cycler**
Cycle through lines of text with various modes and timing controls.

#### **DP_create_json_file**
Generate JSON files from workflow data for configuration and batch processing.

#### **DP_Sampler_With_Info** / **DP_Advanced_Sampler**
Enhanced samplers with detailed information display and advanced parameter control.

### 🎲 Random Generators

#### **DP_Random_Crazy_Prompt_Generator**
Generate wild and creative prompts with adjustable randomness and style combinations.

#### **DP_Random_Superhero_Prompt_Generator**
Create superhero-themed prompts with powers, costumes, and background generation.

#### **DP_Random_Vehicle_Generator**
Generate vehicle descriptions with types, modifications, and environmental settings.

#### **DP_Random_Psychedelic_Punk_Generator**
Create psychedelic and punk-themed prompts with style and color combinations.

#### **DP_Random_Logo_Style_Generator**
Generate logo style descriptions with typography, effects, and design elements.

#### **DP_Art_Style_Generator**
Create art style descriptions combining movements, techniques, and artistic elements.

#### **DP_Random_Character**
Generate character descriptions with appearance, clothing, and personality traits.

#### **DP_random_min_max**
Generate random numbers within specified ranges with various distribution options.

#### **DP_Versatile_Prompt_Subjects_Generator**
Create diverse subject prompts across multiple categories and themes.

#### **DP_Crazy_Prompt_Mixer**
Mix and combine existing prompts in creative ways with randomization options.

### 🎪 Creative Effects

#### **DP_Add_Weight_To_String_Sdxl** / **DP_Advanced_Weight_String_Sdxl**
Add SDXL-compatible weight formatting to text strings with advanced syntax support.

#### **DP_IF_INT_CONDITION**
Conditional integer operations with comparison logic and branching support.

#### **DP_Image_Empty_Latent_Switch_Flux** / **DP_Image_Empty_Latent_Switch_SDXL**
Switch between images and empty latents for conditional generation workflows.

---

## 🔧 Technical Requirements

- ComfyUI (latest version recommended)
- Python 3.8+
- PyTorch with CUDA support (for GPU acceleration)
- Additional dependencies as specified in requirements.txt

## 🤝 Support & Contribution

This node pack is actively maintained and updated. For issues, feature requests, or contributions, please visit the project repository.

## 📄 License

Licensed under the appropriate open-source license. See LICENSE file for details.

---

*🌵 Desert Pixel Nodes - Enhancing your ComfyUI experience with powerful, creative, and efficient tools.*
