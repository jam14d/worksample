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

def calculate_channel_variance_image(tile, channel_index):
    tile_array = np.array(tile)
    channel = tile_array[:, :, channel_index]  # Extract the specified channel (0=Red, 1=Green, 2=Blue)

    # Calculate pixel-wise variance of the channel
    variance = np.var(channel)

    # Normalize the channel for visualization as grayscale
    normalized_channel = (channel - np.min(channel)) / (np.max(channel) - np.min(channel)) * 255
    normalized_channel = normalized_channel.astype(np.uint8)

    return Image.fromarray(normalized_channel), variance, channel

def calculate_pixelwise_variance(channel):
    # Calculate pixel-wise variance
    return np.var(channel, axis=0)

def subtract_variance_from_channel(channel, pixelwise_variance):
    # Subtract the pixel-wise variance from the original channel
    subtracted_channel = np.clip(channel - pixelwise_variance, 0, 255)
    return subtracted_channel.astype(np.uint8)

def display_red_channel_tiles(tiles, tile_indices):
    plt.figure(figsize=(12, 8))  # Set the plot window size

    for idx, position in enumerate(tile_indices):
        tile, _ = tiles[position]

        # Calculate variance and get the red channel
        red_var_image, red_var, red_channel = calculate_channel_variance_image(tile, 0)  # Red channel is index 0

        # Calculate pixel-wise variance for the red channel
        pixelwise_variance = calculate_pixelwise_variance(red_channel)

        # Subtract the pixel-wise variance from the red channel
        subtracted_red_channel = subtract_variance_from_channel(red_channel, pixelwise_variance)
        subtracted_image = Image.fromarray(subtracted_red_channel)

        # Display original tile
        plt.subplot(len(tile_indices), 4, idx * 4 + 1)
        plt.title(f"Original Tile {position}")
        plt.imshow(tile)
        plt.axis('off')

        # Display red channel variance
        plt.subplot(len(tile_indices), 4, idx * 4 + 2)
        plt.title(f"Red Channel Variance: {red_var:.2f}")
        plt.imshow(red_var_image, cmap='gray')
        plt.axis('off')

        # Display red channel as grayscale
        plt.subplot(len(tile_indices), 4, idx * 4 + 3)
        plt.title("Red Channel Grayscale")
        plt.imshow(Image.fromarray(red_channel), cmap='gray')
        plt.axis('off')

        # Display the subtraction image
        plt.subplot(len(tile_indices), 4, idx * 4 + 4)
        plt.title("Red Channel - Variance")
        plt.imshow(subtracted_image, cmap='gray')
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

    display_red_channel_tiles(tiles, tile_indices)  # Show specified tiles and the channel processing

if __name__ == "__main__":
    input_tif_path = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/TH_TAFA4_ROI_first try.tif"  # Replace with your input file path
    output_dir = "/Users/jamieannemortel/Downloads/Work/Puncta Python Party/output"  # Replace with your desired output directory
    tile_size = (256, 256)  # Adjust tile size as needed
    tile_indices = [0, 1, 2, 3]  # Specify the indices of the tiles you want to display

    preprocess_tif(input_tif_path, output_dir, tile_size, tile_indices)
