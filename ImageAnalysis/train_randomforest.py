import numpy as np
import pandas as pd
from skimage import io, measure, feature
from sklearn.ensemble import RandomForestClassifier
from stardist.models import StarDist2D
from openslide import OpenSlide
from stardist import random_label_cmap

# Define paths
model_weights_path = "StarDist/32_2D_versatile_he.pth"
slide_path = "/Users/jamieannemortel/Downloads/CMU-1.tiff"
classifier_save_path = "random_forest_classifier.pkl"
csv_save_path = "features.csv"

# Load whole slide image using OpenSlide
slide = OpenSlide(slide_path)

# Specify region to load based on the level and region dimensions
tile = np.array(slide.read_region((10000, 18400), 0, (988, 544)))

# Load StarDist model
model = StarDist2D(None, name='2D_versatile_he', basedir=None)
model.load_weights(model_weights_path)

# Perform segmentation
labels, _ = model.predict_instances(tile)

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
import matplotlib.pyplot as plt
cmap = random_label_cmap()
plt.imshow(labels, cmap=cmap)
plt.show()
