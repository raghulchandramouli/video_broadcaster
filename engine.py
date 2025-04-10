import cv2
from ultralytics import YOLO
import numpy as np
import torch

class CustomerSegmentationWithYolo():
    
    def __init__(self):
        self.model = YOLO("yolov8m-seg.pt")
        self.background_image = cv2.imread("static\image.png")
        
        
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
                people_mask = torch.any(people_masks, dim=0).to(torch.unit8) * 255
                
                return people_mask
            
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
        background_image = cv2.resize(self.background_image, (frame.shape[1], frame.shape[0]))
        
        # Apply the masks:
        result_frame = np.where(mask[:, :, np.newaxis] == 255, frame, background_image)
        return result_frame
        
