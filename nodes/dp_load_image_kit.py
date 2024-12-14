import os
import re
import torch
import numpy as np
import cv2
from PIL import Image, ImageOps, ImageSequence
import folder_paths
import hashlib
from pathlib import Path
from .image_effects import ImageEffects

class DP_Image_Loader_Medium:
    def __init__(self):
        self.effects = ImageEffects()
    
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = []
        for filename in os.listdir(input_dir):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                files.append(filename)

        available_styles = [
            "original", "grayscale", "enhance", "flip_h",
            "flip_v", "posterize", "sharpen", "contrast",
            "equalize", "sepia", "blur", "emboss", "palette",
            "solarize", "denoise", "vignette", "glow_edges",
            "edge_detect", "edge_gradient", "lineart_clean",
            "lineart_anime", "threshold", "pencil_sketch",
            "sketch_lines", "bold_lines", "depth_edges",
            "relief_light", "edge_enhance", "edge_morph",
            "relief_shadow"
        ]
        
        return {"required": {
            "image": (sorted(files), {"image_upload": True}),
            "output_01_fx": (available_styles, {"default": "original"}),
            "output_02_fx": (available_styles, {"default": "grayscale"}),
            "output_03_fx": (available_styles, {"default": "flip_h"}),
            "output_04_fx": (available_styles, {"default": "flip_v"})
        },
        "optional": {
            "pipe_input": ("IMAGE",)
        }}

    RETURN_TYPES = ("STRING", "IMAGE", "IMAGE", "IMAGE", "IMAGE", "STRING")
    RETURN_NAMES = ("filename", "output1", "output2", "output3", "output4", "prompt")
    FUNCTION = "load_image_and_process"
    CATEGORY = "DP/Image"

    def extract_prompt_from_metadata(self, image_source):
        try:
            if isinstance(image_source, torch.Tensor):
                img_np = (image_source.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
                img_pil = Image.fromarray(img_np)
            elif isinstance(image_source, str):
                img_pil = Image.open(image_source)
            else:
                img_pil = image_source
                
            # First try to get our custom dp_prompt
            dp_prompt = img_pil.text.get('dp_prompt', '')
            if dp_prompt:
                return dp_prompt
            
            # Fall back to original prompt handling
            prompt = img_pil.text.get('prompt', '')
            if prompt:
                try:
                    import json
                    prompt_data = json.loads(prompt)
                    for node in prompt_data.values():
                        if isinstance(node, dict) and 'inputs' in node:
                            if 'text' in node['inputs']:
                                return node['inputs']['text']
                            elif 'prompt' in node['inputs']:
                                return node['inputs']['prompt']
                    return "Prompt found but no text content extracted"
                except json.JSONDecodeError:
                    return prompt
            return "No prompt found in metadata"
        except Exception as e:
            return f"Error reading metadata: {str(e)}"

    def load_image_and_process(self, image, output_01_fx, output_02_fx, output_03_fx, output_04_fx, pipe_input=None):
        # Initialize prompt_text
        prompt_text = ""
        formatted_name = ""

        if pipe_input is not None:
            output_image = pipe_input
        else:
            image_path = folder_paths.get_annotated_filepath(image)
            formatted_name = os.path.splitext(os.path.basename(image_path))[0]
            
            # Try to load associated caption/prompt file
            caption_path = os.path.splitext(image_path)[0] + ".txt"
            if os.path.exists(caption_path):
                try:
                    with open(caption_path, 'r', encoding='utf-8') as f:
                        prompt_text = f.read().strip()
                except Exception as e:
                    print(f"Warning: Could not read caption file: {e}")
            
            try:
                with Image.open(image_path) as img:
                    img = ImageOps.exif_transpose(img)
                    if img.mode == 'I':
                        img = img.point(lambda i: i * (1 / 255))
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    image = np.array(img).astype(np.float32) / 255.0
                    output_image = torch.from_numpy(image).unsqueeze(0)
                    
                    # Try to get prompt from image metadata
                    if not prompt_text and hasattr(img, 'info'):
                        prompt_text = img.info.get('dp_prompt', '')
                    
            except Exception as e:
                print(f"Error processing image: {e}")
                raise e

        style_map = {
            "original": output_image,
            "grayscale": self.effects.grayscale(output_image),
            "enhance": self.effects.enhance(output_image),
            "flip_h": self.effects.flip_h(output_image),
            "flip_v": self.effects.flip_v(output_image),
            "posterize": self.effects.posterize(output_image, 4),
            "sharpen": self.effects.sharpen(output_image, 1.0),
            "contrast": self.effects.contrast(output_image),
            "equalize": self.effects.equalize(output_image),
            "sepia": self.effects.sepia(output_image, 1.0),
            "blur": self.effects.blur(output_image, 5.0),
            "emboss": self.effects.emboss(output_image, 1.0),
            "palette": self.effects.palette(output_image, 8),
            "solarize": self.effects.solarize(output_image, 0.5),
            "denoise": self.effects.denoise(output_image, 3),
            "vignette": self.effects.vignette(output_image, 0.75),
            "glow_edges": self.effects.glow_edges(output_image, 0.75),
            "edge_detect": self.effects.edge_detect(output_image),
            "edge_gradient": self.effects.edge_gradient(output_image),
            "lineart_clean": self.effects.lineart_clean(output_image),
            "lineart_anime": self.effects.lineart_anime(output_image),
            "threshold": self.effects.threshold(output_image),
            "pencil_sketch": self.effects.pencil_sketch(output_image),
            "sketch_lines": self.effects.sketch_lines(output_image),
            "bold_lines": self.effects.bold_lines(output_image),
            "depth_edges": self.effects.depth_edges(output_image),
            "relief_light": self.effects.relief_light(output_image),
            "edge_enhance": self.effects.edge_enhance(output_image),
            "edge_morph": self.effects.edge_morph(output_image),
            "relief_shadow": self.effects.relief_shadow(output_image)
        }

        return (formatted_name,
                style_map[output_01_fx],
                style_map[output_02_fx],
                style_map[output_03_fx],
                style_map[output_04_fx],
                prompt_text)

    @classmethod
    def IS_CHANGED(s, image, output_01_fx, output_02_fx, output_03_fx, output_04_fx, pipe_input=None):
        if pipe_input is not None:
            return True
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image, output_01_fx, output_02_fx, output_03_fx, output_04_fx, pipe_input=None):
        if pipe_input is not None:
            return True
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True


