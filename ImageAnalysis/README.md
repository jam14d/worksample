# Overview
These projects are designed to process whole slide images (WSI) using the StarDist model for nuclei segmentation. It calculates features of the segmented nuclei, performs binary classification based on these features, trains a Random Forest classifier, and saves the model and extracted data. The script also includes an optional visualization step for the segmented nuclei.

## Prerequisites
Ensure that Python 3 is installed on your system. You can download Python from the official website.

## Setting up the Virtual Environment
To isolate the dependencies required by this script, it's recommended to use a Python virtual environment. Below are the steps to set up and activate a virtual environment:

**Create the Virtual Environment:**
```python3 -m venv IA```

**Activate the Virtual Environment:**
 ```source IA/bin/activate```

**Installation of Dependencies:**
```pip install numpy pandas scikit-image scikit-learn stardist openslide-python joblib matplotlib```
