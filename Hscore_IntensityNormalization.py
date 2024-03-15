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

# Path to data
path_det = "/Users/jamieannemortel/Downloads/detectionobjects"
path_ano = "/Users/jamieannemortel/Downloads/annotationobjects"
os.chdir(path_det)

# Directory creation for saving plots (optional)
plots_dir = "/Users/jamieannemortel/Downloads/plots"
os.makedirs(plots_dir, exist_ok=True)

# Set the custom intensity value to ignore values below
custom_intensity_threshold = 0.01  # Add your custom intensity value here (useful for omitting high background)

# Tells it to look for all .txt files in the path given above
filelist = [file for file in os.listdir(path_det) if file.endswith(".txt")]

# Create empty lists to store data for each metric
custom_min_value_list = []
lower_25th_percentile_list = []
median_intensity_list = []
upper_75th_percentile_list = []
custom_max_value_list = []
all_unfiltered_intensity = []
background_intensity_list = []

# For every file ending in .txt in that path, we will run through this loop of calculations once.
for f in filelist:
    # Declare some tables for data
    Read_Data = pd.DataFrame()
    Cell = pd.DataFrame()

    # This line reads the .txt file and places it into a table we can look at
    Read_Data = pd.read_csv(f, sep="\t", header=0)

    #os.chdir(path_ano)
    #filename = f.replace("Detections", "")
    #Read_Data_ano = pd.read_csv(filename, sep="\t", header=0)
    #os.chdir(path_det)

    # Basic calculations from the data, NotCells are all the things that are given the Class NotCell in the data etc, can be changed to be whatever
    NotCell = Read_Data[Read_Data["Classification"] == "NotCell"]
    Cell = Read_Data[Read_Data["Classification"] == "Cell"]

    # Exclude values below the custom intensity threshold
    Cell_filtered = Cell[Cell["DAB: Nucleus: Mean"] >= custom_intensity_threshold]

    # Check if there are any valid values after filtering
    if not Cell_filtered.empty:
        # Finding peaks in the histogram (background estimation)
        hist_values, bin_edges, _ = plt.hist(Cell_filtered["DAB: Nucleus: Mean"], bins=50, range=(min(Cell_filtered["DAB: Nucleus: Mean"]), max(Cell_filtered["DAB: Nucleus: Mean"])), color='red', alpha=0.7)

        # If there are at least two peaks, find the minimum between them
        peaks, _ = find_peaks(hist_values, height=0)
        if len(peaks) >= 2:
            # Get the positions of the two highest peaks
            peak1_position = bin_edges[peaks[0]]
            peak2_position = bin_edges[peaks[1]]

            # Find the indices corresponding to the region between the peaks
            between_peaks_indices = np.where((bin_edges >= peak1_position) & (bin_edges <= peak2_position))

            # Find the minimum value in the region between the peaks
            min_between_peaks = bin_edges[np.argmin(hist_values[between_peaks_indices])]

            # Plotting the histogram with the minimum value between peaks marked
            plt.figure(figsize=(10, 6))
            plt.hist(Cell_filtered["DAB: Nucleus: Mean"], bins=50, range=(min(Cell_filtered["DAB: Nucleus: Mean"]), max(Cell_filtered["DAB: Nucleus: Mean"])), color='red', alpha=0.7)
            plt.axvline(x=min_between_peaks, color='blue', linestyle='dashed', linewidth=2, label='Min Between Peaks')
            plt.title("Histogram of Entire Unfiltered Intensity Dataset")
            plt.xlabel("Intensity")
            plt.ylabel("Frequency")
            plt.legend()
            plt.savefig(os.path.join(plots_dir, f"histogram_with_min_between_peaks_{f}.png"))
            plt.close()

            print(f"Minimum value between peaks for {f}: {min_between_peaks}")

        # Normalization step using custom min and max values for each file
        custom_min_value = np.min(Cell_filtered["DAB: Nucleus: Mean"])
        custom_max_value = np.max(Cell_filtered["DAB: Nucleus: Mean"])
        normalized_values = (Cell_filtered["DAB: Nucleus: Mean"] - custom_min_value) / (custom_max_value - custom_min_value)

        Quant_Intensity = normalized_values.quantile([0.25, 0.5, 0.75])

        # Append data for each file to the lists
        custom_min_value_list.append(custom_min_value)
        lower_25th_percentile_list.append(custom_min_value + Quant_Intensity[0.25] * (custom_max_value - custom_min_value))
        median_intensity_list.append(custom_min_value + Quant_Intensity[0.5] * (custom_max_value - custom_min_value))
        upper_75th_percentile_list.append(custom_min_value + Quant_Intensity[0.75] * (custom_max_value - custom_min_value))
        custom_max_value_list.append(custom_max_value)
        all_unfiltered_intensity.extend(Cell["DAB: Nucleus: Mean"].values)

# Calculate overall mean values across all files
overall_mean_custom_min_value = sum(custom_min_value_list) / len(custom_min_value_list)
overall_mean_lower_25th_percentile = sum(lower_25th_percentile_list) / len(lower_25th_percentile_list)
overall_mean_median_intensity = sum(median_intensity_list) / len(median_intensity_list)
overall_mean_upper_75th_percentile = sum(upper_75th_percentile_list) / len(upper_75th_percentile_list)
overall_mean_custom_max_value = sum(custom_max_value_list) / len(custom_max_value_list)

# Create a DataFrame with the overall values
overall_values = pd.DataFrame({
    "Metric": ["Custom Min Value", "Lower 25th Percentile Intensity", "50th Percentile Intensity", "Upper 75th Percentile Intensity", "Custom Max Value"],
    "Overall Value": [overall_mean_custom_min_value, overall_mean_lower_25th_percentile, overall_mean_median_intensity, overall_mean_upper_75th_percentile, overall_mean_custom_max_value]
})

# Writes a csv file with the overall values in the path
overall_values.to_csv("Overall_Values_minmedmax_normalized_custommax.csv", index=False)
