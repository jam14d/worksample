import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Specify directories
input_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4 - OPRM1TRAINING_WITHCOMPOSITES/detections_withMu_12.6.24_csv"
overall_plots_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4 - OPRM1TRAINING_WITHCOMPOSITES/output_overall_plots"
overall_data_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4 - OPRM1TRAINING_WITHCOMPOSITES/output_overall_data"
os.makedirs(overall_plots_directory, exist_ok=True)
os.makedirs(overall_data_directory, exist_ok=True)

# Define classifications
classifications = [
    "Cell (vglut2_Pos: vgat_Neg)",
    "Cell (vglut2_Neg: vgat_Pos)",
    "Cell (vglut2_Pos: vgat_Pos)",
    "Cell (vglut2_Neg: vgat_Neg)"
]
metric_column = "Num spots"

# Initialize a list to store overall data for all classifications
overall_distribution_data = []

# Read all CSV files and combine data
for file in os.listdir(input_directory):
    if file.endswith(".csv"):
        try:
            # Load file and normalize headers
            file_path = os.path.join(input_directory, file)
            df = pd.read_csv(file_path, encoding="utf-8")
            df.columns = df.columns.str.strip()  # Normalize column names

            if "Parent" not in df.columns or metric_column not in df.columns:
                print(f"Skipping file {file}: Missing required columns.")
                continue

            df["Parent"] = df["Parent"].str.strip()  # Normalize Parent values

            # Append relevant data to the overall dataset
            for cls in classifications:
                parent_data = df[df["Parent"] == cls][metric_column].dropna()
                overall_distribution_data.extend([(cls, spots) for spots in parent_data])

        except Exception as e:
            print(f"Error processing file {file}: {e}")

# Convert overall data to DataFrame
overall_df = pd.DataFrame(overall_distribution_data, columns=["Cell Type", "Num Spots"])

# Calculate overall descriptive statistics
overall_statistics_data = []
for cls in classifications:
    cls_data = overall_df[overall_df["Cell Type"] == cls]["Num Spots"]
    if not cls_data.empty:
        overall_statistics = {
            "Cell Type": cls,
            "Min": cls_data.min(),
            "Max": cls_data.max(),
            "Mean": cls_data.mean(),
            "25th Percentile": np.percentile(cls_data, 25),
            "Median": cls_data.median(),
            "75th Percentile": np.percentile(cls_data, 75),
            "Standard Deviation": cls_data.std(),
            "Variance": cls_data.var()
        }
        overall_statistics_data.append(overall_statistics)

        # Generate and save histogram for this cell type
        plt.figure()
        cls_data.hist(bins=20, edgecolor="black", alpha=0.7)
        plt.title(f"Overall Distribution of Spots Per Cell\n{cls}", fontsize=10)
        plt.xlabel("Number of Spots Per Cell")
        plt.ylabel("Frequency")
        plt.tight_layout()

        histogram_path = os.path.join(overall_plots_directory, f"Overall_{cls.replace(': ', '_').replace(' ', '_')}_Histogram.png")
        plt.savefig(histogram_path)
        plt.close()

        # Generate and save CDF plot for this cell type
        sorted_data = np.sort(cls_data)
        cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

        plt.figure()
        plt.plot(sorted_data, cdf, marker="o", linestyle="--", color="blue")
        plt.title(f"CDF of Spots Per Cell\n{cls}", fontsize=10)
        plt.xlabel("Number of Spots Per Cell")
        plt.ylabel("CDF")
        plt.tight_layout()

        cdf_path = os.path.join(overall_plots_directory, f"Overall_{cls.replace(': ', '_').replace(' ', '_')}_CDF.png")
        plt.savefig(cdf_path)
        plt.close()

# Save overall descriptive statistics to CSV
overall_statistics_df = pd.DataFrame(overall_statistics_data)
overall_statistics_output_path = os.path.join(overall_data_directory, "overall_descriptive_statistics.csv")
overall_statistics_df.to_csv(overall_statistics_output_path, index=False)
print(f"Overall descriptive statistics saved to {overall_statistics_output_path}.")
