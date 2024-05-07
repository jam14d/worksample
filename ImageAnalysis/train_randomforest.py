import numpy as np
import pandas as pd
from skimage import io, measure, feature
from sklearn.ensemble import RandomForestClassifier
from stardist.models import StarDist2D
from openslide import OpenSlide
from stardist import random_label_cmap
import joblib
import matplotlib.pyplot as plt

##IN PROGRESS 
# Define paths
slide_path = "/Users/jamieannemortel/Downloads/OS-2.ndpi"
classifier_save_path = "random_forest_classifier.pkl"
csv_save_path = "features.csv"

# Load whole slide image using OpenSlide
slide = OpenSlide(slide_path)

# Specify region to load based on the level and region dimensions
tile = np.array(slide.read_region((10000, 18400), 0, (988, 544)))
tile = tile[:, :, :3]  # Keep only the first three channels (RGB) if four channels are detected

# Check the number of channels
if tile.ndim == 3 and tile.shape[2] == 3:
    print("Image has 3 channels.")
elif tile.ndim == 2:
    print("Image is grayscale and has 1 channel.")
else:
    print(f"Unexpected number of channels: {tile.shape[2]}")

# If model expects grayscale images, uncomment the next line
# tile = np.mean(tile, axis=2).astype(tile.dtype)  # Convert RGB to grayscale

# Initialize and load the StarDist model
model = StarDist2D.from_pretrained('2D_versatile_he')

# Perform segmentation with explicit axes specification
labels, _ = model.predict_instances(tile, axes='YXC')

# Calculate features for each segmented nucleus
properties = measure.regionprops_table(labels, tile, properties=('area', 'eccentricity', 'intensity_mean'))

# Convert to DataFrame
df = pd.DataFrame(properties)

# Assume a simplistic binary classification based on area
df['label'] = (df['area'] > 200).astype(int)

# Fit Random Forest Classifier
features = df[['area', 'eccentricity', 'intensity_mean']]
labels = df['label']
clf = RandomForestClassifier(n_estimators=25, random_state=42)
clf.fit(features, labels)

# Save classifier and features to disk
joblib.dump(clf, classifier_save_path)
df.to_csv(csv_save_path, index=False)

# Optionally, display the segmented nuclei (using matplotlib)
cmap = random_label_cmap()
plt.imshow(labels, cmap=cmap)
plt.show()
