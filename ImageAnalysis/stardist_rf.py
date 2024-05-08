import numpy as np
import matplotlib.pyplot as plt
from openslide import OpenSlide
from csbdeep.utils import normalize
from stardist.models import StarDist2D
from stardist.plot import render_label

def process_tile(tile):
    """
    Normalize and segment the tile using the StarDist 2D model pre-trained on H&E stained images.
    """
    try:
        tile = normalize(tile, 1, 99.8, axis=(0, 1))  # Normalize jointly across channels
        model = StarDist2D.from_pretrained("2D_versatile_he")
        labels, _ = model.predict_instances(tile)
        return labels
    except Exception as e:
        print(f"Error during segmentation: {e}")
        return None

def plot_results(tile, labels):
    """
    Plot original image and segmentation result side by side.
    """
    if tile is not None and labels is not None:
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        axes[0].imshow(tile)
        axes[0].set_title("Original Image")
        axes[0].axis('off')

        axes[1].imshow(render_label(labels, img=tile))
        axes[1].set_title("Segmentation with StarDist")
        axes[1].axis('off')
        plt.show()
    else:
        print("Failed to generate plots due to previous errors.")

def process_in_tiles(image_path, tile_size=(1000, 1000)):
    """
    Load and process an image in tiles using OpenSlide.
    """
    try:
        slide = OpenSlide(image_path)
        width, height = slide.dimensions
        for y in range(0, height, tile_size[1]):
            for x in range(0, width, tile_size[0]):
                tile = np.array(slide.read_region((x, y), 0, tile_size))
                labels = process_tile(tile[:, :, :3])  # Discard the alpha channel if present
                plot_results(tile[:, :, :3], labels)
    except Exception as e:
        print(f"Error loading or processing image: {e}")

if __name__ == "__main__":
    image_path = "/Users/jamieannemortel/Downloads/OS-2.ndpi"  # Path to your whole-slide image
    process_in_tiles(image_path, tile_size=(1000, 1000))
