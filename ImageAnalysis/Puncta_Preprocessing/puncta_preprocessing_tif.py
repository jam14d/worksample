import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

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

def superimpose_red_channel(original_tile, red_channel):
    # Create a new image for the superimposed result
    superimposed = np.array(original_tile).copy()

    # Blend the red channel with the original image
    superimposed[:, :, 0] = np.clip(superimposed[:, :, 0] + red_channel, 0, 255)  # Add red channel to red channel

    return Image.fromarray(superimposed)

def display_specific_tiles(tiles, tile_indices):
    plt.figure(figsize=(12, 8))

    for idx, position in enumerate(tile_indices):
        tile, _ = tiles[position]

        # Extract the red channel
        red_channel = extract_red_channel(tile)

        # Superimpose the red channel onto the original tile
        superimposed_image = superimpose_red_channel(tile, red_channel)

        # Display original tile
        plt.subplot(len(tile_indices), 3, idx * 3 + 1)
        plt.title(f"Original Tile {position}")
        plt.imshow(tile)
        plt.axis('off')

        # Display red channel as grayscale
        plt.subplot(len(tile_indices), 3, idx * 3 + 2)
        plt.title("Red Channel (Grayscale)")
        plt.imshow(red_channel, cmap='gray')
        plt.axis('off')

        # Display superimposed image
        plt.subplot(len(tile_indices), 3, idx * 3 + 3)
        plt.title("Superimposed Red Channel")
        plt.imshow(superimposed_image)
        plt.axis('off')

    plt.tight_layout()
    plt.show()  # Display the tiles
    plt.close('all')  # Close all figures after displaying

def preprocess_tif(input_tif_path, output_dir, tile_size=(256, 256), tile_indices=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tiles = tile_image(input_tif_path, tile_size)

    if tile_indices is None:
        tile_indices = [0, 1, 2, 3]  # Default to first four tiles

    display_specific_tiles(tiles, tile_indices)  # Show specified tiles and their channel variance

if __name__ == "__main__":
    input_tif_path = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/TH_TAFA4_ROI_first try.tif"  # Replace with your input file path
    output_dir = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/output"  # Replace with your desired output directory
    tile_size = (256, 256)  # Adjust tile size as needed
    tile_indices = [0, 25, 50, 100]  # Specify the indices of the tiles you want to display consistently
    #tile_indices = list(range(8))  # Specify the indices of the first eight tiles

    preprocess_tif(input_tif_path, output_dir, tile_size, tile_indices)


#tile 50 is good example