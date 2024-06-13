import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def rename(dataset):
    # Renaming the column "filename" to "path"
    dataset = dataset.rename(columns={"filename": "path"})
    # Displaying the first 5 entries to verify the renaming
    print(dataset.head())
    return dataset

def count_unique_patients(dataset):
    patients = set()
    for path in dataset['path']:
        patient_id = path.split("/")[3]  # Assuming the patient ID is in the 4th segment of the path
        patients.add(patient_id)
    return len(patients)

def visualize_dataset(dataset):
    sns.set(font_scale=1.5)
    sns.set_style("darkgrid")
    plt.figure(figsize=(10, 6))

    # Plot number of images
    plt.subplot(1, 2, 1)
    sns.countplot(data=dataset, x="grp")  # Change x to "grp"
    plt.xlabel("Class")
    plt.ylabel("Number of Images")
    plt.title("Distribution of Images in the Dataset")  



    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    # Load the dataset
    dataset = pd.read_csv("/Users/jamieannemortel/archive/Folds.csv")  # Update with the path to the CSV file

    # Rename the column "filename" to "path"
    dataset = rename(dataset)

    print(dataset.columns)  # Move print statement here

    visualize_dataset(dataset)
