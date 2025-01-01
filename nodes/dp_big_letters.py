import random
import torch
from PIL import Image, ImageDraw, ImageFont
import os
from server import PromptServer
import numpy as np

class DP_Big_Letters:
    def __init__(self):
        self.current_index = -1
        self.id = str(random.randint(0, 2**64))
        self.last_seed = 0
        
    @staticmethod
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

    # Initialize font files and weights
    FONT_FILES, FONT_WEIGHTS = find_font_files()

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["Batch_Mode", "Cycler_Mode"],{"default": "Cycler_Mode"}),
                "text": ("STRING", {"default": "DESERT PIXEL"}),
                "cycle_mode": (["increment", "decrement", "fixed"],),
                "index": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "image_width": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "image_height": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "padding_top": ("INT", {"default": 20, "min": 0, "max": 500}),
                "padding_bottom": ("INT", {"default": 20, "min": 0, "max": 500}),
                "padding_left": ("INT", {"default": 20, "min": 0, "max": 500}),
                "padding_right": ("INT", {"default": 20, "min": 0, "max": 500}),
                "font_name": (sorted(list(cls.FONT_FILES.keys())),),
                "font_weight": (cls.FONT_WEIGHTS,),
                "font_color": (["white", "black", "red", "green", "blue", "yellow"],),
                "background_color": (["black", "white", "red", "green", "blue", "yellow"],),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING",)
    RETURN_NAMES = ("image", "letter_name",)
    FUNCTION = "process_letters"
    CATEGORY = "DP/Animation"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        mode = kwargs.get("mode", "Batch_Mode")
        if mode == "Cycler_Mode":
            return float("NaN")
        return ""

    def find_optimal_font_size_for_all_letters(self, letters, font_path, image_width, image_height,
                                             padding_top, padding_bottom, padding_left, padding_right):
        available_width = image_width - padding_left - padding_right
        available_height = image_height - padding_top - padding_bottom
        
        min_size = 1
        max_size = min(available_width, available_height)
        optimal_size = min_size
        
        while min_size <= max_size:
            mid_size = (min_size + max_size) // 2
            font = ImageFont.truetype(font_path, size=mid_size)
            
            fits_all = True
            for letter in letters:
                bbox = font.getbbox(letter)
                bbox_width = bbox[2] - bbox[0]
                bbox_height = bbox[3] - bbox[1]
                
                if (bbox_width > available_width or bbox_height > available_height):
                    fits_all = False
                    break
            
            if fits_all:
                optimal_size = mid_size
                min_size = mid_size + 1
            else:
                max_size = mid_size - 1
        
        return optimal_size

    def get_character_description(self, char):
        if char.isalpha():
            return f"the letter {char.upper()}"
        elif char.isdigit():
            return f"the digit {char}"
        else:
            # Dictionary for common special characters
            special_chars = {
                '#': 'hash',
                '@': 'at',
                '$': 'dollar',
                '%': 'percent',
                '^': 'caret',
                '&': 'ampersand',
                '*': 'asterisk',
                '(': 'left parenthesis',
                ')': 'right parenthesis',
                '-': 'hyphen',
                '_': 'underscore',
                '+': 'plus',
                '=': 'equals',
                '!': 'exclamation',
                '?': 'question mark'
            }
            return f"the {special_chars.get(char, 'special character')} symbol"

    def process_letters(self, mode, text, cycle_mode, index, image_width, image_height,
                       padding_top, padding_bottom, padding_left, padding_right,
                       font_name, font_weight, font_color, background_color, unique_id):
        if mode == "Batch_Mode":
            # Process batch mode
            batch_result = self.create_letter_images(
                text, image_width, image_height,
                padding_top, padding_bottom, padding_left, padding_right,
                font_name, font_weight, font_color, background_color
            )
            # Update metadata for batch mode
            characters = [char for char in text if not char.isspace()]
            descriptions = [self.get_character_description(char) for char in characters]
            metadata = " | ".join(descriptions)
            return (batch_result[0], metadata)
        else:
            # Store the current state before any processing
            current_color = getattr(self, 'color', "#121317")
            current_bgcolor = getattr(self, 'bgcolor', "#006994")
            
            # Store random state
            random_state = random.getstate()
            
            try:
                characters = [char for char in text if not char.isspace()]
                if not characters:
                    return (torch.zeros((1, image_height, image_width, 4)), "")

                num_chars = len(characters)
                next_index = self.current_index

                print(f"[Python] Index calculation:")
                print(f"  - Current index: {self.current_index}")
                print(f"  - Control mode: {cycle_mode}")
                print(f"  - Number of chars: {num_chars}")
                
                # Calculate next index based on cycle mode
                if cycle_mode == "increment":
                    next_index = (self.current_index + 1) % num_chars
                    print(f"  - Increment: ({self.current_index} + 1) % {num_chars} = {next_index}")
                elif cycle_mode == "decrement":
                    next_index = (self.current_index - 1) % num_chars
                    print(f"  - Decrement: ({self.current_index} - 1) % {num_chars} = {next_index}")
                else:  # fixed
                    next_index = index % num_chars
                    print(f"  - Fixed: {index} % {num_chars} = {next_index}")
                
                self.current_index = next_index
                print(f"  - Final current_index: {self.current_index}")
                
                selected_char = characters[self.current_index]
                char_description = self.get_character_description(selected_char)
                print(f"  - Selected char: {selected_char}")

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
                    characters, font_path, image_width, image_height,
                    padding_top, padding_bottom, padding_left, padding_right
                )

                # Create the image
                img = self.create_letter_image(
                    selected_char, font_path, font_size,
                    image_width, image_height,
                    padding_top, padding_bottom, padding_left, padding_right,
                    font_color, background_color
                )

                # First send WebSocket message (like prompt manager)
                message = {
                    "node": self.id,
                    "new_letter": selected_char,
                    "index": self.current_index,
                    "widget_name": "index",
                    "force_widget_update": True
                }
                print(f"[Python] Sending WebSocket message:")
                print(f"  - Message type: letter.update")
                print(f"  - Message data: {message}")
                
                try:
                    PromptServer.instance.send_sync("letter.update", message)
                    print(f"[Python] WebSocket message sent successfully")
                except Exception as e:
                    print(f"[Python] Error sending WebSocket message: {str(e)}")

                # Then update node (like prompt manager)
                try:
                    PromptServer.instance.send_sync("update_node", {
                        "node_id": unique_id,
                        "index_value": self.current_index,
                        "color": current_color,
                        "bgcolor": current_bgcolor
                    })
                except Exception as e:
                    print(f"[Python] Error updating node: {str(e)}")

                return (img, f"{char_description}")
                
            finally:
                # Restore the random state after execution
                random.setstate(random_state)

    def create_letter_image(self, letter, font_path, font_size,
                          image_width, image_height,
                          padding_top, padding_bottom, padding_left, padding_right,
                          font_color, background_color):
        img = Image.new("RGBA", (image_width, image_height), background_color)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, size=font_size)

        bbox = font.getbbox(letter)
        bbox_left, bbox_top, bbox_right, bbox_bottom = bbox
        letter_width = bbox_right - bbox_left
        letter_height = bbox_bottom - bbox_top

        x = padding_left + (image_width - padding_left - padding_right - letter_width) // 2 - bbox_left
        y = padding_top + (image_height - padding_top - padding_bottom - letter_height) // 2 - bbox_top

        draw.text((x, y), letter, font=font, fill=font_color)

        return torch.from_numpy(np.array(img).astype(np.float32) / 255.0).unsqueeze(0) 

    def create_letter_images(self, text, image_width, image_height,
                           padding_top, padding_bottom, padding_left, padding_right,
                           font_name, font_weight, font_color, background_color):
        # Remove spaces and get letters
        letters = [char for char in text if not char.isspace()]
        
        if not letters:
            # Return empty batch if no letters
            return (torch.zeros((1, image_height, image_width, 4)), "No letters found")

        # Get font path
        font_path = None
        if font_name in self.FONT_FILES:
            if font_weight in self.FONT_FILES[font_name]:
                font_path = self.FONT_FILES[font_name][font_weight]
            else:
                font_path = next(iter(self.FONT_FILES[font_name].values()))

        if not font_path:
            font_path = os.path.join(os.environ.get('SystemRoot', ''), 'Fonts', 'arial.ttf')

        # Find optimal font size for all letters to maintain consistency
        font_size = self.find_optimal_font_size_for_all_letters(
            letters, font_path, image_width, image_height,
            padding_top, padding_bottom, padding_left, padding_right
        )

        # Create a tensor to store all letter images
        letter_tensors = []

        for letter in letters:
            img = Image.new("RGBA", (image_width, image_height), background_color)
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(font_path, size=font_size)

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
            letter_tensors.append(torch.from_numpy(np.array(img).astype(np.float32) / 255.0).unsqueeze(0))

        # Stack all tensors into a single batch
        batch_tensor = torch.cat(letter_tensors, dim=0)

        return (batch_tensor, "Batch Mode") 