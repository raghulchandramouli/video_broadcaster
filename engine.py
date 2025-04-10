import cv2
from ultralytics import YOLO
import numpy as np
import torch

class CustomerSegmentationWithYolo():
    
    def __init__(self, erode_size=5, erode_intensity=2):
        self.model = YOLO("yolov8m-seg.pt")
        self.erode_size = erode_size
        self.erode_intensity = erode_intensity
        # Fix path with forward slashes for better compatibility
        self.background_image = cv2.imread("static/image.png")
        if self.background_image is None:
            print("Warning: Could not load background image. Check the path.")
        
        
    def generate_mask_from_result(self, results):
        for result in results:
            if result.masks:
                
                # Get array results:
                masks = result.masks.data
                boxes = result.boxes.data
                
                # Extract classes:
                clss = boxes[:, 5]
                
                # Get indices of results with class 0:
                people_indices = torch.where(clss == 0)
                
                # use these indices to extract the relavent masks:
                people_masks = masks[people_indices]
                
                if len(people_masks) == 0:
                    return None
                
                # scale for vizualing results:
                people_mask = torch.any(people_masks, dim=0).to(torch.uint8) * 255
                
                kernel = np.ones((self.erode_size, self.erode_size), np.uint8)
                eroded_mask = cv2.erode(people_mask.cpu().numpy(), kernel, iterations=self.erode_intensity)
                
                return eroded_mask
            
            else:
                return None
            
    
    def apply_blur_with_mask(self, frame, mask, blur_strength=21):
        # Apply blur to the frame using the mask:
        blurred_strength = (blur_strength, blur_strength)
        
        blurred_frame = cv2.GaussianBlur(frame, blur_strength, 0)
        
        mask = (mask > 0).astype(np.uint8)
        
        mask_3d = cv2.merge([mask, mask, mask])
        
        result_frame = np.where(mask_3d == 1, frame, blurred_frame)
        
        return result_frame
    
    def apply_black_background(self, frame, mask):
        black_background = np.zeros_like(frame)
        
        result_frame = np.where(mask[:, :, np.newaxis] == 255, frame, black_background)
        
        return result_frame
    
    def apply_custom_background(self, frame, mask):
        # Use absolute path to load the background image
        if self.background_image is None or self.background_image.size == 0:
            print("Warning: Background image not loaded properly")
            # Try with absolute path
            self.background_image = cv2.imread("c:\\Users\\raghu\\OneDrive\\Desktop\\video_broadcaster\\static\\image.png")
            
            # If still not loaded, create a solid color background
            if self.background_image is None or self.background_image.size == 0:
                print("Creating fallback background")
                self.background_image = np.ones_like(frame) * 120  # Gray background
        
        # Resize background to match frame dimensions
        background_image = cv2.resize(self.background_image, (frame.shape[1], frame.shape[0]))
        
        # Make sure mask is properly formatted
        mask_binary = (mask > 128).astype(np.uint8) * 255
        
        # Create 3-channel mask for proper blending
        mask_3d = np.stack([mask_binary, mask_binary, mask_binary], axis=2) / 255.0
        
        # Apply the mask using proper blending
        result_frame = (frame * mask_3d + background_image * (1 - mask_3d)).astype(np.uint8)
        
        return result_frame
        
