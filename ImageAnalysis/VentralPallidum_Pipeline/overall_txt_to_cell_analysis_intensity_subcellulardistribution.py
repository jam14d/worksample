import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Specify directories
# Uncomment the desired input type:
# For CSV files:
# input_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4 - OPRM1TRAINING_WITHCOMPOSITES/detections_withMu_12.6.24_csv"

# For text files:
input_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4/detections_iteration4_withMu_12.23.24"

overall_plots_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4 - OPRM1TRAINING_WITHCOMPOSITES/output_cluster_intensity_overall_plots"
overall_data_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4 - OPRM1TRAINING_WITHCOMPOSITES/output_cluster_intensity_overall_data"
os.makedirs(overall_plots_directory, exist_ok=True)
os.makedirs(overall_data_directory, exist_ok=True)

# Define classifications
classifications = [
    "vglut2_Pos: vgat_Neg",
    "vglut2_Neg: vgat_Pos",
    "vglut2_Pos: vgat_Pos",
    "vglut2_Neg: vgat_Neg"
]
metric_column = "AF568: Cell: Mean"

# Initialize a list to store overall data for all classifications
overall_distribution_data = []

# Read all files and combine data
for file in os.listdir(input_directory):
    if file.endswith(".csv") or file.endswith(".txt"):
        try:
            # Load file and normalize headers
            file_path = os.path.join(input_directory, file)
            
            # Check the file extension to decide parsing logic
            if file.endswith(".csv"):
                df = pd.read_csv(file_path, encoding="utf-8")
            elif file.endswith(".txt"):
                df = pd.read_csv(file_path, delimiter="\t", encoding="utf-8")
            
            df.columns = df.columns.str.strip()  # Normalize column names

            if "Classification" not in df.columns or metric_column not in df.columns:
                print(f"Skipping file {file}: Missing required columns.")
                continue

            df["Classification"] = df["Classification"].str.strip()  # Normalize Classification values

            # Append relevant data to the overall dataset
            for cls in classifications:
                Classification_data = df[df["Classification"] == cls][metric_column].dropna()
                overall_distribution_data.extend([(cls, spots) for spots in Classification_data])

        except Exception as e:
            print(f"Error processing file {file}: {e}")

# Convert overall data to DataFrame
overall_df = pd.DataFrame(overall_distribution_data, columns=["Cell Type", "AF568: Cell: Mean"])

## DEBUG
print(overall_df.head())
print(overall_df["AF568: Cell: Mean"].dtype)


# Calculate overall descriptive statistics
overall_statistics_data = []
for cls in classifications:
    cls_data = overall_df[overall_df["Cell Type"] == cls]["AF568: Cell: Mean"]
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
        plt.title(f"Overall Distribution of OPRM1 Cluster Intensity Per Cell\n{cls}", fontsize=10)
        plt.xlabel("OPRM1 Cluster Intensity Per Cell")
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
        plt.title(f"CDF of OPRM1 Cluster Intensity Per Cell\n{cls}", fontsize=10)
        plt.xlabel("OPRM1 Cluster Intensity Per Cell")
        plt.ylabel("CDF")
        plt.tight_layout()

        cdf_path = os.path.join(overall_plots_directory, f"Overall_{cls.replace(': ', '_').replace(' ', '_')}CDF.png")
        plt.savefig(cdf_path)
        plt.close()

# Save overall descriptive statistics to CSV
overall_statistics_df = pd.DataFrame(overall_statistics_data)
overall_statistics_output_path = os.path.join(overall_data_directory, "oprm1intensity_cluster_overall_descriptive_statistics.csv")
overall_statistics_df.to_csv(overall_statistics_output_path, index=False)
print(f"Intensity overall descriptive statistics saved to {overall_statistics_output_path}.")
