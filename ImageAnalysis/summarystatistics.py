from breastcancerclassification import BreastCancerClassifier  # Import the BreastCancerClassifier class from breastcancerclassification.py
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
dataset = pd.read_csv("/Users/jamieannemortel/Downloads/archive/Folds.csv")  # Update with the path to your dataset

# Extract tissue type from the path
dataset['tissue_type'] = dataset['filename'].apply(lambda x: x.split("/")[5])  # Assuming tissue type is in the 6th segment of the path

# Extract class information from the filename column
dataset['class'] = dataset['filename'].apply(lambda x: 'benign' if 'benign' in x else 'malignant')

# Count the number of samples for each class
class_counts = dataset['class'].value_counts()

# Plot the number of samples for each class and tissue types side by side
plt.figure(figsize=(16, 6))

# Subplot for tissue types
plt.subplot(1, 2, 1)
sns.countplot(data=dataset, x="tissue_type")
plt.xlabel("Tissue Type")
plt.ylabel("Count")
plt.title("Summary Statistics of Tissue Types")
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

# Subplot for number of samples for each class
plt.subplot(1, 2, 2)
sns.barplot(x=class_counts.index, y=class_counts.values)
plt.xlabel("Class")
plt.ylabel("Number of Samples")
plt.title("Number of Samples for Benign and Malignant Classes")

# Print the number of samples for each class
print("Number of samples for each class:")
for class_name, count in class_counts.items():
    print(f"{class_name.capitalize()}: {count}")

plt.tight_layout()  # Adjust layout to prevent overlapping
plt.show()
