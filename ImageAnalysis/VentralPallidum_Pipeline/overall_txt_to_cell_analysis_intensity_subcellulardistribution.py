import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Specify directories
input_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4/detections_iteration4_withMu_12.23.24"
overall_plots_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4/SCALEDoutputintensity_overall_plots"
overall_data_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4/SCALEDoutputintensity_overall_data"
#boxplot_directory = os.path.join(overall_plots_directory, "boxplots")
os.makedirs(overall_plots_directory, exist_ok=True)
os.makedirs(overall_data_directory, exist_ok=True)
#os.makedirs(boxplot_directory, exist_ok=True)

# Define classifications
classifications = [
    "vglut2_Pos: vgat_Neg",
    "vglut2_Neg: vgat_Pos",
    "vglut2_Pos: vgat_Pos",
    "vglut2_Neg: vgat_Neg"
]

# Define colors for classifications
colors = {
    "vglut2_Pos: vgat_Neg": "red",
    "vglut2_Neg: vgat_Pos": "blue",
    "vglut2_Pos: vgat_Pos": "purple",
    "vglut2_Neg: vgat_Neg": "black"
}

metric_column = "AF568: Cell: Mean"

# Initialize a list to store overall data for all classifications
overall_distribution_data = []

# Read all files and combine data
for file in os.listdir(input_directory):
    if file.endswith(".csv") or file.endswith(".txt"):
        try:
            # Load file and normalize headers
            file_path = os.path.join(input_directory, file)

            if file.endswith(".csv"):
                df = pd.read_csv(file_path, encoding="utf-8")
            elif file.endswith(".txt"):
                df = pd.read_csv(file_path, delimiter="\t", encoding="utf-8")

            df.columns = df.columns.str.strip()

            if "Classification" not in df.columns or metric_column not in df.columns:
                print(f"Skipping file {file}: Missing required columns.")
                continue

            df["Classification"] = df["Classification"].str.strip()

            # Append relevant data to the overall dataset
            for cls in classifications:
                Classification_data = df[df["Classification"] == cls][metric_column].dropna()
                overall_distribution_data.extend([(cls, spots) for spots in Classification_data])

        except Exception as e:
            print(f"Error processing file {file}: {e}")

# Convert overall data to DataFrame
overall_df = pd.DataFrame(overall_distribution_data, columns=["Cell Type", "AF568: Cell: Mean"])

# Calculate global min and max for x-axis
x_min = overall_df["AF568: Cell: Mean"].min()
x_max = overall_df["AF568: Cell: Mean"].max()

# Calculate global max for y-axis
y_max = 0
for cls in classifications:
    cls_data = overall_df[overall_df["Cell Type"] == cls]["AF568: Cell: Mean"]
    if not cls_data.empty:
        y_max = max(y_max, np.histogram(cls_data, bins=20, range=(x_min, x_max))[0].max())

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
        cls_data.hist(bins=20, edgecolor="black", alpha=0.7, color=colors[cls], range=(x_min, x_max))
        plt.title(f"Distribution of OPRM1 Intensity For Cell Type\n{cls}", fontsize=10)
        plt.xlabel("OPRM1 Intensity")
        plt.ylabel("Frequency")
        plt.xlim(x_min, x_max)  # Set consistent x-axis
        plt.ylim(0, y_max)  # Set consistent y-axis
        plt.tight_layout()

        histogram_path = os.path.join(overall_plots_directory, f"Overall_{cls.replace(': ', '_').replace(' ', '_')}_Histogram.png")
        plt.savefig(histogram_path)
        plt.close()

        # Generate and save CDF plot for this cell type
        sorted_data = np.sort(cls_data)
        cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

        plt.figure()
        plt.plot(sorted_data, cdf, marker="o", linestyle="--", color=colors[cls])
        plt.title(f"CDF of OPRM1 Intensity For Cell Type\n{cls}", fontsize=10)
        plt.xlabel("OPRM1 Intensity")
        plt.ylabel("CDF")
        plt.xlim(x_min, x_max)  # Set consistent x-axis
        plt.tight_layout()

        cdf_path = os.path.join(overall_plots_directory, f"Overall_{cls.replace(': ', '_').replace(' ', '_')}CDF.png")
        plt.savefig(cdf_path)
        plt.close()

# Generate and save combined CDF plot for all classifications
plt.figure(figsize=(10, 6))

for cls in classifications:
    cls_data = overall_df[overall_df["Cell Type"] == cls]["AF568: Cell: Mean"]
    if not cls_data.empty:
        sorted_data = np.sort(cls_data)
        cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
        plt.plot(sorted_data, cdf, label=cls, color=colors[cls])  # Add label for legend

plt.title("Overlayed CDF of OPRM1 Intensity Per Cell Type", fontsize=14)
plt.xlabel("OPRM1 Intensity")
plt.ylabel("CDF")
plt.xlim(x_min, x_max)  # Set consistent x-axis
plt.legend(title="Cell Type", loc='upper left')
plt.tight_layout()

