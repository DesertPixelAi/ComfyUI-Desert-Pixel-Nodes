import folder_paths
import random
from nodes import LoraLoader
import torch
import comfy
import gc
import os

class DP_Five_Lora_Random:
    """
    ComfyUI node for loading up to five LoRA models with random strength values.
    """
    def __init__(self):
        self.lora_loader = LoraLoader()  # Reuse single instance
    
    @classmethod
    def INPUT_TYPES(cls):
        lora_files = ['None'] + folder_paths.get_filename_list("loras")  # Cache list
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "loader_state": (["ON", "OFF"],),
                "Lora_01": (lora_files,),
                "Lora_01_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Min": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Max": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
            },
            "optional": {
                "Lora_02": (lora_files,),
                "Lora_02_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Min_2": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Max_2": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_03": (lora_files,),
                "Lora_03_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Min_3": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Max_3": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_04": (lora_files,),
                "Lora_04_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Min_4": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Max_4": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_05": (lora_files,),
                "Lora_05_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Min_5": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Max_5": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING")
    RETURN_NAMES = ("model", "clip", "lora_info")
    FUNCTION = "apply_lora"
    CATEGORY = "DP/loaders"
    
    IS_CHANGED = True

    def get_random_strength(self, strength, min_val, max_val):
        if min_val == 0 and max_val == 0:
            return strength
        return round(random.uniform(min_val, max_val), 2)

    def apply_lora(self, model, clip, loader_state,
                  Lora_01, Lora_01_Strength, Random_Min, Random_Max,
                  Lora_02="None", Lora_02_Strength=1.0, Random_Min_2=0.0, Random_Max_2=0.0,
                  Lora_03="None", Lora_03_Strength=1.0, Random_Min_3=0.0, Random_Max_3=0.0,
                  Lora_04="None", Lora_04_Strength=1.0, Random_Min_4=0.0, Random_Max_4=0.0,
                  Lora_05="None", Lora_05_Strength=1.0, Random_Min_5=0.0, Random_Max_5=0.0):
        
        if loader_state == "OFF":
            return (model, clip, "LoRA Models Info:\nBypassed - No LoRAs applied")

        weights_info = ["LoRA Models Info:"]
        loras = [
            (Lora_01, Lora_01_Strength, Random_Min, Random_Max),
            (Lora_02, Lora_02_Strength, Random_Min_2, Random_Max_2),
            (Lora_03, Lora_03_Strength, Random_Min_3, Random_Max_3),
            (Lora_04, Lora_04_Strength, Random_Min_4, Random_Max_4),
            (Lora_05, Lora_05_Strength, Random_Min_5, Random_Max_5)
        ]
        
        # Process all LoRAs in a single loop
        for lora_name, base_strength, min_val, max_val in loras:
            if lora_name != "None":
                strength = self.get_random_strength(base_strength, min_val, max_val)
                model, clip = self.lora_loader.load_lora(
                    model, clip, lora_name, strength, strength
                )
                weights_info.append(f"{lora_name}: {strength}")
        
        return (model, clip, "\n".join(weights_info))

class OptimizedLoraLoader:
    _lora_cache = {}  # Cache for loaded LoRA models
    _weight_cache = {}  # Cache for preloaded weights
    
    @classmethod
    def preload_weights(cls, lora_name):
        """Preload LoRA weights into RAM"""
        lora_path = folder_paths.get_full_path("loras", lora_name)
        if lora_path not in cls._weight_cache:
            cls._weight_cache[lora_path] = comfy.utils.load_torch_file(lora_path)

    def load_lora(self, model, clip, lora_names, strengths):
        """Batch load multiple LoRAs efficiently"""
        # Preload all weights
        for lora_name in lora_names:
            self.preload_weights(lora_name)
            
        # Batch process LoRAs
        with torch.cuda.amp.autocast():
            for lora_name, strength in zip(lora_names, strengths):
                lora_path = folder_paths.get_full_path("loras", lora_name)
                
                # Use cached weights if available
                if lora_path in self._weight_cache:
                    lora_weights = self._weight_cache[lora_path]
                else:
                    lora_weights = comfy.utils.load_torch_file(lora_path)
                
                # Apply LoRA with optimizations
                model, clip = self._apply_lora_optimized(
                    model, clip, lora_weights, strength
                )
        
        return (model, clip)

    def _apply_lora_optimized(self, model, clip, lora_weights, strength):
        """Optimized LoRA application"""
        # Use mixed precision
        with torch.cuda.amp.autocast():
            # Batch process weight updates
            for key in lora_weights:
                if key.startswith("lora_unet_"):
                    self._apply_weight_update(model, lora_weights[key], strength)
                elif key.startswith("lora_te_"):
                    self._apply_weight_update(clip, lora_weights[key], strength)
        
        return model, clip

    @staticmethod
    def _apply_weight_update(target_model, weight, strength):
        """Optimized weight update"""
        # Use in-place operations where possible
        if hasattr(target_model, "weight"):
            target_model.weight.data.add_(weight * strength)

class BaseOptimizedLoader:
    @staticmethod
    def setup_optimizations():
        if torch.cuda.is_available():
            # Enable TF32 
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            
            # Optimize CUDA allocator
            torch.cuda.set_per_process_memory_fraction(0.95)  # Use more GPU memory
            torch.cuda.empty_cache()
            
            # Enable cudnn benchmarking
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False
            
            # Set optimal thread settings
            torch.set_num_threads(6)  # Adjust based on CPU cores
            torch.set_num_interop_threads(6)

class MemoryOptimizer:
    @staticmethod
    def clear_cache():
        """Aggressive cache clearing"""
        torch.cuda.empty_cache()
        gc.collect()
    
    @staticmethod
    def optimize_memory():
        """Memory optimization settings"""
        if torch.cuda.is_available():
            # Fragment memory less
            torch.cuda.set_per_process_memory_fraction(0.95)
            
            # Use unified memory pool
            torch.cuda.set_allocator_settings({
                'max_split_size_mb': 128,
                'roundup_power2_divisions': 8,
            })

def batch_process_loras(model, clip, lora_configs):
    """Process multiple LoRAs in batches"""
    with torch.cuda.amp.autocast():
        # Sort LoRAs by size for better memory management
        lora_configs.sort(key=lambda x: os.path.getsize(x['path']))
        
        # Process in batches
        batch_size = 2  # Adjust based on available memory
        for i in range(0, len(lora_configs), batch_size):
            batch = lora_configs[i:i+batch_size]
            
            # Load and apply batch
            for config in batch:
                model, clip = apply_lora(model, clip, config)
                
            # Clear intermediate memory
            torch.cuda.empty_cache()

class OptimizedModelLoader:
    def __init__(self):
        self.setup_optimizations()
        self.memory_optimizer = MemoryOptimizer()
    
    def load_model(self, model_path):
        with torch.cuda.amp.autocast():
            model = torch.jit.script(self._load_base_model(model_path))
            return model.cuda()
    
    def apply_loras(self, model, lora_configs):
        # Sort by size and batch process
        return batch_process_loras(model, self.clip, lora_configs)