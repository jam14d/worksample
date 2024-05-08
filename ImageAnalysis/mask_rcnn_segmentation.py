import os
import numpy as np
import pandas as pd
from skimage import measure
import matplotlib.pyplot as plt
from openslide import OpenSlide

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers as KL
from tensorflow.keras import models as KM

# Ensure you are using an updated or compatible version of mrcnn that works with tf.keras
from mrcnn.config import Config
from mrcnn import model as modellib
from mrcnn import visualize
from mrcnn.model import load_image_gt
from mrcnn.model import mold_image


#optimizing on local is a pain -- work on colab for now?

# Configuration for inference
class InferenceConfig(Config):
    NAME = "nucleus"
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 1 + 1  # background + nucleus
    DETECTION_MIN_CONFIDENCE = 0.7

# Initialize configuration and model
config = InferenceConfig()
config.display()

# Create a Mask R-CNN model in inference mode
model = modellib.MaskRCNN(mode="inference", config=config, model_dir=os.getcwd())

# Load pre-trained weights, ensure they are the correct format for tf.keras
model.load_weights('path_to_coco_weights.h5', by_name=True)

# Load your image
slide_path = "/Users/jamieannemortel/Downloads/OS-2.ndpi"
slide = OpenSlide(slide_path)
tile = np.array(slide.read_region((10000, 18400), 0, (988, 544)))[:, :, :3]

# Detect objects
results = model.detect([tile], verbose=1)
r = results[0]

# Visualize results
visualize.display_instances(tile, r['rois'], r['masks'], r['class_ids'], 
                            ['BG', 'nucleus'], r['scores'])

# Additional processing can be added here to handle the masks or extract further features