# Save the overlayed CDF plot
combined_cdf_path = os.path.join(overall_plots_directory, "Overall_Combined_CDF.png")
plt.savefig(combined_cdf_path)
plt.close()

print(f"Overlayed CDF plot saved to {combined_cdf_path}.")


#overlay histogram
# Generate and save an overlay histogram for all classifications
# Generate and save an overlay histogram for all classifications
plt.figure(figsize=(10, 6))

# Calculate the maximum frequency for consistent y-axis
max_frequency = 0
for cls in classifications:
    cls_data = overall_df[overall_df["Cell Type"] == cls]["AF568: Cell: Mean"]
    if not cls_data.empty:
        frequencies, _ = np.histogram(cls_data, bins=20, range=(x_min, x_max))
        max_frequency = max(max_frequency, frequencies.max())

for cls in classifications:
    cls_data = overall_df[overall_df["Cell Type"] == cls]["AF568: Cell: Mean"]
    if not cls_data.empty:
        plt.hist(
            cls_data,
            bins=20,
            alpha=0.5,  # Transparency for overlay effect
            label=cls,
            color=colors[cls],
            range=(x_min, x_max),
            density=False  # Use absolute frequencies
        )

# plt.title("Overlayed Histogram of OPRM1 Intensity Per Cell Type", fontsize=14)
# plt.xlabel("OPRM1 Intensity")
# plt.ylabel("Frequency")  # Change label to reflect absolute frequency
# plt.legend(title="Cell Type", loc='upper right')
# plt.ylim(0, max_frequency)  # Apply consistent y-axis limit
# plt.tight_layout()

# # Save the overlay histogram plot
# overlay_histogram_path = os.path.join(overall_plots_directory, "Overall_Combined_Histogram_Absolute.png")
# plt.savefig(overlay_histogram_path)
# plt.close()

# print(f"Overlay histogram with absolute frequency saved to {overlay_histogram_path}.")

# Generate and save a box plot for distributions across classifications
plt.figure(figsize=(10, 6))

# Use seaborn's boxplot for distribution representation
sns.boxplot(
    data=overall_df,
    x="Cell Type",
    y="AF568: Cell: Mean",
    palette=colors
)

plt.title("Distribution of OPRM1 Intensity Per Cell Type", fontsize=14)
plt.xlabel("Cell Type")
plt.ylabel("OPRM1 Intensity")
plt.xticks(rotation=45)  # Rotate x-axis labels for readability
plt.tight_layout()

# Save the box plot
box_plot_path = os.path.join(overall_plots_directory, "Overall_Box_Plot.png")
plt.savefig(box_plot_path)
plt.close()

print(f"Box plot saved to {box_plot_path}.")


#scatter plot intensity vs avg frequency

# Generate and save a density heatmap scatter plot for intensity vs frequency
plt.figure(figsize=(12, 8))

# Combine all cell types into a single DataFrame for Seaborn visualization
density_data = []

# Define bins for intensity and calculate frequencies
bins = 50  # More bins for finer granularity
bin_edges = np.linspace(x_min, x_max, bins + 1)

for cls in classifications:
    cls_data = overall_df[overall_df["Cell Type"] == cls]["AF568: Cell: Mean"]
    if not cls_data.empty:
        # Calculate histogram for frequencies
        frequencies, edges = np.histogram(cls_data, bins=bin_edges)
        bin_centers = (edges[:-1] + edges[1:]) / 2  # Bin centers

        # Append data for visualization
        for center, freq in zip(bin_centers, frequencies):
            density_data.append({"Cell Type": cls, "Intensity": center, "Frequency": freq})

# Convert density data into a DataFrame
density_df = pd.DataFrame(density_data)

# Plot density heatmap-style scatter plot
sns.scatterplot(
    data=density_df,
    x="Intensity",
    y="Frequency",
    hue="Cell Type",
    palette=colors,
    style="Cell Type",
    size="Frequency",
    sizes=(10, 200),  # Scale for scatter sizes
    alpha=0.6  # Transparency for overlap
)

plt.title("Density Scatter Plot: Intensity vs Frequency Per Cell Type", fontsize=16)
plt.xlabel("OPRM1 Intensity")
plt.ylabel("Frequency")
plt.xlim(x_min, x_max)
plt.legend(title="Cell Type", loc="upper right", bbox_to_anchor=(1.2, 1))
plt.tight_layout()

# Save the heatmap scatter plot
heatmap_scatter_path = os.path.join(overall_plots_directory, "Density_Scatter_Intensity_vs_Frequency.png")
plt.savefig(heatmap_scatter_path)
plt.close()

print(f"Density scatter plot saved to {heatmap_scatter_path}.")



