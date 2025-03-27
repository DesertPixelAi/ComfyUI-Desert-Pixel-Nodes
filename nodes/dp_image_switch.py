import random

import torch

import comfy.utils
from server import PromptServer


class DP_Image_And_String_Pairs_Switch:
    def __init__(self):
        self.current_index = 1
        self.id = str(random.randint(0, 2**64))

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "cycle_mode": (
                    ["fixed", "increment", "decrement"],
                    {"default": "fixed"},
                ),
                "index": ("INT", {"default": 1, "min": 1, "max": 5, "step": 1}),
            },
            "optional": {
                # Pair 1
                "Image_01": ("IMAGE",),
                "String_01": ("STRING", {"multiline": True, "forceInput": True}),
                # Pair 2
                "Image_02": ("IMAGE",),
                "String_02": ("STRING", {"multiline": True, "forceInput": True}),
                # Pair 3
                "Image_03": ("IMAGE",),
                "String_03": ("STRING", {"multiline": True, "forceInput": True}),
                # Pair 4
                "Image_04": ("IMAGE",),
                "String_04": ("STRING", {"multiline": True, "forceInput": True}),
                # Pair 5
                "Image_05": ("IMAGE",),
                "String_05": ("STRING", {"multiline": True, "forceInput": True}),
            },
            "hidden": {"unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("IMAGE", "STRING", "INT")
    RETURN_NAMES = ("IMAGE", "TEXT", "INDEX")
    FUNCTION = "process"
    CATEGORY = "DP/image"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def process(self, cycle_mode, index, unique_id, **kwargs):
        try:
            # Find connected pairs
            connected_indices = []
            for i in range(1, 6):
                if (
                    kwargs.get(f"Image_{i:02d}") is not None
                    or kwargs.get(f"String_{i:02d}") is not None
                ):
                    connected_indices.append(i)

            if not connected_indices:
                print("Warning: No connected inputs found")
                return (None, "", 1)

            # Handle cycling logic
            if cycle_mode == "fixed":
                # In fixed mode, require the specified index to be connected
                if index in connected_indices:
                    self.current_index = index
                else:
                    connected_str = ", ".join(map(str, connected_indices))
                    raise ValueError(
                        f"Selected index {index} is not connected. Available indices are: {connected_str}"
                    )
            else:
                # Find current position in connected indices
                try:
                    current_pos = connected_indices.index(self.current_index)
                except ValueError:
                    # If current index isn't in connected list, start from beginning
                    current_pos = -1

                # Calculate next position
                if cycle_mode == "increment":
                    next_pos = (current_pos + 1) % len(connected_indices)
                else:  # decrement
                    next_pos = (current_pos - 1) % len(connected_indices)

                self.current_index = connected_indices[next_pos]

            # Update UI
            try:
                PromptServer.instance.send_sync(
                    "dp_pair_update",
                    {"node_id": unique_id, "index": self.current_index},
                )
            except Exception as e:
                print(f"Error updating UI: {str(e)}")

            # Get selected image and text
            selected_image = kwargs.get(f"Image_{self.current_index:02d}")
            selected_text = kwargs.get(f"String_{self.current_index:02d}")

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

            return (selected_image, selected_text, self.current_index)

        except Exception as e:
            print(f"Error in DP_Image_And_String_Pairs_Switch: {str(e)}")
            return (None, "", 1)


class DP_10_Images_Switch_Or_Batch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["Switch_Mode", "Batch_Mode"], {"default": "Switch_Mode"}),
                "index": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1}),
            },
            "optional": {
                "Image_01": ("IMAGE", {"forceInput": True}),
                "Image_02": ("IMAGE", {"forceInput": True}),
                "Image_03": ("IMAGE", {"forceInput": True}),
                "Image_04": ("IMAGE", {"forceInput": True}),
                "Image_05": ("IMAGE", {"forceInput": True}),
                "Image_06": ("IMAGE", {"forceInput": True}),
                "Image_07": ("IMAGE", {"forceInput": True}),
                "Image_08": ("IMAGE", {"forceInput": True}),
                "Image_09": ("IMAGE", {"forceInput": True}),
                "Image_10": ("IMAGE", {"forceInput": True}),
            },
        }

    RETURN_TYPES = (
        "IMAGE",
        "INT",
    )
    RETURN_NAMES = (
        "IMAGE",
        "CURRENT_INDEX",
    )
    FUNCTION = "process"
    CATEGORY = "DP/image"

    def process(self, mode, index, **kwargs):
        try:
            if mode == "Switch_Mode":
                # Get selected image
                selected_key = f"Image_{index:02d}"
                img = kwargs.get(selected_key)

                if img is not None:
                    if len(img.shape) == 3:
                        img = img.unsqueeze(0)
                    # Ensure proper channel order
                    if img.shape[-1] != 3:
                        img = img.permute(0, 2, 3, 1)
                    return (img, index)
                else:
                    print(f"Warning: Selected input '{selected_key}' is not connected")
                    return (None, index)
            else:  # Batch_Mode
                # Collect all connected images
                images = []
                base_shape = None

                # First find a valid image to get base shape
                for i in range(1, 11):
                    img = kwargs.get(f"Image_{i:02d}")
                    if img is not None:
                        if len(img.shape) == 3:
                            img = img.unsqueeze(0)
                        if base_shape is None:
                            base_shape = img.shape[1:]  # Get C,H,W
                            images.append(img)
                        else:
                            # Resize if dimensions don't match
                            current_h, current_w = img.shape[2:]
                            target_h, target_w = base_shape[1:]
                            if (current_h, current_w) != (target_h, target_w):
                                print(
                                    f"Resizing Image_{i:02d} from {(current_h, current_w)} to {(target_h, target_w)}"
                                )
                                try:
                                    # Move channels to correct position for resizing
                                    samples = img.movedim(-1, 1)
                                    # Resize using lanczos
                                    resized = comfy.utils.common_upscale(
                                        samples, target_w, target_h, "lanczos", "center"
                                    )
                                    # Move channels back
                                    img = resized.movedim(1, -1)
                                except Exception as e:
                                    print(
                                        f"Warning: Failed to resize Image_{i:02d}: {str(e)}"
                                    )
                                    continue
                            images.append(img)

                if images:
                    # Concatenate all images into a batch
                    result = torch.cat(images, dim=0)
                    # Ensure proper channel order
                    if result.shape[-1] != 3:
                        result = result.permute(0, 2, 3, 1)
                    return (result, len(images))
                else:
                    print("Warning: No connected images found")
                    return (None, 0)

        except Exception as e:
            print(f"Error in DP_10_Images_Switch_Or_Batch: {str(e)}")
            return (None, 1)


