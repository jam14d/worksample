import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define paths
paths = {
    "raw_detection": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - vglut2_OPRM1_COMPOSITE/detections_iteration4_vglut2withMu_12.13.24"
}

# Create directory for plots
plots_dir = os.path.join(os.path.dirname(paths["raw_detection"]), "punctacount_plots")
os.makedirs(plots_dir, exist_ok=True)

# List files in the detection directory
filelist = [f for f in os.listdir(paths["raw_detection"]) if f.endswith(".txt") and not f.startswith("._")]

# Define corrected Parents and colors
classifications = {
    "vglut2_positive_oprm1_negative": ["Cell (vglut2_Pos: oprm1_Neg)"],
    "vglut2_positive_oprm1_positive": ["Cell (vglut2_Pos: oprm1_Pos)"]
}
colors = {
    "vglut2_positive_oprm1_negative": "blue",
    "vglut2_positive_oprm1_positive": "orange"
}

# Initialize data dictionary
subcellular_data = {key: [] for key in classifications.keys()}

# Process files
for file in filelist:
    try:
        print(f"\nProcessing file: {file}")

        # Attempt to read the file
        det_data = pd.read_csv(os.path.join(paths["raw_detection"], file), sep="\t", encoding="utf-8")

        # Print column names
        print(f"Columns in {file}: {list(det_data.columns)}")
        
        # Debugging: Print unique classifications
        unique_classifications = det_data["Parent"].unique()
        print(f"Unique classifications in {file}: {unique_classifications}")

        for cell_type, labels in classifications.items():
            print(f"\nFiltering for {cell_type} using labels: {labels}")

            # Filter rows by classification
            filtered_data = det_data[det_data["Parent"].isin(labels)]
            
            # Debugging: Show filtered rows
            print(f"Filtered rows for {cell_type}:\n{filtered_data[['Parent', 'Num spots']].head()}")

            if "Num spots" in filtered_data.columns:
                extracted_values = filtered_data["Num spots"].dropna().tolist()
            else:
                print(f"'Num spots' column not found in {file}")
                extracted_values = []

            print(f"Extracted values for {cell_type} from {file}: {extracted_values}")
            subcellular_data[cell_type].extend(extracted_values)
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Generate plots
for cell_type, values in subcellular_data.items():
    if values:
        values = np.array(values)

        # Debugging: Print summary statistics
        print(f"\nSummary for {cell_type}:")
        print(f"  Count: {len(values)}")
        print(f"  Min: {np.min(values)}")
        print(f"  Max: {np.max(values)}")
        print(f"  Mean: {np.mean(values)}")

        # Histogram
        plt.figure(figsize=(10, 6))
        plt.hist(values, bins=30, color=colors[cell_type], edgecolor="black", alpha=0.7)
        plt.title(f"Distribution of Puncta Counts for {cell_type.replace('_', ' ').title()}")
        plt.xlabel("Num Spots")
        plt.xlim(0, 30)  # Set x-axis limits
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.savefig(os.path.join(plots_dir, f"{cell_type}_histogram.png"))
        plt.close()

        # CDF
        sorted_data = np.sort(values)
        cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

        plt.figure(figsize=(10, 6))
        plt.plot(sorted_data, cdf, color=colors[cell_type])
        plt.title(f"CDF for {cell_type.replace('_', ' ').title()}")
        plt.xlabel("Num Spots")
        plt.xlim(0, 30)  # Set x-axis limits
        plt.ylabel("Cumulative Probability")
        plt.grid(True)
        plt.savefig(os.path.join(plots_dir, f"{cell_type}_cdf.png"))
        plt.close()

        print(f"Plots for {cell_type} saved.")
    else:
        print(f"No data for {cell_type}.")