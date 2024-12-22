import torch
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import cv2

class ImageEffects:
    @staticmethod
    def _validate_input(img_tensor, function_name):
        """Validate input tensor"""
        if img_tensor is None:
            print(f"Warning: {function_name} received None input")
            return False
        if not isinstance(img_tensor, torch.Tensor):
            print(f"Warning: {function_name} expected torch.Tensor, got {type(img_tensor)}")
            return False
        if img_tensor.dim() != 4 and img_tensor.dim() != 3:
            print(f"Warning: {function_name} expected 3 or 4 dimensions, got {img_tensor.dim()}")
            return False
        return True

    @staticmethod
    def _tensor_to_numpy(img_tensor, function_name):
        """Safely convert tensor to numpy array"""
        try:
            if not ImageEffects._validate_input(img_tensor, function_name):
                print(f"Warning: {function_name} validation failed, returning original tensor")
                return (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
            # Ensure we're working with a 3D tensor (remove batch dimension if present)
            if img_tensor.dim() == 4:
                img_tensor = img_tensor.squeeze(0)
            img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
            return img_np
        except Exception as e:
            print(f"Warning: {function_name} error converting tensor to numpy: {str(e)}")
            return None

    @staticmethod
    def _convert_to_tensor(gray_img):
        """Helper method to convert grayscale numpy array to proper tensor format"""
        # Convert to 3 channels
        img_3ch = np.stack([gray_img, gray_img, gray_img], axis=-1)
        # Convert to float32 and normalize to 0-1
        img_float = img_3ch.astype(np.float32) / 255.0
        # Convert to tensor and add batch dimension
        return torch.from_numpy(img_float).unsqueeze(0)

    @staticmethod
    def grayscale(img_tensor):
        img_np = ImageEffects._tensor_to_numpy(img_tensor, "grayscale")
        if img_np is None:
            return img_tensor
        
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
        return torch.from_numpy(gray_rgb.astype(np.float32) / 255.0).unsqueeze(0)

    @staticmethod
    def flip_h(img_tensor):
        return torch.flip(img_tensor, dims=[2])

    @staticmethod
    def flip_v(img_tensor):
        return torch.flip(img_tensor, dims=[1])

    @staticmethod
    def posterize(img_tensor, levels):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        posterized = ImageOps.posterize(img_pil, bits=levels)
        img_np = np.array(posterized).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    @staticmethod
    def sharpen(img_tensor, factor):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        enhancer = ImageEnhance.Sharpness(img_pil)
        sharpened = enhancer.enhance(factor)
        img_np = np.array(sharpened).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    @staticmethod
    def contrast(img_tensor, strength=1.0):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        enhancer = ImageEnhance.Contrast(img_pil)
        contrasted = enhancer.enhance(0.5 + (strength * 1.5))
        img_np = np.array(contrasted).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    @staticmethod
    def equalize(img_tensor, strength=1.0):
        if strength <= 0:
            return img_tensor
        
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        
        # Convert to LAB color space
        lab = cv2.cvtColor(img_np, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        l_eq = clahe.apply(l)
        
        # Merge channels back
        lab_eq = cv2.merge([l_eq, a, b])
        
        # Convert back to RGB
        equalized = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2RGB)
        
        # Blend between original and equalized based on strength
        blended = cv2.addWeighted(img_np, 1 - strength, equalized, strength, 0)
        
        # Convert back to tensor format
        return torch.from_numpy(blended.astype(np.float32) / 255.0).unsqueeze(0)

    @staticmethod
    def sepia(img_tensor, strength=1.0):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        
        r = strength
        sepia_filter = (
            0.393 + 0.607 * (1 - r), 0.769 - 0.769 * (1 - r), 0.189 - 0.189 * (1 - r), 0,
            0.349 - 0.349 * (1 - r), 0.686 + 0.314 * (1 - r), 0.168 - 0.168 * (1 - r), 0,
            0.272 - 0.272 * (1 - r), 0.534 - 0.534 * (1 - r), 0.131 + 0.869 * (1 - r), 0
        )
        
        sepia_img = img_pil.convert('RGB', sepia_filter)
        img_np = np.array(sepia_img).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    @staticmethod
    def blur(img_tensor, strength):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        blurred = img_pil.filter(ImageFilter.GaussianBlur(radius=strength))
        img_np = np.array(blurred).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)
    
    @staticmethod
    def emboss(img_tensor, strength):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        embossed = img_pil.filter(ImageFilter.EMBOSS)
        enhancer = ImageEnhance.Contrast(embossed)
        embossed = enhancer.enhance(strength)
        img_np = np.array(embossed).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    @staticmethod
    def palette(img_tensor, color_count):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        paletted = img_pil.convert('P', palette=Image.ADAPTIVE, colors=color_count)
        reduced = paletted.convert('RGB')
        img_np = np.array(reduced).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    @staticmethod
    def enhance(img_tensor, strength=0.5):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        
        contrast = ImageEnhance.Contrast(img_pil)
        img_pil = contrast.enhance(1 + (0.2 * strength))
        
        sharpener = ImageEnhance.Sharpness(img_pil)
        img_pil = sharpener.enhance(1 + (0.3 * strength))
        
        color = ImageEnhance.Color(img_pil)
        img_pil = color.enhance(1 + (0.1 * strength))
        
        equalized = ImageOps.equalize(img_pil)
        equalized_np = np.array(equalized)
        original_np = np.array(img_pil)
        blend_factor = 0.2 * strength
        blended = (1 - blend_factor) * original_np + blend_factor * equalized_np
        
        final_np = np.clip(blended, 0, 255).astype(np.uint8)
        img_np = np.array(final_np).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    @staticmethod
    def solarize(img_tensor, threshold=0.5):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        solarized = ImageOps.solarize(img_pil, threshold=int(threshold * 255))
        img_np = np.array(solarized).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    @staticmethod
    def denoise(img_tensor, strength=0.5):
        size = max(3, min(9, int(strength * 9)))
        if size % 2 == 0:
            size -= 1
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        blurred = img_pil.filter(ImageFilter.MedianFilter(size=size))
        img_np = np.array(blurred).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    @staticmethod
    def vignette(img_tensor, intensity=0.75):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        height, width = img_np.shape[:2]
        
        # Create radial gradient
        center_x, center_y = width/2, height/2
        Y, X = np.ogrid[:height, :width]
        dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        max_dist = np.sqrt(center_x**2 + center_y**2)
        
        # Normalize and adjust intensity
        vignette_mask = 1 - (dist_from_center * intensity / max_dist)
        vignette_mask = np.clip(vignette_mask, 0, 1)
        vignette_mask = vignette_mask[..., np.newaxis]
        
        # Apply vignette
        vignetted = (img_np * vignette_mask).astype(np.uint8)
        img_np = vignetted.astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    @staticmethod
    def glow_edges(img_tensor, strength=0.75):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        
        # Edge detection
        edges = img_pil.filter(ImageFilter.FIND_EDGES)
        edges = edges.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Enhance edges
        enhancer = ImageEnhance.Brightness(edges)
        glowing = enhancer.enhance(1.5)
        
        # Blend with original
        blend_factor = strength
        blended = Image.blend(img_pil, glowing, blend_factor)
        
        img_np = np.array(blended).astype(np.float32) / 255.0
        return torch.from_numpy(img_np).unsqueeze(0)

    @staticmethod
    def new_effect(img_tensor, param1=1.0):
        # Your new effect implementation
        pass

    @staticmethod
    def edge_detect(img_tensor):
        img_np = ImageEffects._tensor_to_numpy(img_tensor, "edge_detect")
        if img_np is None:
            return img_tensor
            
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        edges = cv2.Canny(gray, 100, 200)
        edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        return torch.from_numpy(edges_rgb.astype(np.float32) / 255.0).unsqueeze(0)

    @staticmethod
    def edge_gradient(img_tensor):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        # Convert back to RGB
        magnitude_rgb = cv2.cvtColor(magnitude, cv2.COLOR_GRAY2RGB)
        return torch.from_numpy(magnitude_rgb.astype(np.float32) / 255.0).unsqueeze(0)

    @staticmethod
    def lineart_anime(img_tensor):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        edge = cv2.Canny(gray, 50, 150)
        edge = cv2.dilate(edge, np.ones((2, 2), np.uint8), iterations=1)
        # Convert back to RGB
        edge_rgb = cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB)
        return torch.from_numpy(edge_rgb.astype(np.float32) / 255.0).unsqueeze(0)

    @staticmethod
    def threshold(img_tensor, strength=0.5):
        img_np = ImageEffects._tensor_to_numpy(img_tensor, "threshold")
        if img_np is None:
            return img_tensor
            
        strength = min(0.8, strength)
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        thresh_value = int(strength * 255)
        _, binary = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
        binary_rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
        return torch.from_numpy(binary_rgb.astype(np.float32) / 255.0).unsqueeze(0)

    @staticmethod
    def pencil_sketch(img_tensor, strength=0.5):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        # Ensure we're working with RGB
        if len(img_np.shape) != 3:
            img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2RGB)
        
        # Convert to grayscale for processing
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        
        # Create inverted blurred image
        inv = 255 - gray
        blur_size = max(3, min(25, int(strength * 25)))
        if blur_size % 2 == 0:
            blur_size += 1
        blur = cv2.GaussianBlur(inv, (blur_size, blur_size), 0)
        
        # Divide gray by inverted blurred image
        sketch = cv2.divide(gray, 255 - blur, scale=256.0)
        
        # Enhance contrast
        sketch = cv2.normalize(sketch, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        
        # Convert back to RGB
        sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
        return torch.from_numpy(sketch_rgb.astype(np.float32) / 255.0).unsqueeze(0)

    @staticmethod
    def relief_shadow(img_tensor, strength=0.5):
        img_np = (img_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np
        kernel = np.array([[0,0,0], [0,1,0], [0,0,-1]]) * strength
        relief = cv2.filter2D(gray, -1, kernel) + 128
        return ImageEffects._convert_to_tensor(relief)

    @staticmethod
    def original(img_tensor, _=None):
        return img_tensor

    def rotate_90_ccw(self, image):
        return torch.rot90(image, k=1, dims=[-3, -2])

    def rotate_180(self, image):
        return torch.rot90(image, k=2, dims=[-3, -2])

    def rotate_270_ccw(self, image):
        return torch.rot90(image, k=3, dims=[-3, -2])