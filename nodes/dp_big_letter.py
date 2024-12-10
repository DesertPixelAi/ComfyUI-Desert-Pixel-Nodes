import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def find_font_files():
    # Common font directories with recursive search
    font_dirs = [
        os.path.join(os.environ.get('SystemRoot', ''), 'Fonts'),  # Windows
        '/System/Library/Fonts',  # MacOS
        '/usr/share/fonts',  # Linux
        os.path.expanduser('~/.local/share/fonts'),  # Linux user fonts
        '/Library/Fonts',  # Additional MacOS
        '.'  # Current directory
    ]
    
    font_files = {}
    font_weights = set()
    
    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            for root, _, files in os.walk(font_dir):
                for file in files:
                    if file.lower().endswith(('.ttf', '.otf')):
                        try:
                            font_path = os.path.join(root, file)
                            test_font = ImageFont.truetype(font_path, size=12)
                            
                            font_name = test_font.getname()[0]
                            style = test_font.getname()[1].lower()
                            
                            weight = "regular"
                            if any(w in style for w in ['bold', 'black', 'light', 'thin', 'medium', 'heavy']):
                                for w in ['bold', 'black', 'light', 'thin', 'medium', 'heavy']:
                                    if w in style:
                                        weight = w
                                        break
                            
                            if font_name not in font_files:
                                font_files[font_name] = {}
                            font_files[font_name][weight] = font_path
                            font_weights.add(weight)
                            
                        except Exception:
                            continue
    
    return font_files, sorted(list(font_weights))

class DP_Big_Letters:
    FONT_FILES, FONT_WEIGHTS = find_font_files()
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "DESERT PIXEL"}),
                "image_width": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "image_height": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "padding_top": ("INT", {"default": 120, "min": 0, "max": 500}),
                "padding_bottom": ("INT", {"default": 120, "min": 0, "max": 500}),
                "padding_left": ("INT", {"default": 100, "min": 0, "max": 500}),
                "padding_right": ("INT", {"default": 100, "min": 0, "max": 500}),
                "font_name": (sorted(list(cls.FONT_FILES.keys())),),
                "font_weight": (cls.FONT_WEIGHTS,),
                "font_color": (["white", "black", "red", "green", "blue", "yellow"],),
                "background_color": (["black", "white", "red", "green", "blue", "yellow"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "create_letter_images"
    CATEGORY = "🔤 DP Nodes"

    def find_optimal_font_size_for_all_letters(self, letters, font_path, image_width, image_height, 
                                             padding_top, padding_bottom, padding_left, padding_right):
        min_size = 1
        max_size = min(image_width, image_height) * 2
        optimal_size = min_size
        
        available_width = image_width - (padding_left + padding_right)
        available_height = image_height - (padding_top + padding_bottom)
        
        while min_size <= max_size:
            mid_size = (min_size + max_size) // 2
            font = ImageFont.truetype(font_path, size=mid_size)
            
            fits_all = True
            for letter in letters:
                bbox = font.getbbox(letter)
                bbox_width = bbox[2] - bbox[0]
                bbox_height = bbox[3] - bbox[1]
                
                if (bbox_width > available_width or 
                    bbox_height > available_height):
                    fits_all = False
                    break
            
            if fits_all:
                optimal_size = mid_size
                min_size = mid_size + 1
            else:
                max_size = mid_size - 1
        
        return optimal_size

    def create_letter_images(self, text, image_width, image_height, 
                           padding_top, padding_bottom, padding_left, padding_right,
                           font_name, font_weight, font_color, background_color):
        # Remove spaces and get letters
        letters = [char for char in text if not char.isspace()]
        
        if not letters:
            # Return empty batch if no letters
            return (torch.zeros((1, image_height, image_width, 4)),)
        
        # Get font path
        font_path = None
        if font_name in self.FONT_FILES:
            if font_weight in self.FONT_FILES[font_name]:
                font_path = self.FONT_FILES[font_name][font_weight]
            else:
                font_path = next(iter(self.FONT_FILES[font_name].values()))
        
        if not font_path:
            font_path = os.path.join(os.environ.get('SystemRoot', ''), 'Fonts', 'arial.ttf')
        
        # Find optimal font size
        font_size = self.find_optimal_font_size_for_all_letters(
            letters, font_path, image_width, image_height,
            padding_top, padding_bottom, padding_left, padding_right
        )
        
        # Create font
        font = ImageFont.truetype(font_path, size=font_size)
        
        # Create a tensor to store all letter images
        letter_tensors = []
        
        for letter in letters:
            img = Image.new("RGBA", (image_width, image_height), background_color)
            draw = ImageDraw.Draw(img)
            
            # Get letter dimensions
            bbox = font.getbbox(letter)
            bbox_left, bbox_top, bbox_right, bbox_bottom = bbox
            letter_width = bbox_right - bbox_left
            letter_height = bbox_bottom - bbox_top
            
            # Calculate center position with padding
            x = padding_left + (image_width - padding_left - padding_right - letter_width) // 2 - bbox_left
            y = padding_top + (image_height - padding_top - padding_bottom - letter_height) // 2 - bbox_top
            
            # Draw the letter
            draw.text((x, y), letter, font=font, fill=font_color)
            
            # Convert to tensor
            letter_tensors.append(pil2tensor(img))
        
        # Stack all tensors into a single batch
        batch_tensor = torch.cat(letter_tensors, dim=0)
        
        return (batch_tensor,)