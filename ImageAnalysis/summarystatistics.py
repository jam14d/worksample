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

# Extract class information from the filename column
dataset['class'] = dataset['filename'].apply(lambda x: 'benign' if 'benign' in x else 'malignant')

# Count the number of samples for each class
class_counts = dataset['class'].value_counts()

# Plot the number of samples for each class
plt.figure(figsize=(8, 6))
sns.barplot(x=class_counts.index, y=class_counts.values)
plt.xlabel("Class")
plt.ylabel("Number of Samples")
plt.title("Number of Samples for Benign and Malignant Classes")
plt.show()