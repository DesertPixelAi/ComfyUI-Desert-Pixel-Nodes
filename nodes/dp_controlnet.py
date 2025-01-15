import torch
import comfy.controlnet
import folder_paths
import os

class DP_ControlNetApplyAdvanced:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"positive": ("CONDITIONING", ),
                             "negative": ("CONDITIONING", ),
                             "control_net": ("CONTROL_NET", ),
                             "image": ("IMAGE", ),
                             "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01}),
                             "start_percent": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                             "end_percent": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.001})
                             }}

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "STRING")
    RETURN_NAMES = ("positive", "negative", "control_info")
    FUNCTION = "apply_controlnet"

    CATEGORY = "Desert Pixel/conditioning"

    def apply_controlnet(self, positive, negative, control_net, image, strength, start_percent, end_percent):
        if strength == 0:
            return (positive, negative, "strength: 0 (controlnet disabled)")

        control_hint = image.movedim(-1,1)
        cnets = {}

        # Format the control info
        info = f"strength: {strength:.2f}\nstart_percent: {start_percent:.3f}\nend_percent: {end_percent:.3f}"
        
        out = []
        for conditioning in [positive, negative]:
            c = []
            for t in conditioning:
                d = t[1].copy()

                prev_cnet = d.get('control', None)
                if prev_cnet in cnets:
                    c_net = cnets[prev_cnet]
                else:
                    c_net = control_net.copy().set_cond_hint(control_hint, strength, (start_percent, end_percent))
                    c_net.set_previous_controlnet(prev_cnet)
                    cnets[prev_cnet] = c_net

                d['control'] = c_net
                d['control_apply_to_uncond'] = False
                n = [t[0], d]
                c.append(n)
            out.append(c)
        return (out[0], out[1], info)

class DP_Load_Controlnet_Model_With_Name:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "control_net_name": (folder_paths.get_filename_list("controlnet"), )}}

    RETURN_TYPES = ("CONTROL_NET", "STRING")
    RETURN_NAMES = ("control_net", "control_net_name")
    FUNCTION = "load_controlnet"

    CATEGORY = "Desert Pixel/loaders"

    def load_controlnet(self, control_net_name):
        controlnet_path = folder_paths.get_full_path_or_raise("controlnet", control_net_name)
        controlnet = comfy.controlnet.load_controlnet(controlnet_path)
        
        # Get just the filename without extension for the info
        name = "controlnet model: " + os.path.splitext(control_net_name)[0]
        return (controlnet, name) 