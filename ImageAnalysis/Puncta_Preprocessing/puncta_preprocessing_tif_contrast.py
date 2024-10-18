import os
import numpy as np
from PIL import Image
import cv2  # OpenCV for edge detection

# Set global threshold parameters here
CANNY_LOW_THRESHOLD = 30
CANNY_HIGH_THRESHOLD = 200

def extract_red_channel(image):
    image_array = np.array(image)
    red_channel = image_array[:, :, 0]  # Extract the red channel (0=Red, 1=Green, 2=Blue)
    return red_channel

def enhance_contrast(red_channel, contrast_factor=2.0, brightness_offset=0):
    # Adjust contrast and brightness using OpenCV
    return cv2.convertScaleAbs(red_channel, alpha=contrast_factor, beta=brightness_offset)

def apply_canny_edge_detection(red_channel):
    # Use the global threshold values for Canny Edge Detection
    edges = cv2.Canny(red_channel, CANNY_LOW_THRESHOLD, CANNY_HIGH_THRESHOLD)
    return edges

def superimpose_edges(original_image, edges):
    # Create a new image for the superimposed result
    superimposed = np.array(original_image).copy()

    # Highlight the edges in red
    superimposed[edges != 0] = [255, 0, 0]  # Make the edge pixels fully red

    return Image.fromarray(superimposed)

def save_image(image_array, save_path):
    # Save the image from a numpy array using Pillow
    img = Image.fromarray(image_array)
    img.save(save_path)

def process_and_save_full_image(input_image_path, output_dir, contrast_factor=1.0, brightness_offset=0):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the full image
    image = Image.open(input_image_path)

    # Extract the original red channel
    red_channel = extract_red_channel(image)

    # Enhance contrast for the red channel
    red_channel_contrasted = enhance_contrast(red_channel, contrast_factor=contrast_factor, 
                                              brightness_offset=brightness_offset)

    # Apply Canny Edge Detection to the enhanced red channel
    edges = apply_canny_edge_detection(red_channel_contrasted)

    # Superimpose edges onto the original image
    superimposed_image = superimpose_edges(image, edges)

    # Save the red channel in grayscale
    grayscale_save_path = os.path.join(output_dir, "full_image_red_channel_grayscale.png")
    save_image(red_channel, grayscale_save_path)

    # Save the enhanced contrast red channel in grayscale
    enhanced_grayscale_save_path = os.path.join(output_dir, "full_image_enhanced_red_channel_grayscale.png")
    save_image(red_channel_contrasted, enhanced_grayscale_save_path)

    # Save the enhanced contrast red channel in its original form (RGB)
    image_array = np.array(image)
    image_array[:, :, 0] = red_channel_contrasted  # Replace the red channel with enhanced one
    enhanced_rgb_save_path = os.path.join(output_dir, "full_image_enhanced_red_channel_rgb.png")
    save_image(image_array, enhanced_rgb_save_path)

    # Save the superimposed edges image
    superimposed_save_path = os.path.join(output_dir, "full_image_edges_superimposed.png")
    superimposed_image.save(superimposed_save_path)

if __name__ == "__main__":
    input_image_path = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/TH_TAFA4_ROI_first try.tif"  # Replace with your input file path
    output_dir = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/output"  # Replace with your desired output directory

    # Adjust these values to experiment with contrast
    contrast_factor = 1.5  # Increase or decrease contrast
    brightness_offset = -3  # Adjust brightness (positive to brighten, negative to darken)

    process_and_save_full_image(input_image_path, output_dir, contrast_factor=contrast_factor, brightness_offset=brightness_offset)
