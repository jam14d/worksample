# Projects Repository
another test
## Image Analysis

### Overview
These projects are actively being developed to process whole slide images (WSI) using the StarDist model for nuclei segmentation. The aim is to calculate features of the segmented nuclei, performs classification based on these features, train a Random Forest classifier, and saves the model and extracted data. It also includes an optional visualization step for the segmented nuclei. As these projects are ongoing, additional functionalities and improvements may be integrated over time.


## Prerequisites
Ensure Python 3 is installed on your system. Python can be downloaded from the official Python website.

### Installation
Create and activate a virtual environment.

Install dependencies:
```
pip install numpy pandas scikit-image scikit-learn stardist openslide-python joblib matplotlib
```

### Usage
1. Segment nuclei using the StarDist model.
2. Calculate area, eccentricity, and mean intensity of each nucleus.
3. Train a Random Forest classifier based on the features extracted.
4. Save the model and data for further use.
5. Optionally visualize segmented nuclei.


## Code to Codons

### Overview
A Streamlit web application that simulates the conversion of text to DNA, applies mutations, and translates the DNA through RNA into protein sequences.

### Features
- Convert text to DNA sequence.
- Mutate DNA and transcribe into RNA.
- Translate RNA to protein and highlight stop codons.

## Prerequisites
Before you begin, ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/). This project assumes you are using Python Python 3.11.7.

### Installation
1. Clone the repo and navigate into the specific project directory.
2. Create a virtual environment and install dependencies.
3. Run the app with `streamlit run app.py`.

### Usage
Input text to convert and mutate into DNA, view the RNA transcription, and the resulting protein sequence with highlighted stop codons.

### Modules
Includes modules for DNA conversion, mutation, RNA transcription, and protein translation.

## Random Folder

The "random" folder within this repository contains a variety of projects at different stages of development. Many of these projects are works in progress, undergoing testing, refinement, or expansion. This folder serves as a creative sandbox, reflecting my ongoing exploration and experimentation with new ideas and technologies. While some projects in this folder may not be fully functional or documented, they offer a glimpse into my interests.