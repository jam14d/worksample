import json
import numpy as np
import matplotlib.pyplot as plt
from openslide import OpenSlide
from csbdeep.utils import normalize
from stardist.models import StarDist2D
from stardist.plot import render_label

def process_tile(tile):
    try:
        tile = normalize(tile, 1, 99.8, axis=(0, 1))  # Normalize jointly across channels
        model = StarDist2D.from_pretrained("2D_versatile_he")
        labels, _ = model.predict_instances(tile)
        return labels
    except Exception as e:
        print(f"Error during segmentation: {e}")
        return None

def plot_results(tile, labels):
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

def process_specific_region(image_path, coordinates):
    """
    Process a specified region using coordinates.
    """
    try:
        slide = OpenSlide(image_path)
        # Calculate bounding box from coordinates
        x_coords, y_coords = zip(*coordinates)
        x, y, width, height = min(x_coords), min(y_coords), max(x_coords) - min(x_coords), max(y_coords) - min(y_coords)

        # Read region defined by bounding box
        region = slide.read_region((x, y), 0, (width, height))
        region = np.array(region)[:, :, :3]  # Convert to RGB and remove alpha if present
        labels = process_tile(region)
        plot_results(region, labels)
    except Exception as e:
        print(f"Error processing region: {e}")

def parse_geojson(geojson_path):
    """
    Parse a GeoJSON file to extract polygon coordinates.
    """
    with open(geojson_path, 'r') as file:
        data = json.load(file)
    coordinates = data['geometry']['coordinates'][0]
    return coordinates

if __name__ == "__main__":
    image_path = "/Users/jamieannemortel/Downloads/OS-2.ndpi"
    geojson_path = "/Users/jamieannemortel/sampleproj_qp/OS-2.geojson"
    coordinates = parse_geojson(geojson_path)
    process_specific_region(image_path, coordinates)