class DP_3_Images_Switch_Or_Batch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["Switch_Mode", "Batch_Mode"], {"default": "Switch_Mode"}),
                "index": ("INT", {"default": 1, "min": 1, "max": 3, "step": 1}),
            },
            "optional": {
                "Image_01": ("IMAGE", {"forceInput": True}),
                "Image_02": ("IMAGE", {"forceInput": True}),
                "Image_03": ("IMAGE", {"forceInput": True}),
            },
        }

    RETURN_TYPES = (
        "IMAGE",
        "INT",
    )
    RETURN_NAMES = (
        "IMAGE",
        "CURRENT_INDEX",
    )
    FUNCTION = "process"
    CATEGORY = "DP/image"

    def process(self, mode, index, **kwargs):
        try:
            if mode == "Switch_Mode":
                # Get selected image
                selected_key = f"Image_{index:02d}"
                img = kwargs.get(selected_key)

                if img is not None:
                    if len(img.shape) == 3:
                        img = img.unsqueeze(0)
                    # Ensure proper channel order
                    if img.shape[-1] != 3:
                        img = img.permute(0, 2, 3, 1)
                    return (img, index)
                else:
                    print(f"Warning: Selected input '{selected_key}' is not connected")
                    return (None, index)
            else:  # Batch_Mode
                # Collect all connected images
                images = []
                base_shape = None

                # First find a valid image to get base shape
                for i in range(1, 4):
                    img = kwargs.get(f"Image_{i:02d}")
                    if img is not None:
                        if len(img.shape) == 3:
                            img = img.unsqueeze(0)
                        if base_shape is None:
                            base_shape = img.shape[1:]  # Get C,H,W
                            images.append(img)
                        else:
                            # Resize if dimensions don't match
                            current_h, current_w = img.shape[2:]
                            target_h, target_w = base_shape[1:]
                            if (current_h, current_w) != (target_h, target_w):
                                print(
                                    f"Resizing Image_{i:02d} from {(current_h, current_w)} to {(target_h, target_w)}"
                                )
                                try:
                                    samples = img.movedim(-1, 1)
                                    resized = comfy.utils.common_upscale(
                                        samples, target_w, target_h, "lanczos", "center"
                                    )
                                    img = resized.movedim(1, -1)
                                except Exception as e:
                                    print(
                                        f"Warning: Failed to resize Image_{i:02d}: {str(e)}"
                                    )
                                    continue
                            images.append(img)

                if images:
                    result = torch.cat(images, dim=0)
                    if result.shape[-1] != 3:
                        result = result.permute(0, 2, 3, 1)
                    return (result, len(images) - 1)
                else:
                    print("Warning: No connected images found")
                    return (None, 0)

        except Exception as e:
            print(f"Error in DP_3_Images_Switch_Or_Batch: {str(e)}")
            return (None, 0)


