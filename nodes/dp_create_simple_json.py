import os
import json

class DP_create_json_file:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "file_name": ("STRING", {"default": "my_json_file"}),
                "save_path": ("STRING", {"default": "output\\json"}),
                "line_separator": ("STRING", {"default": "|"}),
                "json_data": ("STRING", {"multiline": True, "default": "item1 name | item2 name | item3 name\nwakeup | world | 06758\ndesert | pixel | 12354"}),
                "save_file": ("BOOLEAN", {"default": True}),
                "overwrite": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("json_text", "log_info")
    FUNCTION = "process"
    CATEGORY = "DP/utils"

    def process(self, file_name: str, save_path: str, line_separator: str, json_data: str, save_file: bool, overwrite: bool):
        try:
            # Clean and validate input data
            lines = [line.strip() for line in json_data.split('\n') if line.strip()]
            if not lines:
                return "", "Error: No data provided"
            
            # Parse header using custom separator and get column count
            headers = [h.strip() for h in lines[0].split(line_separator)]
            columns = len(headers)
            
            # Convert headers to valid JSON keys (remove spaces, special chars)
            headers = [h.lower().replace(' ', '_') for h in headers]
            
            # Process data lines using custom separator
            json_items = []
            for i, line in enumerate(lines[1:], 1):
                values = [v.strip() for v in line.split(line_separator)]
                if len(values) != columns:
                    return "", f"Error: Line {i+1} has {len(values)} columns but expected {columns}"
                
                item = dict(zip(headers, values))
                json_items.append(item)
            
            # Create JSON string with proper formatting
            json_text = json.dumps(json_items, indent=2)
            
            # If save_file is False, return early with success message
            if not save_file:
                return json_text, "JSON data created. No file saved because save is set to false"
            
            # Handle file saving
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            base_name = os.path.join(save_path, file_name)
            final_path = f"{base_name}.json"
            
            # Handle file naming conflicts
            if not overwrite and os.path.exists(final_path):
                counter = 1
                while os.path.exists(f"{base_name}_{counter:03d}.json"):
                    counter += 1
                final_path = f"{base_name}_{counter:03d}.json"
            
            # Save the file
            with open(final_path, 'w', encoding='utf-8') as f:
                f.write(json_text)
            
            log_info = f"File created successfully and saved to: {final_path}"
            return json_text, log_info
            
        except Exception as e:
            return "", f"Error: {str(e)}"

# Node registration info
NODE_CLASS_MAPPINGS = {
    "DP_create_json_file": DP_create_json_file
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_create_json_file": "Create JSON File"
}