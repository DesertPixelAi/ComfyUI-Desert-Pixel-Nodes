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
    def _process_batch(img_tensor, process_func, *args):
        """Helper method to process batched images"""
        # Ensure we're working with batched input
        if len(img_tensor.shape) == 3:
            img_tensor = img_tensor.unsqueeze(0)
        
        # Convert to numpy with proper scaling
        img_np = (img_tensor.cpu().numpy() * 255).astype(np.uint8)
        
        # Process each image in batch
        results = []
        for i in range(img_np.shape[0]):
            # Process single image
            processed = process_func(img_np[i], *args)
            results.append(processed)
        
        # Stack results and convert back to tensor
        results = np.stack(results)
        return torch.from_numpy(results.astype(np.float32) / 255.0)

    @staticmethod
    def grayscale(img_tensor):
        # Convert to grayscale using tensor operations
        r, g, b = img_tensor[..., 0], img_tensor[..., 1], img_tensor[..., 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        # Stack the grayscale channel three times to maintain RGB format
        return torch.stack([gray, gray, gray], dim=-1)

    @staticmethod
    def flip_h(img_tensor):
        return torch.flip(img_tensor, dims=[2])

    @staticmethod
    def flip_v(img_tensor):
        return torch.flip(img_tensor, dims=[1])

    @staticmethod
    def posterize(img_tensor, levels):
        def process_single(img, lvls):
            img_pil = Image.fromarray(img)
            posterized = ImageOps.posterize(img_pil, bits=lvls)
            return np.array(posterized)
        return ImageEffects._process_batch(img_tensor, process_single, levels)

    @staticmethod
    def sharpen(img_tensor, factor):
        def process_single(img, f):
            img_pil = Image.fromarray(img)
            enhancer = ImageEnhance.Sharpness(img_pil)
            sharpened = enhancer.enhance(f)
            return np.array(sharpened)
        return ImageEffects._process_batch(img_tensor, process_single, factor)

    @staticmethod
    def contrast(img_tensor, strength=1.0):
        def process_single(img, f):
            img_pil = Image.fromarray(img)
            enhancer = ImageEnhance.Contrast(img_pil)
            contrasted = enhancer.enhance(0.5 + (f * 1.5))
            return np.array(contrasted)
        return ImageEffects._process_batch(img_tensor, process_single, strength)

    @staticmethod
    def equalize(img_tensor, strength=1.0):
        def process_single(img, f):
            if f <= 0:
                return img
            
            # Convert to LAB color space
            lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            
            # Apply CLAHE to L channel
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            l_eq = clahe.apply(l)
            
            # Merge channels back
            lab_eq = cv2.merge([l_eq, a, b])
            
            # Convert back to RGB
            equalized = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2RGB)
            
            # Blend between original and equalized
            return cv2.addWeighted(img, 1 - f, equalized, f, 0)
        return ImageEffects._process_batch(img_tensor, process_single, strength)

    @staticmethod
    def sepia(img_tensor, strength=1.0):
        def process_single(img, f):
            img_pil = Image.fromarray(img)
            sepia_filter = (
                0.393 + 0.607 * (1 - f), 0.769 - 0.769 * (1 - f), 0.189 - 0.189 * (1 - f), 0,
                0.349 - 0.349 * (1 - f), 0.686 + 0.314 * (1 - f), 0.168 - 0.168 * (1 - f), 0,
                0.272 - 0.272 * (1 - f), 0.534 - 0.534 * (1 - f), 0.131 + 0.869 * (1 - f), 0
            )
            sepia_img = img_pil.convert('RGB', sepia_filter)
            return np.array(sepia_img)
        return ImageEffects._process_batch(img_tensor, process_single, strength)

    @staticmethod
    def blur(img_tensor, strength):
        def process_single(img, f):
            img_pil = Image.fromarray(img)
            blurred = img_pil.filter(ImageFilter.GaussianBlur(radius=f))
            return np.array(blurred)
        return ImageEffects._process_batch(img_tensor, process_single, strength)
    
    @staticmethod
    def emboss(img_tensor, strength):
        def process_single(img, f):
            img_pil = Image.fromarray(img)
            embossed = img_pil.filter(ImageFilter.EMBOSS)
            enhancer = ImageEnhance.Contrast(embossed)
            embossed = enhancer.enhance(f)
            return np.array(embossed)
        return ImageEffects._process_batch(img_tensor, process_single, strength)

    @staticmethod
    def palette(img_tensor, color_count):
        def process_single(img, colors):
            img_pil = Image.fromarray(img)
            paletted = img_pil.convert('P', palette=Image.ADAPTIVE, colors=colors)
            reduced = paletted.convert('RGB')
            return np.array(reduced)
        return ImageEffects._process_batch(img_tensor, process_single, color_count)

    @staticmethod
    def enhance(img_tensor, strength=0.5):
        def process_single(img, f):
            img_pil = Image.fromarray(img)
            
            # Apply enhancements
            enhancer = ImageEnhance.Color(img_pil)
            img_pil = enhancer.enhance(1.0 + f * 0.5)
            
            enhancer = ImageEnhance.Contrast(img_pil)
            img_pil = enhancer.enhance(1.0 + f * 0.5)
            
            enhancer = ImageEnhance.Sharpness(img_pil)
            img_pil = enhancer.enhance(1.0 + f * 0.5)
            
            return np.array(img_pil)
        return ImageEffects._process_batch(img_tensor, process_single, strength)

    @staticmethod
    def solarize(img_tensor, threshold=0.5):
        def process_single(img, t):
            img_pil = Image.fromarray(img)
            solarized = ImageOps.solarize(img_pil, threshold=int(t * 255))
            return np.array(solarized)
        return ImageEffects._process_batch(img_tensor, process_single, threshold)

    @staticmethod
    def denoise(img_tensor, strength=1.0):
        def process_single(img, f):
            # Ensure input is uint8
            img_uint8 = img.astype(np.uint8)
            
            # Apply denoising with adjusted parameters
            denoised = cv2.fastNlMeansDenoisingColored(
                img_uint8,
                None,
                h=10.0 * f,  # Luminance component
                hColor=10.0 * f,  # Color component
                templateWindowSize=7,
                searchWindowSize=21
            )
            return denoised
        return ImageEffects._process_batch(img_tensor, process_single, strength)

    @staticmethod
    def vignette(img_tensor, intensity=0.75):
        def process_single(img, f):
            height, width = img.shape[:2]
            
            # Create radial gradient
            Y, X = np.ogrid[:height, :width]
            center_x, center_y = width/2, height/2
            dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
            max_dist = np.sqrt(center_x**2 + center_y**2)
            
            # Normalize and adjust intensity
            vignette_mask = 1 - (dist_from_center * f / max_dist)
            vignette_mask = np.clip(vignette_mask, 0, 1)
            
            # Expand mask to match image channels
            vignette_mask = np.expand_dims(vignette_mask, axis=-1)
            vignette_mask = np.repeat(vignette_mask, 3, axis=-1)
            
            # Apply vignette
            return (img * vignette_mask).astype(np.uint8)
        return ImageEffects._process_batch(img_tensor, process_single, intensity)

    @staticmethod
    def glow_edges(img_tensor, strength=0.75):
        def process_single(img, f):
            img_pil = Image.fromarray(img)
            # Edge detection
            edges = img_pil.filter(ImageFilter.FIND_EDGES)
            edges = edges.filter(ImageFilter.GaussianBlur(radius=2))
            # Enhance edges
            enhancer = ImageEnhance.Brightness(edges)
            glowing = enhancer.enhance(1.5)
            # Blend with original
            blended = Image.blend(img_pil, glowing, f)
            return np.array(blended)
        return ImageEffects._process_batch(img_tensor, process_single, strength)

    @staticmethod
    def new_effect(img_tensor, param1=1.0):
        # Your new effect implementation
        pass

    @staticmethod
    def edge_detect(img_tensor):
        def process_single(img, _):
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            return edges_rgb
        return ImageEffects._process_batch(img_tensor, process_single, None)

    @staticmethod
    def edge_gradient(img_tensor):
        def process_single(img, _):
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            magnitude = np.sqrt(sobelx**2 + sobely**2)
            magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
            magnitude_rgb = cv2.cvtColor(magnitude, cv2.COLOR_GRAY2RGB)
            return magnitude_rgb
        return ImageEffects._process_batch(img_tensor, process_single, None)

    @staticmethod
    def lineart_anime(img_tensor):
        def process_single(img, _):
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            edge = cv2.Canny(gray, 50, 150)
            edge = cv2.dilate(edge, np.ones((2, 2), np.uint8), iterations=1)
            edge_rgb = cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB)
            return edge_rgb
        return ImageEffects._process_batch(img_tensor, process_single, None)

    @staticmethod
    def threshold(img_tensor, strength=0.5):
        def process_single(img, f):
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            thresh_value = int(min(0.8, f) * 255)
            _, binary = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY)
            binary_rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
            return binary_rgb
        return ImageEffects._process_batch(img_tensor, process_single, strength)

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

    @staticmethod
    def rotate_90_ccw(img_tensor):
        return torch.rot90(img_tensor, k=1, dims=[-3, -2])

    @staticmethod
    def rotate_180(img_tensor):
        return torch.rot90(img_tensor, k=2, dims=[-3, -2])

    @staticmethod
    def rotate_270_ccw(img_tensor):
        return torch.rot90(img_tensor, k=3, dims=[-3, -2])

    @staticmethod
    def desaturate(img_tensor):
        # Convert to HSV using tensor operations
        img = img_tensor.clone()
        
        # Get RGB channels
        r, g, b = img[..., 0], img[..., 1], img[..., 2]
        
        # Calculate Value (max of RGB)
        v = torch.max(torch.max(r, g), b)
        
        # Calculate minimum of RGB
        min_rgb = torch.min(torch.min(r, g), b)
        
        # Calculate Saturation
        s = torch.where(v != 0, (v - min_rgb) / v, torch.zeros_like(v))
        
        # Reduce saturation (keeping 30% of original saturation)
        s = s * 0.3
        
        # Calculate delta
        delta = v * s
        
        # Calculate RGB values with reduced saturation
        if torch.numel(delta) > 0:
            min_rgb = v - delta
            
            # Recalculate RGB with new saturation
            mask = v != 0
            r = torch.where(mask, min_rgb + (r - min_rgb) * 0.3, r)
            g = torch.where(mask, min_rgb + (g - min_rgb) * 0.3, g)
            b = torch.where(mask, min_rgb + (b - min_rgb) * 0.3, b)
            
            # Stack channels back together
            return torch.stack([r, g, b], dim=-1)
        
        return img_tensor