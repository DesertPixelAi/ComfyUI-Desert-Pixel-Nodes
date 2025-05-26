import random
import torch
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
import re

class DP_Words:
    IS_CHANGED = True

    def __init__(self):
        self.current_font_index = 0
        self.id = str(random.randint(0, 2**64))

    @staticmethod
    def find_font_files():
        # Improved font search: add more directories and always include node pack fonts folder
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        node_fonts_dir = os.path.join(base_dir, 'fonts')
        font_dirs = [
            os.path.join(os.environ.get('SystemRoot', ''), 'Fonts'),  # Windows
            os.path.expanduser('~/.fonts'),  # Linux user fonts
            os.path.expanduser('~/.local/share/fonts'),  # Linux user fonts
            '/usr/share/fonts',  # Linux system fonts
            '/Library/Fonts',  # MacOS
            '/System/Library/Fonts',  # MacOS
            node_fonts_dir,  # Always include node pack fonts
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

    FONT_FILES, FONT_WEIGHTS = find_font_files()

    @classmethod
    def INPUT_TYPES(cls):
        # Find fonts in the nodepack fonts folder only
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        node_fonts_dir = os.path.join(base_dir, 'fonts')
        nodepack_fonts = []
        for root, _, files in os.walk(node_fonts_dir):
            for file in files:
                if file.lower().endswith(('.ttf', '.otf')):
                    try:
                        font_path = os.path.join(root, file)
                        test_font = ImageFont.truetype(font_path, size=12)
                        font_name = test_font.getname()[0]
                        nodepack_fonts.append((font_name, font_path))
                    except Exception:
                        continue
        nodepack_font_names = [f[0] for f in nodepack_fonts]
        return {
            "required": {
                "font_selection_mode": (["Off", "Cycle", "Random"], {"default": "Off"}),
                "image_width": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "image_height": ("INT", {"default": 256, "min": 32, "max": 1024}),
                "font_name": (sorted(list(cls.FONT_FILES.keys())),),
                "font_weight": (cls.FONT_WEIGHTS,),
                "kerning": ("INT", {"default": 0, "min": -10, "max": 20}),
                "leading": ("INT", {"default": 0, "min": -100, "max": 100}),
                "padding_top": ("INT", {"default": 20, "min": 0, "max": 200}),
                "padding_bottom": ("INT", {"default": 20, "min": 0, "max": 200}),
                "padding_left": ("INT", {"default": 20, "min": 0, "max": 200}),
                "padding_right": ("INT", {"default": 20, "min": 0, "max": 200}),
                "align": (["Left", "Center", "Right"], {"default": "Center"}),
                "text": ("STRING", {"default": "WELCOME", "multiline": True}),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING",)
    RETURN_NAMES = ("image", "font_name", "info",)
    FUNCTION = "process_text"
    CATEGORY = "DP/Text"

    def find_optimal_font_size(self, text, font_path, image_width, image_height, padding_top, padding_bottom, padding_left, padding_right, kerning):
        available_width = image_width - padding_left - padding_right
        available_height = image_height - padding_top - padding_bottom
        min_size = 1
        max_size = min(available_width, available_height)
        optimal_size = min_size
        while min_size <= max_size:
            mid_size = (min_size + max_size) // 2
            font = ImageFont.truetype(font_path, size=mid_size)
            bbox = font.getbbox(text)
            bbox_width = bbox[2] - bbox[0] + kerning * (len(text) - 1)
            bbox_height = bbox[3] - bbox[1]
            if bbox_width <= available_width and bbox_height <= available_height:
                optimal_size = mid_size
                min_size = mid_size + 1
            else:
                max_size = mid_size - 1
        return optimal_size

    def find_optimal_font_size_multiline(self, lines, font_path, image_width, image_height, padding_top, padding_bottom, padding_left, padding_right, kerning, leading):
        available_width = image_width - padding_left - padding_right
        available_height = image_height - padding_top - padding_bottom
        min_size = 1
        max_size = min(available_width, available_height)
        optimal_size = min_size
        while min_size <= max_size:
            mid_size = (min_size + max_size) // 2
            font = ImageFont.truetype(font_path, size=mid_size)
            line_widths = []
            line_heights = []
            for line in lines:
                bbox = font.getbbox(line)
                width = bbox[2] - bbox[0] + kerning * (len(line) - 1)
                height = bbox[3] - bbox[1]
                line_widths.append(width)
                line_heights.append(height)
            total_height = sum(line_heights) + leading * (len(lines) - 1)
            max_line_width = max(line_widths) if line_widths else 0
            if max_line_width <= available_width and total_height <= available_height:
                optimal_size = mid_size
                min_size = mid_size + 1
            else:
                max_size = mid_size - 1
        return optimal_size

    def parse_line_size_kerning_leading(self, line, default_kerning, default_leading):
        # Look for @Sxx@, @Kyy@, and @Lzz@ markers at the end of the line (in any order)
        size_pct = 100
        kerning = default_kerning
        leading = default_leading
        # Find all markers
        matches = list(re.finditer(r'@(S(\d{1,3})|K(-?\d{1,3})|L(-?\d{1,3}))@', line))
        for m in matches:
            if m.group(2):  # Sxx
                size_pct = int(m.group(2))
            elif m.group(3):  # Kyy
                kerning = int(m.group(3))
            elif m.group(4):  # Lzz
                leading = int(m.group(4))
        # Remove all markers from the line
        clean_line = re.sub(r'@(S\d{1,3}|K-?\d{1,3}|L-?\d{1,3})@', '', line)
        return clean_line, size_pct, kerning, leading

    def process_text(self, font_selection_mode, image_width, image_height, font_name, font_weight, kerning, leading, padding_top, padding_bottom, padding_left, padding_right, align, text):
        import random
        # 1. Select font FIRST
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        node_fonts_dir = os.path.join(base_dir, 'fonts')
        nodepack_fonts = []
        for root, _, files in os.walk(node_fonts_dir):
            for file in files:
                if file.lower().endswith(('.ttf', '.otf')):
                    try:
                        font_path = os.path.join(root, file)
                        test_font = ImageFont.truetype(font_path, size=12)
                        font_name_found = test_font.getname()[0]
                        nodepack_fonts.append((font_name_found, font_path))
                    except Exception:
                        continue
        used_font_name = font_name
        font_path = None
        if font_selection_mode == "Off":
            if font_name in self.FONT_FILES:
                if font_weight in self.FONT_FILES[font_name]:
                    font_path = self.FONT_FILES[font_name][font_weight]
                else:
                    font_path = next(iter(self.FONT_FILES[font_name].values()))
            if not font_path:
                font_path = os.path.join(os.environ.get('SystemRoot', ''), 'Fonts', 'arial.ttf')
        elif font_selection_mode == "Cycle":
            if nodepack_fonts:
                self.current_font_index = (self.current_font_index + 1) % len(nodepack_fonts)
                used_font_name, font_path = nodepack_fonts[self.current_font_index]
            else:
                font_path = os.path.join(os.environ.get('SystemRoot', ''), 'Fonts', 'arial.ttf')
        elif font_selection_mode == "Random":
            if nodepack_fonts:
                prev_index = getattr(self, 'current_font_index', -1)
                while True:
                    idx = random.randint(0, len(nodepack_fonts) - 1)
                    if idx != prev_index or len(nodepack_fonts) == 1:
                        break
                self.current_font_index = idx
                used_font_name, font_path = nodepack_fonts[self.current_font_index]
            else:
                font_path = os.path.join(os.environ.get('SystemRoot', ''), 'Fonts', 'arial.ttf')
        # 2. Parse lines and settings
        raw_lines = text.splitlines() if text else [""]
        # Parse every line (including the first) for markers
        parsed_lines = []
        for line in raw_lines:
            clean_line, size_pct, line_kerning, line_leading = self.parse_line_size_kerning_leading(line, kerning, leading)
            parsed_lines.append((clean_line, size_pct, line_kerning, line_leading))
        # Build info string
        info_lines = [
            f"DP_Words Node: Generates a text image with per-line font size (@Sxx@), kerning (@Kxx@), and leading (@Lxx@) markers.",
            f"Font used: {used_font_name}",
            f"Lines: {len(parsed_lines)}"
        ]
        for idx, (clean_line, size_pct, line_kerning, line_leading) in enumerate(parsed_lines):
            info_lines.append(f"Line {idx+1}: '{clean_line}' | Size: {size_pct}% | Kerning: {line_kerning} | Leading: {line_leading}")
        info = "\n".join(info_lines)
        min_font_size = 4
        def block_height(base_font_size):
            heights = []
            for i, (line, size_pct, line_kerning, line_leading) in enumerate(parsed_lines):
                font = ImageFont.truetype(font_path, size=max(int(base_font_size * size_pct / 100), 1))
                bbox = font.getbbox(line)
                height = bbox[3] - bbox[1]
                heights.append(height)
            total = 0
            for i, h in enumerate(heights):
                total += h
                if i < len(parsed_lines) - 1:
                    total += parsed_lines[i][3]
            return total
        def max_line_width(base_font_size):
            widths = []
            for line, size_pct, line_kerning, line_leading in parsed_lines:
                font = ImageFont.truetype(font_path, size=max(int(base_font_size * size_pct / 100), 1))
                bbox = font.getbbox(line)
                width = bbox[2] - bbox[0] + line_kerning * (len(line) - 1)
                widths.append(width)
            return max(widths) if widths else 0
        available_width = image_width - padding_left - padding_right
        available_height = image_height - padding_top - padding_bottom
        lo, hi = min_font_size, min(available_width, available_height)
        base_font_size = lo
        while lo <= hi:
            mid = (lo + hi) // 2
            if max_line_width(mid) <= available_width and block_height(mid) <= available_height:
                base_font_size = mid
                lo = mid + 1
            else:
                hi = mid - 1
        # 3. Render to a large temporary image
        temp_w = image_width * 2
        temp_h = image_height * 2
        temp_img = Image.new("RGB", (temp_w, temp_h), "white")
        temp_draw = ImageDraw.Draw(temp_img)
        # Calculate all line heights and widths for final base_font_size
        line_heights = []
        line_widths = []
        fonts = []
        kernings = []
        leadings = []
        for line, size_pct, line_kerning, line_leading in parsed_lines:
            font = ImageFont.truetype(font_path, size=max(int(base_font_size * size_pct / 100), 1))
            bbox = font.getbbox(line)
            width = bbox[2] - bbox[0] + line_kerning * (len(line) - 1)
            height = bbox[3] - bbox[1]
            line_heights.append(height)
            line_widths.append(width)
            fonts.append(font)
            kernings.append(line_kerning)
            leadings.append(line_leading)
        total_height = 0
        for i, h in enumerate(line_heights):
            total_height += h
            if i < len(line_heights) - 1:
                total_height += leadings[i]
        # Draw all lines on the temp image, centered horizontally
        y = (temp_h - total_height) // 2
        for idx, (line, size_pct, line_kerning, line_leading) in enumerate(parsed_lines):
            font = fonts[idx]
            width = line_widths[idx]
            height = line_heights[idx]
            if align == "Left":
                x = 0
            elif align == "Right":
                x = temp_w - width
            else:
                x = (temp_w - width) // 2
            current_x = x
            for i, char in enumerate(line):
                temp_draw.text((current_x, y), char, font=font, fill="black")
                char_width = font.getbbox(char)[2] - font.getbbox(char)[0]
                current_x += char_width + kernings[idx]
            if idx < len(parsed_lines) - 1:
                y += height + leadings[idx]
            else:
                y += height
        # 4. Find the bounding box of all non-white pixels
        np_img = np.array(temp_img)
        mask = np.any(np_img != 255, axis=2)
        coords = np.argwhere(mask)
        if coords.size == 0:
            # No text drawn, return blank
            img = Image.new("RGB", (image_width, image_height), "white")
            return (torch.from_numpy(np.array(img).astype(np.float32) / 255.0).unsqueeze(0), used_font_name, info)
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1
        # 5. Crop and paste onto final canvas, aligned with padding
        cropped = temp_img.crop((x0, y0, x1, y1))
        crop_w, crop_h = cropped.size
        final_img = Image.new("RGB", (image_width, image_height), "white")
        # Alignment logic for pasting
        if align == "Left":
            paste_x = padding_left
        elif align == "Right":
            paste_x = image_width - padding_right - crop_w
        else:  # Center
            paste_x = padding_left + (image_width - padding_left - padding_right - crop_w) // 2
        paste_y = padding_top + (image_height - padding_top - padding_bottom - crop_h) // 2
        final_img.paste(cropped, (paste_x, paste_y))
        return (torch.from_numpy(np.array(final_img).astype(np.float32) / 255.0).unsqueeze(0), used_font_name, info) 