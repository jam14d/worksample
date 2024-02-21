import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

'''
Uses .txt files containing stardist segmentation measurements, exported from the open-source software QuPath.
The primary purpose of this script is to analyze the intensity distribution of detected objects, filter out background noise, perform normalization, and aggregate intensity metrics across multiple datasets. 
This is useful for biological imaging or any other field where quantifying signal intensity from detections (such as cells in microscopy images).
'''

# Specify the directories for detected objects and annotated objects
path_det = "/Users/jmortel/Downloads/detectionsobjects"
path_ano = "/Users/jmortel/Downloads/annotationobjects"
os.chdir(path_det)

# Ensure a directory exists to save generated plots, creating it if necessary
plots_dir = "/Users/jmortel/Downloads/plots"
os.makedirs(plots_dir, exist_ok=True)

# Define a threshold for intensity below which values will be disregarded
custom_intensity_threshold = 0.01  # Set the threshold for filtering out low-intensity values

# Gather a list of all .txt files in the specified directory for processing
filelist = [file for file in os.listdir(path_det) if file.endswith(".txt")]

# Initialize lists for storing calculated metrics across all files
custom_min_value_list = []
lower_25th_percentile_list = []
median_intensity_list = []
upper_75th_percentile_list = []
custom_max_value_list = []
all_unfiltered_intensity = []
background_intensity_list = []

# Process each .txt file individually for analysis
for f in filelist:
    # Initialize dataframes for holding file data
    Read_Data = pd.DataFrame()
    Cell = pd.DataFrame()

    # Load the current file's data into a DataFrame
    Read_Data = pd.read_csv(f, sep="\t", header=0)

    # Switch to annotations directory to read corresponding annotation file
    os.chdir(path_ano)
    filename = f.replace(" Detections", "")
    Read_Data_ano = pd.read_csv(filename, sep="\t", header=0)
    # Switch back to detections directory
    os.chdir(path_det)

    # Filter records based on classification as 'Cell' or 'NotCell'
    NotCell = Read_Data[Read_Data["Class"] == "NotCell"]
    Cell = Read_Data[Read_Data["Class"] == "Cell"]

    # Further filter 'Cell' records by intensity threshold
    Cell_filtered = Cell[Cell["DAB: Nucleus: Mean"] >= custom_intensity_threshold]

    # Proceed if filtered dataset is not empty
    if not Cell_filtered.empty:
        # Estimate background by identifying peaks in a histogram of intensities
        hist_values, bin_edges, _ = plt.hist(Cell_filtered["DAB: Nucleus: Mean"], bins=50, color='red', alpha=0.7)

        # Attempt to identify the minimum value between the two highest peaks, if present
        peaks, _ = find_peaks(hist_values, height=0)
        if len(peaks) >= 2:
            peak1_position, peak2_position = bin_edges[peaks[0]], bin_edges[peaks[1]]
            between_peaks_indices = np.where((bin_edges >= peak1_position) & (bin_edges <= peak2_position))
            min_between_peaks = bin_edges[np.argmin(hist_values[between_peaks_indices])]

            # Visualize the histogram and mark the minimum value between peaks
            plt.figure(figsize=(10, 6))
            plt.hist(Cell_filtered["DAB: Nucleus: Mean"], bins=50, color='red', alpha=0.7)
            plt.axvline(x=min_between_peaks, color='blue', linestyle='dashed', linewidth=2, label='Min Between Peaks')
            plt.title("Histogram of Filtered Intensity Data")
            plt.xlabel("Intensity")
            plt.ylabel("Frequency")
            plt.legend()
            plt.savefig(os.path.join(plots_dir, f"histogram_with_min_between_peaks_{f}.png"))
            plt.close()

            print(f"Identified minimum value between peaks for {f}: {min_between_peaks}")

        # Normalize intensity values using file-specific min and max
        custom_min_value = np.min(Cell_filtered["DAB: Nucleus: Mean"])
        custom_max_value = np.max(Cell_filtered["DAB: Nucleus: Mean"])
        normalized_values = (Cell_filtered["DAB: Nucleus: Mean"] - custom_min_value) / (custom_max_value - custom_min_value)

        # Calculate and store percentiles from normalized intensities
        Quant_Intensity = normalized_values.quantile([0.25, 0.5, 0.75])
        custom_min_value_list.append(custom_min_value)
        lower_25th_percentile_list.append(custom_min_value + Quant_Intensity[0.25] * (custom_max_value - custom_min_value))
        median_intensity_list.append(custom_min_value + Quant_Intensity[0.5] * (custom_max_value - custom_min_value))
        upper_75th_percentile_list.append(custom_min_value + Quant_Intensity[0.75] * (custom_max_value - custom_min_value))
        custom_max_value_list.append(custom_max_value)
        all_unfiltered_intensity.extend(Cell["DAB: Nucleus: Mean"].values)

# Compute and report overall metrics from aggregated data
overall_means = {
    "Metric": ["Custom Min Value", "Lower 25th Percentile Intensity", "50th Percentile Intensity", "Upper 75th Percentile Intensity", "Custom Max Value"],
    "Overall Value": [
        sum(custom_min_value_list) / len(custom_min_value_list),
        sum(lower_25th_percentile_list) / len(lower_25th_percentile_list),
        sum(median_intensity_list) / len(median_intensity_list),
        sum(upper_75th_percentile_list) / len(upper_75th_percentile_list),
        sum(custom_max_value_list) / len(custom_max_value_list)
    ]
}

# Compile overall metrics into a DataFrame and save to CSV
pd.DataFrame(overall_means).to_csv("Overall_Values_minmedmax_normalized_custommax.csv", index=False)
