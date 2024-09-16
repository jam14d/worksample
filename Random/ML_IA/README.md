
# Overview
These projects are actively being developed to process whole slide images (WSI) using the StarDist model for nuclei segmentation and to classify breast cancer histopathological images. The primary focus is on binary classification of breast cancer histopathological images into benign and malignant categories using convolutional neural networks (CNNs). As these projects are ongoing, additional functionalities and improvements may be integrated over time.


## Prerequisites
Ensure Python 3 is installed on your system. Python can be downloaded from the official Python website.

### Installation
Create and activate a virtual environment.

Install dependencies:
```
pip install numpy pandas scikit-image scikit-learn stardist openslide-python joblib matplotlib
```

### Usage for Stardist 
1. Segment nuclei using the StarDist model.
2. Optionally visualize segmented nuclei.

# Breast Cancer Histopathological Image Classification Overview

The ```breastcancerclassification.py``` performs binary classification of breast cancer histopathological images into benign and malignant categories using convolutional neural networks (CNNs). Before running the script, please ensure that you have the dataset prepared in the following format:


## Dataset Structure

The dataset directory should have the following structure:

``` 
dataset_dir/
    ├── benign/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    └── malignant/
        ├── image1.jpg
        ├── image2.jpg
        └── ...
``` 

## How It Works

This script performs binary classification of breast cancer histopathological images using convolutional neural networks (CNNs). It's a common task in medical image analysis where the goal is to automatically distinguish between benign (non-cancerous) and malignant (cancerous) tissue samples.

The repository is organized as follows:

- train.py: Python script for training the breast cancer classification model.
- predict.py: Python script for making predictions on new breast histology images using a pre-trained model.
- data_loader.py: Module for loading and preprocessing the BreaKHis dataset.
- model.py: Module containing the definition of the CNN model architecture.
- evaluation.py: Module for evaluating the performance of the trained model.
- imagepredictor.py: Module containing the ImagePredictor class for making predictions on new images.


## Requirements

- Python 3.x
- TensorFlow (or Keras): Deep learning libraries that provide tools for building and training neural networks.
- NumPy: A library for numerical operations, used for handling arrays and matrices of image data.
- Matplotlib: A plotting library for creating visualizations, used for displaying the ROC curve.
- scikit-learn: A machine learning library that includes tools for evaluating model performance, used for calculating the ROC curve and AUC.


## Usage

To train the breast cancer classification model, run the following command:

```python train.py```

To make predictions on a new breast histology image, update image_path in predict.py and run:

```python predict.py```

## Dataset
The BreaKHis dataset used in this project can be downloaded from https://www.kaggle.com/datasets/ambarish/breakhis.

Ensure the dataset is stored in the appropriate directory specified in data_loader.py.