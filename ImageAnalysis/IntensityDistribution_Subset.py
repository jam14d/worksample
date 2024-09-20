import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
Uses .txt files containing stardist segmentation measurements, exported from the open-source software QuPath.
The primary purpose of this script is to analyze the intensity distribution of detected objects, filter out background noise, perform normalization, and aggregate intensity metrics across multiple datasets. 
This is useful for biological imaging or any other field where quantifying signal intensity from detections (such as cells in microscopy images).
'''

# Path to data
path_det = "/Users/jamieannemortel/Downloads/Andrew/detections"
os.chdir(path_det)

# Naming stuff
Pink_posName = "DRD1_Pos"
Pink_posName_2 = "DRD1_Pos: A2A_Neg"

# Directory creation for saving plots (optional)
plots_dir = "/Users/jamieannemortel/Downloads/Andrew/plots"
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

# For every file ending in .txt in that path, we will run through this loop of calculations once.
for f in filelist:
    # Declare some tables for data
    Read_Data = pd.DataFrame()

    # This line reads the .txt file and places it into a table we can look at
    Read_Data = pd.read_csv(f, sep="\t", header=0)

    # Subset the data for Pink_posName only
    Cell = Read_Data[Read_Data['Name'].isin([Pink_posName,Pink_posName_2])]


    # Exclude values below the custom intensity threshold
    Cell_filtered = Cell[Cell["Cy5: Mean"] >= custom_intensity_threshold]

    # Check if there are any valid values after filtering
    if not Cell_filtered.empty:
        # Plot histogram of the filtered data
        plt.figure(figsize=(10, 6))
        plt.hist(Cell_filtered["Cy5: Mean"], bins=50, range=(min(Cell_filtered["Cy5: Mean"]), max(Cell_filtered["Cy5: Mean"])), color='red', alpha=0.7)
        plt.title("Histogram of signal intensity in DRD1 Positive cells expressing oprm1")
        plt.xlabel("Intensity")
        plt.ylabel("Frequency")
        plt.savefig(os.path.join(plots_dir, f"histogram_DRD1_Pos_{f}.png"))
        plt.close()

        # Normalization step using custom min and max values for each file
        custom_min_value = np.min(Cell_filtered["Cy5: Mean"])
        custom_max_value = np.max(Cell_filtered["Cy5: Mean"])
        normalized_values = (Cell_filtered["Cy5: Mean"] - custom_min_value) / (custom_max_value - custom_min_value)

        Quant_Intensity = normalized_values.quantile([0.25, 0.5, 0.75])

        # Append data for each file to the lists
        custom_min_value_list.append(custom_min_value)
        lower_25th_percentile_list.append(custom_min_value + Quant_Intensity[0.25] * (custom_max_value - custom_min_value))
        median_intensity_list.append(custom_min_value + Quant_Intensity[0.5] * (custom_max_value - custom_min_value))
        upper_75th_percentile_list.append(custom_min_value + Quant_Intensity[0.75] * (custom_max_value - custom_min_value))
        custom_max_value_list.append(custom_max_value)
        all_unfiltered_intensity.extend(Cell["Cy5: Mean"].values)

# Check if the lists are empty before performing calculations
if custom_min_value_list:
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
else:
    print("No valid data was found for processing.")
