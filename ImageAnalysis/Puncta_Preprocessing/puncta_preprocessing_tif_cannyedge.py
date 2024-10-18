import os
import numpy as np
from PIL import Image
import cv2  # OpenCV for edge detection

# Set global threshold parameters here
CANNY_LOW_THRESHOLD = 30
CANNY_HIGH_THRESHOLD = 200

def tile_image(input_tif_path, tile_size=(256, 256)):
    img = Image.open(input_tif_path)
    img_width, img_height = img.size
    tiles = []

    # Create tiles
    for i in range(0, img_width, tile_size[0]):
        for j in range(0, img_height, tile_size[1]):
            box = (i, j, min(i + tile_size[0], img_width), min(j + tile_size[1], img_height))
            tile = img.crop(box)
            tiles.append((tile, (i, j)))

    return tiles, img_width, img_height

def extract_red_channel(tile):
    tile_array = np.array(tile)
    red_channel = tile_array[:, :, 0]  # Extract the red channel (0=Red, 1=Green, 2=Blue)
    return red_channel

def enhance_contrast(red_channel, contrast_factor=2.0, brightness_offset=0):
    # Adjust contrast and brightness using OpenCV
    return cv2.convertScaleAbs(red_channel, alpha=contrast_factor, beta=brightness_offset)

def apply_canny_edge_detection(red_channel):
    # Use the global threshold values for Canny Edge Detection
    edges = cv2.Canny(red_channel, CANNY_LOW_THRESHOLD, CANNY_HIGH_THRESHOLD)
    return edges

def superimpose_edges(original_tile, edges):
    # Create a new image for the superimposed result
    superimposed = np.array(original_tile).copy()

    # Highlight the edges in red
    superimposed[edges != 0] = [255, 0, 0]  # Make the edge pixels fully red

    return Image.fromarray(superimposed)

def process_tile(tile, contrast_factor=1.0, brightness_offset=0):
    # Extract the red channel from the tile
    red_channel = extract_red_channel(tile)

    # Enhance contrast for the red channel
    red_channel_contrasted = enhance_contrast(red_channel, contrast_factor=contrast_factor, brightness_offset=brightness_offset)

    # Apply Canny Edge Detection to the enhanced red channel
    edges = apply_canny_edge_detection(red_channel_contrasted)

    # Superimpose edges onto the original tile
    superimposed_image = superimpose_edges(tile, edges)

    return superimposed_image

def stitch_tiles(tiles, tile_size, img_width, img_height):
    # Create an empty canvas for the full image
    full_image = Image.new('RGB', (img_width, img_height))

    # Paste each processed tile back into its original position
    for tile, (i, j) in tiles:
        full_image.paste(tile, (i, j))

    return full_image

def preprocess_and_save_full_image(input_tif_path, output_dir, tile_size=(256, 256), contrast_factor=1.0, brightness_offset=0):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get tiles and image dimensions
    tiles, img_width, img_height = tile_image(input_tif_path, tile_size)

    processed_tiles = []
    
    # Process each tile
    for tile, position in tiles:
        processed_tile = process_tile(tile, contrast_factor=contrast_factor, brightness_offset=brightness_offset)
        processed_tiles.append((processed_tile, position))

    # Stitch all processed tiles back into the full image
    full_image = stitch_tiles(processed_tiles, tile_size, img_width, img_height)

    # Save the full processed image
    output_image_path = os.path.join(output_dir, "processed_full_image.png")
    full_image.save(output_image_path)
    print(f"Processed full image saved at {output_image_path}")

if __name__ == "__main__":
    input_tif_path = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/TH_TAFA4_ROI_first try.tif"  # Replace with your input file path
    output_dir = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/"  # Replace with your desired output directory
    tile_size = (256, 256)  # Adjust tile size as needed

    # Adjust these values to experiment with contrast
    contrast_factor = 1.2  # Increase or decrease contrast
    brightness_offset = -1  # Adjust brightness (positive to brighten, negative to darken)

    preprocess_and_save_full_image(input_tif_path, output_dir, tile_size, contrast_factor=contrast_factor, brightness_offset=brightness_offset)
