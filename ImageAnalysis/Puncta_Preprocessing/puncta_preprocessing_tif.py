import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
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

    return tiles

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

def display_specific_tiles(tiles, tile_indices, contrast_factor=1.0, brightness_offset=0):
    plt.figure(figsize=(12, 8))

    for idx, position in enumerate(tile_indices):
        tile, _ = tiles[position]

        # Extract the original red channel without contrast enhancement
        red_channel = extract_red_channel(tile)

        # Enhance contrast for the red channel
        red_channel_contrasted = enhance_contrast(red_channel, contrast_factor=contrast_factor, 
                                                  brightness_offset=brightness_offset)

        # Apply Canny Edge Detection to the enhanced red channel
        edges = apply_canny_edge_detection(red_channel_contrasted)

        # Superimpose edges onto the original tile
        superimposed_image = superimpose_edges(tile, edges)

        # Display original tile
        plt.subplot(len(tile_indices), 4, idx * 4 + 1)
        plt.title(f"Original Tile {position}")
        plt.imshow(tile)
        plt.axis('off')

        # Display red channel as grayscale
        plt.subplot(len(tile_indices), 4, idx * 4 + 2)
        plt.title("Red Channel (Grayscale)")
        plt.imshow(red_channel, cmap='gray')
        plt.axis('off')

        # Display contrast-enhanced red channel as grayscale
        plt.subplot(len(tile_indices), 4, idx * 4 + 3)
        plt.title(f"Enhanced Red Channel\n(Contrast: {contrast_factor}, Brightness: {brightness_offset})")
        plt.imshow(red_channel_contrasted, cmap='gray')
        plt.axis('off')

        # Display superimposed edges
        plt.subplot(len(tile_indices), 4, idx * 4 + 4)
        plt.title("Edges Superimposed")
        plt.imshow(superimposed_image)
        plt.axis('off')

    plt.tight_layout()
    plt.show()  # Display the tiles
    plt.close('all')  # Close all figures after displaying

def preprocess_tif(input_tif_path, output_dir, tile_size=(256, 256), tile_indices=None, contrast_factor=1.0, brightness_offset=0):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tiles = tile_image(input_tif_path, tile_size)

    if tile_indices is None:
        tile_indices = [0, 1, 2, 3]  # Default to first four tiles

    display_specific_tiles(tiles, tile_indices, contrast_factor=contrast_factor, brightness_offset=brightness_offset)

if __name__ == "__main__":
    input_tif_path = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/TH_TAFA4_ROI_first try.tif"  # Replace with your input file path
    output_dir = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/output"  # Replace with your desired output directory
    tile_size = (256, 256)  # Adjust tile size as needed
    tile_indices = [0, 50, 75, 150]  # Specify the indices of the tiles you want to display

    # Adjust these values to experiment with contrast
    contrast_factor = 1.2  # Increase or decrease contrast
    brightness_offset = -1  # Adjust brightness (positive to brighten, negative to darken)

    preprocess_tif(input_tif_path, output_dir, tile_size, tile_indices, 
                   contrast_factor=contrast_factor, brightness_offset=brightness_offset)
