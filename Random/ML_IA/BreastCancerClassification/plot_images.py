import os
import matplotlib.pyplot as plt
import random
from PIL import Image

def plot_sample_images(dataset_dir, class_names, num_samples=5, figsize=(10, 10)):
    plt.figure(figsize=figsize)
    for i, class_name in enumerate(class_names):
        class_dir = os.path.join(dataset_dir, class_name)
        # Recursively find all image files within the class directory
        image_files = []
        for root, dirs, files in os.walk(class_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    image_files.append(os.path.join(root, file))
        if len(image_files) < num_samples:
            print(f"Warning: Not enough images in {class_name} class directory.")
            continue
        sample_images = random.sample(image_files, num_samples)
        for j, image_file in enumerate(sample_images):
            try:
                image = Image.open(image_file)
                plt.subplot(len(class_names), num_samples, i * num_samples + j + 1)
                plt.imshow(image)
                plt.title(class_name)
                plt.axis("off")                 
            except Exception as e:
                print(f"Error: {e}")
    plt.tight_layout()
    plt.show()

dataset_dir = "/Users/jamieannemortel/archive/BreaKHis_v1/BreaKHis_v1/histology_slides/breast"  # Update with the path to your dataset directory
class_names = ["benign", "malignant"]  # List of class names
plot_sample_images(dataset_dir, class_names)
