import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define all paths in a single dictionary (Windows-style)
paths = {
    "raw_detection": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGAT_OPRM1_COMPOSITE/detections_iteration4_vgatwithMu_12.13.24",
    "raw_annotation": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGAT_OPRM1_COMPOSITE/annotations_iteration4_vgatwithMu_12.13.24"
}

# Function to convert Windows paths to Unix-like paths if running in a Unix environment
def convert_to_unix_path(win_path):
    if os.name != "nt":
        win_path = win_path.replace("\\", "/")
        if win_path[1:3] == ":/":
            return f"/mnt/{win_path[0].lower()}{win_path[2:]}"
    return win_path

# Convert all paths to Unix-like if necessary
paths = {key: convert_to_unix_path(value) for key, value in paths.items()}

# Create a "plots" directory
plots_dir = os.path.join(os.path.dirname(paths["raw_detection"]), "plots")
os.makedirs(plots_dir, exist_ok=True)

# Get all detection text files
filelist = [f for f in os.listdir(paths["raw_detection"]) if f.endswith(".txt")]

# Define cell type classifications and their colors
classifications = {
    "vgat_positive_oprm1_negative": ["vgat_Pos", "vgat_Pos: oprm1_Neg"],
    "vgat_positive_oprm1_positive": ["vgat_Pos: oprm1_Pos"]
}
colors = {
    "vgat_positive_oprm1_negative": "blue",
    "vgat_positive_oprm1_positive": "green"
}

# Initialize a dictionary to collect intensities by cell type
intensity_data = {key: [] for key in classifications.keys()}

# Process each file to collect intensity data
for file in filelist:
    try:
        det_data = pd.read_csv(os.path.join(paths["raw_detection"], file), sep="\t")
        for cell_type, labels in classifications.items():
            cell_data = det_data[det_data['Classification'].isin(labels)]
            intensity_data[cell_type].extend(cell_data['AF568: Cell: Mean'].dropna())
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Set y-axis maximum for histograms and CDF plots
y_max = 10000

# Calculate global min and max for x-axis
x_min = min([min(values) for values in intensity_data.values() if values])
x_max = max([max(values) for values in intensity_data.values() if values])

# Generate plots for each cell type
for cell_type, values in intensity_data.items():
    if values:
        values = np.array(values)

        # Create a histogram
        plt.figure(figsize=(10, 6))
        plt.hist(values, bins=30, color=colors[cell_type], edgecolor='black', alpha=0.7)
        plt.title(f"Distribution of Oprm1 Intensity for {cell_type.replace('_', ' : ').title()}")
        plt.xlabel("Oprm1 Intensity")
        plt.ylabel("Frequency")
        plt.xlim(x_min, x_max)
        plt.ylim(0, y_max)
        plt.grid(True)
        hist_path = os.path.join(plots_dir, f"Distribution_of_oprm1_intensity_{cell_type}.png")
        plt.savefig(hist_path)
        plt.close()

        # Create a cumulative distribution function (CDF) plot
        sorted_data = np.sort(values)
        cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

        plt.figure(figsize=(10, 6))
        plt.plot(sorted_data, cdf, marker='.', linestyle='none', color=colors[cell_type])
        plt.title(f"CDF of Oprm1 Intensity for {cell_type.replace('_', ' : ').title()}")
        plt.xlabel("Oprm1 Intensity")
        plt.ylabel("Cumulative Probability")
        plt.xlim(x_min, x_max)  # Set consistent x-axis
        plt.grid(True)
        cdf_path = os.path.join(plots_dir, f"Oprm1_intensity_CDF_{cell_type}.png")
        plt.savefig(cdf_path)
        plt.close()

        print(f"Plots for {cell_type.replace('_', ' ').title()} saved to {plots_dir}")
    else:
        print(f"No AF568: Cell: Mean data available for {cell_type.replace('_', ' ').title()}.")