class DP_5_Images_Switch_Or_Batch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["Switch_Mode", "Batch_Mode"], {"default": "Switch_Mode"}),
                "index": ("INT", {"default": 1, "min": 1, "max": 5, "step": 1}),
            },
            "optional": {
                "Image_01": ("IMAGE", {"forceInput": True}),
                "Image_02": ("IMAGE", {"forceInput": True}),
                "Image_03": ("IMAGE", {"forceInput": True}),
                "Image_04": ("IMAGE", {"forceInput": True}),
                "Image_05": ("IMAGE", {"forceInput": True}),
            },
        }

    RETURN_TYPES = (
        "IMAGE",
        "INT",
    )
    RETURN_NAMES = (
        "IMAGE",
        "CURRENT_INDEX",
    )
    FUNCTION = "process"
    CATEGORY = "DP/image"

    def process(self, mode, index, **kwargs):
        try:
            if mode == "Switch_Mode":
                # Get selected image
                selected_key = f"Image_{index:02d}"
                img = kwargs.get(selected_key)

                if img is not None:
                    if len(img.shape) == 3:
                        img = img.unsqueeze(0)
                    # Ensure proper channel order
                    if img.shape[-1] != 3:
                        img = img.permute(0, 2, 3, 1)
                    return (img, index)
                else:
                    print(f"Warning: Selected input '{selected_key}' is not connected")
                    return (None, index)
            else:  # Batch_Mode
                # Collect all connected images
                images = []
                base_shape = None

                # First find a valid image to get base shape
                for i in range(1, 6):
                    img = kwargs.get(f"Image_{i:02d}")
                    if img is not None:
                        if len(img.shape) == 3:
                            img = img.unsqueeze(0)
                        if base_shape is None:
                            base_shape = img.shape[1:]  # Get C,H,W
                            images.append(img)
                        else:
                            # Resize if dimensions don't match
                            current_h, current_w = img.shape[2:]
                            target_h, target_w = base_shape[1:]
                            if (current_h, current_w) != (target_h, target_w):
                                print(
                                    f"Resizing Image_{i:02d} from {(current_h, current_w)} to {(target_h, target_w)}"
                                )
                                try:
                                    samples = img.movedim(-1, 1)
                                    resized = comfy.utils.common_upscale(
                                        samples, target_w, target_h, "lanczos", "center"
                                    )
                                    img = resized.movedim(1, -1)
                                except Exception as e:
                                    print(
                                        f"Warning: Failed to resize Image_{i:02d}: {str(e)}"
                                    )
                                    continue
                            images.append(img)

                if images:
                    result = torch.cat(images, dim=0)
                    if result.shape[-1] != 3:
                        result = result.permute(0, 2, 3, 1)
                    return (result, len(images) - 1)
                else:
                    print("Warning: No connected images found")
                    return (None, 0)

        except Exception as e:
            print(f"Error in DP_5_Images_Switch_Or_Batch: {str(e)}")
            return (None, 0)
