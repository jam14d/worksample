import os
import numpy as np
from PIL import Image
import cv2  # OpenCV for edge detection

# Set global threshold parameters here
CANNY_LOW_THRESHOLD = 30
CANNY_HIGH_THRESHOLD = 200

#OpenCv uses bgr
def extract_red_channel(image):
    image_array = np.array(image)
    red_channel = image_array[:, :, 0]  # Extract the red channel (0=Red, 1=Green, 2=Blue)
    return red_channel

def enhance_contrast(red_channel, contrast_factor=1, brightness_offset=-1):
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

    return superimposed

def process_tile(tile, contrast_factor, brightness_offset):
    # Process the tile by extracting red channel, enhancing contrast, and detecting edges
    red_channel = extract_red_channel(tile)
    red_channel_contrasted = enhance_contrast(red_channel, contrast_factor=contrast_factor, 
                                              brightness_offset=brightness_offset)
    edges = apply_canny_edge_detection(red_channel_contrasted)
    return superimpose_edges(tile, edges)

def stitch_tiles(tiles, image_size, tile_size):
    # Stitch the tiles back together into a full image
    stitched_image = Image.new("RGB", image_size)
    num_tiles_x = image_size[0] // tile_size[0]
    num_tiles_y = image_size[1] // tile_size[1]
    
    for i in range(num_tiles_x):
        for j in range(num_tiles_y):
            tile = tiles[i * num_tiles_y + j]
            stitched_image.paste(tile, (i * tile_size[0], j * tile_size[1]))
    return stitched_image

def process_and_save_image_by_tiles(input_image_path, output_dir, tile_size=(256, 256), 
                                    contrast_factor=1.0, brightness_offset=0):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the full image
    image = Image.open(input_image_path)
    image_width, image_height = image.size
    tiles = []

    # Process each tile
    for x in range(0, image_width, tile_size[0]):
        for y in range(0, image_height, tile_size[1]):
            box = (x, y, x + tile_size[0], y + tile_size[1])
            tile = image.crop(box)
            processed_tile = process_tile(tile, contrast_factor, brightness_offset)
            tiles.append(Image.fromarray(processed_tile))

    # Stitch tiles back together
    stitched_image = stitch_tiles(tiles, image.size, tile_size)

    # Save the final stitched image
    final_save_path = os.path.join(output_dir, "full_image_processed.png")
    stitched_image.save(final_save_path)
    print(f"Saved stitched image to {final_save_path}")

if __name__ == "__main__":
    input_image_path = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/TH_TAFA4_ROI_first try.tif"  # Replace with your input file path
    output_dir = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/output_stitch"  # Replace with your desired output directory

    # Adjust these values to experiment with contrast and brightness
    contrast_factor = 1  # Increase or decrease contrast
    brightness_offset = -1  # Adjust brightness (positive to brighten, negative to darken)

    # Run tile-based processing and save the stitched result
    process_and_save_image_by_tiles(input_image_path, output_dir, tile_size=(256, 256), 
                                    contrast_factor=contrast_factor, brightness_offset=brightness_offset)
