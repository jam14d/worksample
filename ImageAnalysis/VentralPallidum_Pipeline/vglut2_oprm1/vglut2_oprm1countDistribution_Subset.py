import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#INPROGRESS

# Path to data
path_det = "/Users/jamieannemortel/Downloads/RawData_VGLUT2/detection results"
os.chdir(path_det)

# Directory for saving plots
plots_dir = "/Users/jamieannemortel/Downloads/RawData_VGLUT2/plots"
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

    # Clean column names to remove any leading or trailing spaces
    Read_Data.columns = Read_Data.columns.str.strip()

    # Print columns to confirm
    print(f"Processing file: {f}")
    print("Columns available:", Read_Data.columns)

    # Subset the data for vglut2_Pos only, or treat it as zero if not found
    Pink_posName = "vglut2_Pos"
    Pink_posName_2 = "vglut2_Pos: vgat_Neg"

    if Pink_posName in Read_Data['Name'].values or Pink_posName_2 in Read_Data['Name'].values:
        Cell = Read_Data[Read_Data['Name'].isin([Pink_posName, Pink_posName_2])]
    else:
        print(f"No {Pink_posName} or {Pink_posName_2} found in {f}. Treating as zero intensity data.")
        # If the `vglut2_Pos` group is not found, we can assume zero values for the analysis
        Cell = Read_Data.copy()  # Keep the original data, but no relevant 'Pink_posName' entries

    # Exclude values below the custom intensity threshold for 'AF568: Cell: Mean'
    if "AF568: Cell: Mean" in Read_Data.columns:
        Cell_filtered = Cell[Cell["AF568: Cell: Mean"] >= custom_intensity_threshold]
    else:
        print("Column 'AF568: Cell: Mean' not found in the data!")

    # Check if there are any valid values after filtering
    if not Cell_filtered.empty:
        # Plot histogram of the filtered data
        plt.figure(figsize=(10, 6))
        plt.hist(Cell_filtered["AF568: Cell: Mean"], bins=50, range=(min(Cell_filtered["AF568: Cell: Mean"]), max(Cell_filtered["AF568: Cell: Mean"])), color='red', alpha=0.7)
        plt.title(f"Histogram of oprm1 spot count for {Pink_posName}")
        plt.xlabel("Intensity")
        plt.ylabel("Frequency")
        plt.savefig(os.path.join(plots_dir, f"histogram_{Pink_posName}_{f}.png"))
        plt.close()

        # Normalization step using custom min and max values for each file
        custom_min_value = np.min(Cell_filtered["AF568: Cell: Mean"])
        custom_max_value = np.max(Cell_filtered["AF568: Cell: Mean"])
        normalized_values = (Cell_filtered["AF568: Cell: Mean"] - custom_min_value) / (custom_max_value - custom_min_value)

        Quant_Intensity = normalized_values.quantile([0.25, 0.5, 0.75])

        # Append data for each file to the lists
        custom_min_value_list.append(custom_min_value)
        lower_25th_percentile_list.append(custom_min_value + Quant_Intensity[0.25] * (custom_max_value - custom_min_value))
        median_intensity_list.append(custom_min_value + Quant_Intensity[0.5] * (custom_max_value - custom_min_value))
        upper_75th_percentile_list.append(custom_min_value + Quant_Intensity[0.75] * (custom_max_value - custom_min_value))
        custom_max_value_list.append(custom_max_value)
        all_unfiltered_intensity.extend(Cell["AF568: Cell: Mean"].values)
    else:
        print(f"No valid data found for {Pink_posName} in {f}")

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
        "Metric": ["Min Value", "Lower 25th Percentile Intensity", "50th Percentile Intensity", "Upper 75th Percentile Intensity", "Max Value"],
        "Overall Value": [overall_mean_custom_min_value, overall_mean_lower_25th_percentile, overall_mean_median_intensity, overall_mean_upper_75th_percentile, overall_mean_custom_max_value]
    })

    # Writes a csv file with the overall values in the path
    overall_values.to_csv(os.path.join(plots_dir, "Overall_Values_minmedmax_normalized_custommax.csv"), index=False)
else:
    print("No valid data was found for processing.")
