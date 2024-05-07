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
```pip install numpy pandas scikit-image scikit-learn stardist openslide-python joblib matplotlib```


For openslide troubleshooting tips, check out my blog: https://medium.com/@jamieannemortel/how-to-fix-openslide-library-not-found-error-by-updating-zshrc-on-macos-32538f857147
