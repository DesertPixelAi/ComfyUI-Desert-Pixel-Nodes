import os
import json
import colorsys
import numpy as np
import torch
from PIL import Image
from sklearn.cluster import KMeans
from skimage import color

class DP_Image_Color_Analyzer_Small:
    """Simplified ComfyUI node for analyzing image colors"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "num_colors": ("INT", {"default": 5, "min": 1, "max": 12, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("color_images", "color_theme")
    FUNCTION = "analyze_image"
    CATEGORY = "DP/Image"

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "color")
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.color_data = {}
        self.load_color_data()
        
        # Color analysis parameters
        self.min_color_distance = 15.0

    def load_color_data(self):
        """Load color definitions from JSON files"""
        try:
            self.color_data = {}
            color_files = ["color_names.json"]
            
            for filename in color_files:
                file_path = os.path.join(self.data_dir, filename)
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for category, colors in data.items():
                            if category not in self.color_data:
                                self.color_data[category] = {}
                            self.color_data[category].update(colors)
                            
            if not self.color_data:
                print("Warning: No color data loaded")
                
        except Exception as e:
            print(f"Error in load_color_data: {str(e)}")

    def calculate_color_distance(self, color1, color2):
        """Calculate color distance using Delta E"""
        try:
            lab1 = color.rgb2lab(np.array([color1]) / 255)
            lab2 = color.rgb2lab(np.array([color2]) / 255)
            return color.deltaE_cie76(lab1, lab2)[0]
        except Exception as e:
            print(f"Error calculating color distance: {e}")
            return float('inf')

    def get_color_name(self, rgb):
        """Find the closest matching color name"""
        try:
            min_distance = float('inf')
            closest_name = "undefined"
            closest_temp = None
            
            for category, colors in self.color_data.items():
                for color_name, data in colors.items():
                    ref_rgb = data.get('rgb', [0, 0, 0])
                    distance = self.calculate_color_distance(rgb, ref_rgb)
                    
                    if distance < min_distance:
                        min_distance = distance
                        sd_names = data.get('sd_names', [color_name])
                        closest_name = sd_names[0] if sd_names else color_name
                        closest_temp = data.get('temperature', None)
            
            return closest_name, closest_temp
            
        except Exception as e:
            print(f"Error finding color name: {e}")
            return "undefined", None

    def get_color_category(self, rgb):
        """Get basic color category"""
        try:
            h, s, v = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)
            h *= 360
            s *= 100
            v *= 100
            
            if v < 20:
                return "black"
            elif v > 80 and s < 20:
                return "white"
            elif s < 15:
                return "gray"
            
            if h < 30:
                return "red"
            elif h < 90:
                return "yellow"
            elif h < 150:
                return "green"
            elif h < 210:
                return "cyan"
            elif h < 270:
                return "blue"
            elif h < 330:
                return "magenta"
            else:
                return "red"
                
        except Exception as e:
            print(f"Error in get_color_category: {e}")
            return "undefined"

    def create_color_panel(self, hex_color):
        """Create a color panel tensor"""
        try:
            # Convert hex to RGB
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            
            # Create solid color image (256x256x3)
            color_array = np.full((256, 256, 3), [r, g, b], dtype=np.uint8)
            
            # Convert to tensor and add batch dimension (B,H,W,C)
            color_tensor = torch.from_numpy(color_array).float() / 255.0
            color_tensor = color_tensor.unsqueeze(0)  # Add batch dimension
            
            return color_tensor
            
        except Exception as e:
            print(f"Error creating color panel: {e}")
            return None

    def rgb_to_hex(self, rgb):
        """Convert RGB to hex color"""
        return f"#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}"

    def analyze_image(self, image, num_colors=5):
        """Analyze image colors and create color strip"""
        try:
            # Convert tensor to PIL Image
            if isinstance(image, torch.Tensor):
                if image.ndim == 4:
                    image = image.squeeze(0)
                img_array = (image * 255).byte().cpu().numpy()
                if img_array.shape[0] == 3:
                    img_array = np.transpose(img_array, (1, 2, 0))
                img = Image.fromarray(img_array)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize for processing
            img = img.resize((150, 150))
            
            # Convert to numpy array for K-means
            img_array = np.array(img)
            pixels = img_array.reshape(-1, 3)
            
            # Apply K-means clustering
            kmeans = KMeans(n_clusters=num_colors, random_state=42)
            kmeans.fit(pixels)
            colors = kmeans.cluster_centers_
            
            # Calculate color percentages
            labels = kmeans.labels_
            total_pixels = len(labels)
            percentages = [(np.sum(labels == i) / total_pixels) * 100 
                          for i in range(num_colors)]
            
            # Sort colors by percentage
            color_info = sorted(zip(colors, percentages), 
                              key=lambda x: x[1], 
                              reverse=True)
            
            # Process colors
            color_names = []
            color_panels = []
            
            # Generate color information
            for color, percentage in color_info[:num_colors]:
                rgb = tuple(map(int, color))
                hex_value = self.rgb_to_hex(rgb)
                
                # Get proper color name from the JSON data
                sd_name, _ = self.get_color_name(rgb)
                if sd_name != "undefined":
                    color_names.append(sd_name)
                else:
                    # Fallback to basic color category if no match found
                    category = self.get_color_category(rgb)
                    color_names.append(category)
                
                # Create color panel
                panel = self.create_color_panel(hex_value)
                if panel is not None:
                    color_panels.append(panel)
            
            # Combine color panels horizontally (B,H,W,C format)
            if color_panels:
                final_panels = torch.cat(color_panels, dim=2)  # Concatenate along width
            else:
                final_panels = torch.zeros(1, 256, 256, 3)
            
            # Generate theme string
            theme = " and ".join(color_names) + " color palette"
            
            return (final_panels, theme)
            
        except Exception as e:
            print(f"Error during image analysis: {e}")
            return (torch.zeros(1, 256, 256, 3), "Error analyzing colors") 