class DP_Image_Loader_Big:
    def __init__(self):
        self.effects = ImageEffects()
    
    def extract_prompt_from_metadata(self, image_source):
        try:
            if isinstance(image_source, torch.Tensor):
                img_np = (image_source.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
                img_pil = Image.fromarray(img_np)
            elif isinstance(image_source, str):
                img_pil = Image.open(image_source)
            else:
                img_pil = image_source
                
            # First try to get our custom dp_prompt
            dp_prompt = img_pil.text.get('dp_prompt', '')
            if dp_prompt:
                return dp_prompt
            
            # Fall back to original prompt handling
            prompt = img_pil.text.get('prompt', '')
            if prompt:
                try:
                    import json
                    prompt_data = json.loads(prompt)
                    for node in prompt_data.values():
                        if isinstance(node, dict) and 'inputs' in node:
                            if 'text' in node['inputs']:
                                return node['inputs']['text']
                            elif 'prompt' in node['inputs']:
                                return node['inputs']['prompt']
                    return "Prompt found but no text content extracted"
                except json.JSONDecodeError:
                    return prompt
            return "No prompt found in metadata"
        except Exception as e:
            return f"Error reading metadata: {str(e)}"

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = []
        for root, dirs, filenames in os.walk(input_dir):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, input_dir)
                relative_path = relative_path.replace("\\", "/")
                files.append(relative_path)

        available_styles = [
            "original", "grayscale", "enhance", "flip_h",
            "flip_v", "posterize", "sharpen", "contrast",
            "equalize", "sepia", "blur", "emboss", "palette",
            "solarize", "denoise", "vignette", "glow_edges",
            "edge_detect", "edge_gradient", "lineart_clean",
            "lineart_anime", "threshold", "pencil_sketch",
            "sketch_lines", "bold_lines", "depth_edges",
            "relief_light", "edge_enhance", "edge_morph",
            "relief_shadow"
        ]
        
        return {"required": {
            "image": (sorted(files), {"image_upload": True}),
            "output_01_fx": (available_styles, {"default": "original"}),
            "output_02_fx": (available_styles, {"default": "grayscale"}),
            "output_03_fx": (available_styles, {"default": "flip_h"}),
            "output_04_fx": (available_styles, {"default": "flip_v"}),
            "auto_fix_intensity": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.1}),
            "sharpen_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.1}),
            "posterize_levels": ("INT", {"default": 4, "min": 2, "max": 8, "step": 1}),
            "blur_strength": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 20.0, "step": 0.5}),
            "emboss_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 5.0, "step": 0.1}),
            "palette_colors": ("INT", {"default": 8, "min": 2, "max": 256, "step": 1}),
            "solarize_threshold": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.1}),
            "denoise_strength": ("INT", {"default": 3, "min": 1, "max": 10, "step": 1}),
            "vignette_strength": ("FLOAT", {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.1}),
            "glow_strength": ("FLOAT", {"default": 0.75, "min": 0.0, "max": 1.0, "step": 0.1})
        },
        "optional": {
            "pipe_input": ("IMAGE",)
        }}

    RETURN_TYPES = ("STRING", "IMAGE", "IMAGE", "IMAGE", "IMAGE", "STRING")
    RETURN_NAMES = ("filename", "output1", "output2", "output3", "output4", "prompt")
    FUNCTION = "load_image_and_process"
    CATEGORY = "DP/Image"

    def load_image_and_process(self, image, output_01_fx, output_02_fx, output_03_fx, output_04_fx,
                             auto_fix_intensity, sharpen_strength, posterize_levels, blur_strength,
                             emboss_strength, palette_colors, solarize_threshold, denoise_strength,
                             vignette_strength, glow_strength, pipe_input=None):
        
        if pipe_input is not None:
            output_image = pipe_input
            formatted_name = "piped_image"
            prompt_text = self.extract_prompt_from_metadata(pipe_input)
            if prompt_text == "No prompt found in metadata" or prompt_text.startswith("Error reading metadata"):
                prompt_text = "Metadata lost in pipeline - try connecting directly to image loader"
        else:
            image_path = folder_paths.get_annotated_filepath(image)
            formatted_name = os.path.basename(image_path)
            # Always strip extension now
            formatted_name = os.path.splitext(formatted_name)[0]
            
            try:
                with Image.open(image_path) as img:
                    img = ImageOps.exif_transpose(img)
                    if img.mode == 'I':
                        img = img.point(lambda i: i * (1 / 255))
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    image = np.array(img).astype(np.float32) / 255.0
                    output_image = torch.from_numpy(image).unsqueeze(0)
            except Exception as e:
                print(f"Error processing image: {e}")
                raise e

        style_map = {
            "original": output_image,
            "grayscale": self.effects.grayscale(output_image),
            "enhance": self.effects.enhance(output_image, auto_fix_intensity),
            "flip_h": self.effects.flip_h(output_image),
            "flip_v": self.effects.flip_v(output_image),
            "posterize": self.effects.posterize(output_image, posterize_levels),
            "sharpen": self.effects.sharpen(output_image, sharpen_strength),
            "contrast": self.effects.contrast(output_image),
            "equalize": self.effects.equalize(output_image),
            "sepia": self.effects.sepia(output_image, 1.0),
            "blur": self.effects.blur(output_image, blur_strength),
            "emboss": self.effects.emboss(output_image, emboss_strength),
            "palette": self.effects.palette(output_image, palette_colors),
            "solarize": self.effects.solarize(output_image, solarize_threshold),
            "denoise": self.effects.denoise(output_image, denoise_strength),
            "vignette": self.effects.vignette(output_image, vignette_strength),
            "glow_edges": self.effects.glow_edges(output_image, glow_strength),
            "edge_detect": self.effects.edge_detect(output_image),
            "edge_gradient": self.effects.edge_gradient(output_image),
            "lineart_clean": self.effects.lineart_clean(output_image),
            "lineart_anime": self.effects.lineart_anime(output_image),
            "threshold": self.effects.threshold(output_image),
            "pencil_sketch": self.effects.pencil_sketch(output_image),
            "sketch_lines": self.effects.sketch_lines(output_image),
            "bold_lines": self.effects.bold_lines(output_image),
            "depth_edges": self.effects.depth_edges(output_image),
            "relief_light": self.effects.relief_light(output_image),
            "edge_enhance": self.effects.edge_enhance(output_image),
            "edge_morph": self.effects.edge_morph(output_image),
            "relief_shadow": self.effects.relief_shadow(output_image)
        }

        return (formatted_name,
                style_map[output_01_fx],
                style_map[output_02_fx],
                style_map[output_03_fx],
                style_map[output_04_fx],
                prompt_text)

    @classmethod
    def VALIDATE_INPUTS(s, image, output_01_fx, output_02_fx, output_03_fx, output_04_fx, pipe_input=None):
        if pipe_input is not None:
            return True
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True


