# Overview

These projects are actively being developed to process whole slide images (WSI) using the StarDist model for nuclei segmentation. The aim is to calculate features of the segmented nuclei, performs classification based on these features, train a Random Forest classifier, and saves the model and extracted data. It also includes an optional visualization step for the segmented nuclei. As these projects are ongoing, additional functionalities and improvements may be integrated over time.

## Prerequisites
Ensure that Python 3 is installed on your system. You can download Python from the official website.

## Setting up the Virtual Environment
To isolate the dependencies required by this script, it's recommended to use a Python virtual environment. Below are the steps to set up and activate a virtual environment:

**Create the Virtual Environment:**
```python3 -m venv IA```

**Activate the Virtual Environment:**
 ```source IA/bin/activate```

**Installation of Dependencies:**
```pip install numpy pandas scikit-image scikit-learn stardist openslide-python joblib matplotlib keras```

For openslide troubleshooting tips, check out my blog: https://rb.gy/q1qnzc


# Breast Cancer Histopathological Image Classification

The ```breastcancerclassification.py``` performs binary classification of breast cancer histopathological images into benign and malignant categories using convolutional neural networks (CNNs). Before running the script, please ensure that you have the dataset prepared in the following format:

## Dataset Structure

The dataset directory should have the following structure:

dataset_dir/
    ├── benign/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    └── malignant/
        ├── image1.jpg
        ├── image2.jpg
        └── ...


## How It Works

This script performs binary classification of breast cancer histopathological images using convolutional neural networks (CNNs). It's a common task in medical image analysis where the goal is to automatically distinguish between benign (non-cancerous) and malignant (cancerous) tissue samples.

1. **Loading and Preprocessing Data**: The script loads the dataset of breast cancer histopathological images. It uses the `ImageDataGenerator` class from TensorFlow's Keras library for data loading and preprocessing. This class performs tasks like rescaling the pixel values of the images and splitting the dataset into training and validation sets.

2. **Building the Model**: The script defines a CNN model using the `Sequential` class from Keras. The model architecture consists of convolutional layers, max-pooling layers, and dense layers. This architecture is effective for learning spatial hierarchies of features in images.

3. **Compiling and Training the Model**: The model is compiled using the Adam optimizer and binary cross-entropy loss function. It's then trained on the training data using the `fit()` method. During training, the model adjusts its parameters (weights and biases) to minimize the loss and improve its performance.

4. **Evaluating the Model**: After training, the model's performance is evaluated on the validation set. The script calculates the probabilities of the images belonging to the positive class (malignant) using the `predict()` method. It then computes the receiver operating characteristic (ROC) curve and calculates the area under the curve (AUC) as a measure of the model's performance.

## Usage

1. **Dataset Preparation**: Obtain a dataset of breast cancer histopathological images. Organize the dataset into subdirectories representing the different classes (benign and malignant).

2. **Running the Script**: Set the `dataset_dir` variable in the script to the path of the dataset directory. Run the script using Python. It will train the CNN model and evaluate its performance using ROC curves and AUC.

3. **Interpreting Results**: After running the script, analyze the generated ROC curve and AUC score. These metrics provide insights into the model's ability to distinguish between benign and malignant tissue samples. A higher AUC score indicates better performance.


## Requirements

- Python 3.x
- TensorFlow (or Keras): Deep learning libraries that provide tools for building and training neural networks.
- NumPy: A library for numerical operations, used for handling arrays and matrices of image data.
- Matplotlib: A plotting library for creating visualizations, used for displaying the ROC curve.
- scikit-learn: A machine learning library that includes tools for evaluating model performance, used for calculating the ROC curve and AUC.