import os
import json
from PIL import Image
import folder_paths
import numpy as np

class DP_Get_Seed_From_Image:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "image": ("IMAGE",),
            "filename": ("STRING", {"default": ""}),
        }}

    RETURN_TYPES = ("INT", "STRING",)
    RETURN_NAMES = ("seed", "seed_string",)
    FUNCTION = "get_seed"
    CATEGORY = "DP/analyze"

    def get_seed(self, image, filename):
        try:
            # First try to get metadata from the original file
            if filename:
                image_path = os.path.join(folder_paths.get_input_directory(), filename)
                if os.path.exists(image_path):
                    with Image.open(image_path) as img:
                        metadata = img.info
                        
                        for key in metadata:
                            try:
                                # Parse each metadata field as JSON
                                data = json.loads(metadata[key])
                                if isinstance(data, dict) and 'nodes' in data:
                                    # Look through all nodes
                                    for node in data['nodes']:
                                        if 'type' in node and 'widgets_values' in node:
                                            # Check for sampler nodes
                                            if any(sampler in node['type'].lower() for sampler in ['sampler', 'dp advanced sampler']):
                                                # The seed is typically the first value in widgets_values
                                                if node['widgets_values'] and isinstance(node['widgets_values'][0], (int, float)):
                                                    seed = int(node['widgets_values'][0])
                                                    return seed, str(seed)
                            except:
                                continue

            # If we couldn't find the seed from file, try from the tensor image
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = img.info
            
            for key in metadata:
                try:
                    data = json.loads(metadata[key])
                    if isinstance(data, dict) and 'nodes' in data:
                        for node in data['nodes']:
                            if 'type' in node and 'widgets_values' in node:
                                if any(sampler in node['type'].lower() for sampler in ['sampler', 'dp advanced sampler']):
                                    if node['widgets_values'] and isinstance(node['widgets_values'][0], (int, float)):
                                        seed = int(node['widgets_values'][0])
                                        return seed, str(seed)
                except:
                    continue
            
            # If we couldn't find the seed
            return 0, "No seed found"
            
        except Exception as e:
            print(f"Error extracting seed: {str(e)}")
            return 0, "Error extracting seed" 