class DP_Image_Loader_Small(DP_Image_Loader_Medium):
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = []
        for root, dirs, filenames in os.walk(input_dir):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, input_dir)
                relative_path = relative_path.replace("\\", "/")
                files.append(relative_path)

        available_styles = [
            "original", "grayscale", "enhance", "flip_h",
            "flip_v", "posterize", "sharpen", "contrast",
            "equalize", "sepia", "blur", "emboss", "palette",
            "solarize", "denoise", "vignette", "glow_edges",
            "edge_detect", "edge_gradient", "lineart_clean", 
            "lineart_anime", "threshold", "pencil_sketch", "sketch_lines",
            "bold_lines", "depth_edges", "relief_light", "edge_enhance",
            "edge_morph", "relief_shadow"
        ]
        
        return {"required": {
            "image": (sorted(files), {"image_upload": True}),
            "output_01_fx": (available_styles, {"default": "original"}),
            "output_02_fx": (available_styles, {"default": "grayscale"})
        },
        "optional": {
            "pipe_input": ("IMAGE",)
        }}

    RETURN_TYPES = ("IMAGE", "IMAGE")
    RETURN_NAMES = ("output1", "output2")
    FUNCTION = "load_image_and_process"
    CATEGORY = "DP/Image"

    @classmethod
    def IS_CHANGED(s, image, output_01_fx, output_02_fx, pipe_input=None):
        if pipe_input is not None:
            return pipe_input
        image_path = folder_paths.get_annotated_filepath(image)
        return image_path

    @classmethod
    def VALIDATE_INPUTS(s, image, output_01_fx, output_02_fx, pipe_input=None):
        if pipe_input is not None:
            return True
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True

    def load_image_and_process(self, image, output_01_fx, output_02_fx, pipe_input=None):
        if pipe_input is not None:
            output_image = pipe_input
        else:
            image_path = folder_paths.get_annotated_filepath(image)
            try:
                with Image.open(image_path) as img:
                    img = ImageOps.exif_transpose(img)
                    if img.mode == 'I':
                        img = img.point(lambda i: i * (1 / 255))
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    image = np.array(img).astype(np.float32) / 255.0
                    output_image = torch.from_numpy(image).unsqueeze(0)
            except Exception as e:
                print(f"Error processing image: {e}")
                raise e

        style_map = {
            "original": output_image,
            "grayscale": self.effects.grayscale(output_image),
            "enhance": self.effects.enhance(output_image),
            "flip_h": self.effects.flip_h(output_image),
            "flip_v": self.effects.flip_v(output_image),
            "posterize": self.effects.posterize(output_image, 4),
            "sharpen": self.effects.sharpen(output_image, 1.0),
            "contrast": self.effects.contrast(output_image),
            "equalize": self.effects.equalize(output_image),
            "sepia": self.effects.sepia(output_image, 1.0),
            "blur": self.effects.blur(output_image, 5.0),
            "emboss": self.effects.emboss(output_image, 1.0),
            "palette": self.effects.palette(output_image, 8),
            "solarize": self.effects.solarize(output_image, 0.5),
            "denoise": self.effects.denoise(output_image, 3),
            "vignette": self.effects.vignette(output_image, 0.75),
            "glow_edges": self.effects.glow_edges(output_image, 0.75),
            "edge_detect": self.effects.edge_detect(output_image),
            "edge_gradient": self.effects.edge_gradient(output_image),
            "lineart_clean": self.effects.lineart_clean(output_image),
            "lineart_anime": self.effects.lineart_anime(output_image),
            "threshold": self.effects.threshold(output_image),
            "pencil_sketch": self.effects.pencil_sketch(output_image),
            "sketch_lines": self.effects.sketch_lines(output_image),
            "bold_lines": self.effects.bold_lines(output_image),
            "depth_edges": self.effects.depth_edges(output_image),
            "relief_light": self.effects.relief_light(output_image),
            "edge_enhance": self.effects.edge_enhance(output_image),
            "edge_morph": self.effects.edge_morph(output_image),
            "relief_shadow": self.effects.relief_shadow(output_image)
        }

        return (style_map[output_01_fx],
                style_map[output_02_fx])


NODE_CLASS_MAPPINGS = {
    "DP_Image_Loader_Medium": DP_Image_Loader_Medium,
    "DP_Image_Loader_Big": DP_Image_Loader_Big,
    "DP_Image_Loader_Small": DP_Image_Loader_Small
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_Image_Loader_Medium": "DP Image Loader (Medium)",
    "DP_Image_Loader_Big": "DP Image Loader (Big)",
    "DP_Image_Loader_Small": "DP Image Loader (Small)"
} 