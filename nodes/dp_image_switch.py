import torch
import comfy.utils
import random
from server import PromptServer

class DP_Image_Switch_3_Inputs:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Source": (["Image_1", "Image_2", "Image_3", "batch"], {"default": "Image_1"}),
            },
            "optional": {
                "Image_1": ("IMAGE",),
                "Image_2": ("IMAGE",),
                "Image_3": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "DP/image"

    def process(self, Source, **kwargs):
        try:
            if Source == "batch":
                Image_Batches = []
                base_shape = None
                
                # First find a valid image to get base shape
                for i in range(1, 4):
                    img = kwargs.get(f"Image_{i}")
                    if img is not None:
                        if len(img.shape) == 3:
                            img = img.unsqueeze(0)
                        base_shape = img.shape[1:]  # Get C,H,W
                        Image_Batches.append(img)
                        break
                
                if not base_shape:
                    print("No valid images found for batch mode")
                    return (None,)
                
                target_h, target_w = base_shape[1:]
                
                # Now collect and resize remaining images to match base shape
                for i in range(1, 4):
                    img = kwargs.get(f"Image_{i}")
                    if img is not None and not any(torch.equal(img, x) for x in Image_Batches):
                        if len(img.shape) == 3:
                            img = img.unsqueeze(0)
                            
                        # Resize if dimensions don't match
                        current_h, current_w = img.shape[2:]
                        if (current_h, current_w) != (target_h, target_w):
                            print(f"Resizing Image_{i} from {(current_h, current_w)} to {(target_h, target_w)}")
                            try:
                                # Move channels to correct position for resizing
                                samples = img.movedim(-1,1)
                                # Resize using lanczos
                                resized = comfy.utils.common_upscale(samples, target_w, target_h, "lanczos", "center")
                                # Move channels back
                                img = resized.movedim(1,-1)
                            except Exception as e:
                                print(f"Warning: Failed to resize Image_{i}: {str(e)}")
                                continue
                            
                        Image_Batches.append(img)
                
                # Return concatenated batch if we have images
                if Image_Batches:
                    result = torch.cat(Image_Batches, dim=0)
                    # Ensure proper channel order
                    if result.shape[-1] != 3:
                        result = result.permute(0, 2, 3, 1)
                    return (result,)
                return (None,)
                    
            else:
                # Single image mode
                img = kwargs.get(Source)
                if img is not None:
                    if len(img.shape) == 3:
                        img = img.unsqueeze(0)
                    # Ensure proper channel order
                    if img.shape[-1] != 3:
                        img = img.permute(0, 2, 3, 1)
                    return (img,)
                else:
                    print(f"Warning: Selected input '{Source}' is not connected")
                    return (None,)
            
        except Exception as e:
            print(f"Error in DP_Image_Switch_3_Inputs: {str(e)}")
            return (None,)

class DP_Image_Switch_5_Inputs:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Source": (["Image_1", "Image_2", "Image_3", "Image_4", "Image_5", "batch"], {"default": "Image_1"}),
            },
            "optional": {
                "Image_1": ("IMAGE", {"forceInput": True}),
                "Image_2": ("IMAGE", {"forceInput": True}),
                "Image_3": ("IMAGE", {"forceInput": True}),
                "Image_4": ("IMAGE", {"forceInput": True}),
                "Image_5": ("IMAGE", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "DP/image"

    def process(self, Source, **kwargs):
        try:
            if Source == "batch":
                images = []
                for i in range(1, 6):
                    img = kwargs.get(f"Image_{i}")
                    if img is not None:
                        if len(img.shape) == 3:
                            img = img.unsqueeze(0)
                        images.append(img)
                
                if not images:
                    return (None,)
                
                if len(images) > 1:
                    return (torch.cat(images, dim=0),)
                return (images[0],)
            else:
                selected = kwargs.get(Source.lower())
                return (selected,) if selected is not None else (None,)
                
        except Exception as e:
            print(f"Error in DP_Image_Switch_5_Inputs: {str(e)}")
            return (None,)

class DP_Image_Switch_10_Inputs:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Source": (["Image_1", "Image_2", "Image_3", "Image_4", "Image_5",
                           "Image_6", "Image_7", "Image_8", "Image_9", "Image_10",
                           "batch"], {"default": "Image_1"}),
            },
            "optional": {
                "Image_1": ("IMAGE",),
                "Image_2": ("IMAGE",),
                "Image_3": ("IMAGE",),
                "Image_4": ("IMAGE",),
                "Image_5": ("IMAGE",),
                "Image_6": ("IMAGE",),
                "Image_7": ("IMAGE",),
                "Image_8": ("IMAGE",),
                "Image_9": ("IMAGE",),
                "Image_10": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "DP/image"

    def process(self, Source, **kwargs):
        try:
            if Source == "batch":
                # Following animation calculator pattern
                Image_Batches = []
                
                # Collect all valid images
                for i in range(1, 11):
                    img = kwargs.get(f"Image_{i}")
                    if img is not None:
                        # Ensure image is in batch format
                        if len(img.shape) == 3:
                            img = img.unsqueeze(0)
                        Image_Batches.append(img)
                
                # Return concatenated batch if we have images
                if Image_Batches:
                    return (torch.cat(Image_Batches, dim=0),)
                    
            else:
                # Single image mode
                img = kwargs.get(Source)
                if img is not None:
                    return (img if len(img.shape) == 4 else img.unsqueeze(0),)
            
            # If we get here, return empty batch with correct dimensions
            return (torch.zeros((1, 3, 64, 64), dtype=torch.float32),)
                
        except Exception as e:
            print(f"Error in DP_Image_Switch_10_Inputs: {str(e)}")
            return (torch.zeros((1, 3, 64, 64), dtype=torch.float32),) 

class DP_Image_And_String_Pairs_Switch:
    def __init__(self):
        self.current_index = 0
        self.id = str(random.randint(0, 2**64))
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Source": (["Pair_01", "Pair_02", "Pair_03", "Pair_04", "Pair_05", "batch"], {"default": "Pair_01"}),
                "cycle_mode": (["fixed", "increment", "decrement"], {"default": "fixed"}),
                "index": ("INT", {"default": 0, "min": 0, "max": 4}),
            },
            "optional": {
                "Image_1": ("IMAGE",),
                "Image_2": ("IMAGE",),
                "Image_3": ("IMAGE",),
                "Image_4": ("IMAGE",),
                "Image_5": ("IMAGE",),
                "String_1": ("STRING", {"multiline": True, "forceInput": True}),
                "String_2": ("STRING", {"multiline": True, "forceInput": True}),
                "String_3": ("STRING", {"multiline": True, "forceInput": True}),
                "String_4": ("STRING", {"multiline": True, "forceInput": True}),
                "String_5": ("STRING", {"multiline": True, "forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "INT")
    RETURN_NAMES = ("IMAGE", "TEXT", "INDEX")
    FUNCTION = "process"
    CATEGORY = "DP/image"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def process(self, Source, cycle_mode, index, unique_id, **kwargs):
        try:
            if Source == "batch":
                # Batch mode processing remains the same
                Image_Batches = []
                String_Parts = []
                base_shape = None
                indices = []
                
                for i in range(1, 6):
                    img = kwargs.get(f"Image_{i}")
                    text = kwargs.get(f"String_{i}")
                    
                    if img is not None:
                        if len(img.shape) == 3:
                            img = img.unsqueeze(0)
                        
                        if base_shape is None:
                            base_shape = img.shape[1:]
                            Image_Batches.append(img)
                        else:
                            current_h, current_w = img.shape[2:]
                            target_h, target_w = base_shape[1:]
                            
                            if (current_h, current_w) != (target_h, target_w):
                                print(f"Resizing Image_{i} from {(current_h, current_w)} to {(target_h, target_w)}")
                                try:
                                    samples = img.movedim(-1,1)
                                    resized = comfy.utils.common_upscale(samples, target_w, target_h, "lanczos", "center")
                                    img = resized.movedim(1,-1)
                                except Exception as e:
                                    print(f"Warning: Failed to resize Image_{i}: {str(e)}")
                                    continue
                            
                            Image_Batches.append(img)
                        
                        if text is not None:
                            if isinstance(text, list):
                                text = " ".join(str(x) for x in text)
                            String_Parts.append(text.strip())
                            indices.append(i)
                
                if Image_Batches:
                    result_image = torch.cat(Image_Batches, dim=0)
                    result_text = ", ".join(String_Parts) if String_Parts else ""
                    return (result_image, result_text, indices[0] if indices else 0)
                
                return (None, "", 0)
            
            else:
                # Handle cycling logic
                next_index = self.current_index
                
                # Handle fixed mode and user input changes
                if cycle_mode == "fixed":
                    if index != self.current_index:
                        next_index = max(0, min(index, 4))
                        self.current_index = next_index
                # Handle increment/decrement modes
                elif cycle_mode == "increment":
                    next_index = (self.current_index + 1) % 5
                    self.current_index = next_index
                elif cycle_mode == "decrement":
                    next_index = (self.current_index - 1) % 5
                    self.current_index = next_index
                
                # Update UI widget using custom event
                try:
                    PromptServer.instance.send_sync("dp_pair_update", {
                        "node_id": unique_id,
                        "index": self.current_index
                    })
                except Exception as e:
                    print(f"Error updating UI: {str(e)}")
                
                # Convert current_index to pair number (1-5)
                pair_num = self.current_index + 1
                
                # Get selected image and text
                selected_image = kwargs.get(f"Image_{pair_num}")
                selected_text = kwargs.get(f"String_{pair_num}")
                
                # Process image
                if selected_image is not None:
                    if len(selected_image.shape) == 3:
                        selected_image = selected_image.unsqueeze(0)
                
                # Process text
                if selected_text is not None:
                    if isinstance(selected_text, list):
                        selected_text = " ".join(str(x) for x in selected_text)
                    selected_text = selected_text.strip()
                else:
                    selected_text = ""
                
                return (selected_image, selected_text, pair_num)
            
        except Exception as e:
            print(f"Error in DP_Image_And_String_Pairs_Switch: {str(e)}")
            return (None, "", 0) 