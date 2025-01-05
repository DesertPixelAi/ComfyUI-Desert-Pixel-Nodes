import torch
import comfy.utils

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