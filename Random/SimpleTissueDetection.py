import cv2
import numpy as np
from skimage.filters import threshold_otsu

def basic_tissue_detection(image_path, output_path):
    # Step 1: Read the Image
    image = cv2.imread(image_path)
    
    # Step 2: Convert to Grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Step 3: Apply Threshold (Otsu's method)
    thresh_val = threshold_otsu(gray_image)
    _, binary_mask = cv2.threshold(gray_image, thresh_val, 255, cv2.THRESH_BINARY_INV)
    
    # Step 4: Post-processing (optional, e.g., removing small objects)
    # For simplicity, this step is not included in this basic example
    
    # Saving the result
    cv2.imwrite(output_path, binary_mask)

    print(f"Processing complete. Result saved to {output_path}")

# Example usage
image_path = '/Users/jamieannemortel/Desktop/TissueDetectionMask_Input/tissue.jpg'  # Update this path
output_path = '/Users/jamieannemortel/Desktop/TissueDetectionMask_Output/binary_mask.jpg'  # Update this path
basic_tissue_detection(image_path, output_path)
