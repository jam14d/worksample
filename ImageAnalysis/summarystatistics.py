from breastcancerclassification import BreastCancerClassifier  # Import the BreastCancerClassifier class from breastcancerclassification.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
dataset = pd.read_csv("/Users/jamieannemortel/Downloads/archive/Folds.csv")  # Update with the path to your dataset

# Extract tissue type from the path
dataset['tissue_type'] = dataset['filename'].apply(lambda x: x.split("/")[5])  # Assuming tissue type is in the 6th segment of the path

# Plot statistics of tissue types
plt.figure(figsize=(10, 6))
sns.countplot(data=dataset, x="tissue_type")
plt.xlabel("Tissue Type")
plt.ylabel("Count")
plt.title("Summary Statistics of Tissue Types")
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.show()