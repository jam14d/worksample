import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Required for cumulative calculations

# Specify directories
input_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4 - OPRM1TRAINING_WITHCOMPOSITES/detections_withMu_12.6.24_csv"
output_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4 - OPRM1TRAINING_WITHCOMPOSITES/output_data_12.23.24"
plots_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4 - OPRM1TRAINING_WITHCOMPOSITES/output_plots_12.23.24"
cdf_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4 - OPRM1TRAINING_WITHCOMPOSITES/output_cdf_12.23.24"
os.makedirs(output_directory, exist_ok=True)
os.makedirs(plots_directory, exist_ok=True)
os.makedirs(cdf_directory, exist_ok=True)

# Define classifications
classifications = [
    "Cell (vglut2_Pos: vgat_Neg)",
    "Cell (vglut2_Neg: vgat_Pos)",
    "Cell (vglut2_Pos: vgat_Pos)",
    "Cell (vglut2_Neg: vgat_Neg)"
]
metric_column = "Num spots"

# Initialize a list to store distribution data for all images
distribution_data = []

# Read CSV files and process data
for file in os.listdir(input_directory):
    if file.endswith(".csv"):
        try:
            # Load file and normalize headers
            file_path = os.path.join(input_directory, file)
            df = pd.read_csv(file_path, encoding="utf-8")
            df.columns = df.columns.str.strip()  # Normalize column names

            # Debug: Check columns and unique values
            print(f"Processing {file}...")
            if "Parent" not in df.columns or metric_column not in df.columns:
                print(f"Skipping file {file}: Missing required columns.")
                continue

            df["Parent"] = df["Parent"].str.strip()  # Normalize Parent values

            # Process distribution for each classification
            for cls in classifications:
                parent_data = df[df["Parent"] == cls]
                print(f"{file} - {cls}: {len(parent_data)} rows found.")

                if not parent_data.empty:
                    # Extract number of spots per cell
                    spots_per_cell = parent_data[metric_column].dropna().tolist()

                    # Record data for this classification and image
                    for spots in spots_per_cell:
                        distribution_data.append({
                            "Image": file,
                            "Cell Type": cls,
                            "Num Spots Per Cell": spots
                        })

                    # Generate and save CDF plot for this cell type
                    sorted_data = np.sort(spots_per_cell)
                    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)

                    plt.figure()
                    plt.plot(sorted_data, cdf, marker="o", linestyle="--", color="blue")
                    plt.title(f"CDF of Spots Per Cell\n{cls} ({file})", fontsize=10)
                    plt.xlabel("Number of Spots Per Cell")
                    plt.ylabel("CDF")
                    plt.xlim(0, 20)  # Adjust as needed
                    plt.tight_layout()

                    # Save the CDF plot
                    cdf_plot_path = os.path.join(
                        cdf_directory,
                        f"{file.replace('.csv', '')}_{cls.replace(': ', '_').replace(' ', '_')}_Num_Spots_CDF.png"
                    )
                    plt.savefig(cdf_plot_path)
                    plt.close()

                    # Generate and save histogram for this cell type
                    plt.figure()
                    plt.hist(spots_per_cell, bins=20, color="green", alpha=0.7, edgecolor="black")
                    plt.title(f"Histogram of Spots Per Cell\n{cls} ({file})", fontsize=10)
                    plt.xlabel("Number of Spots Per Cell")
                    plt.ylabel("Frequency")
                    plt.xlim(0, 20)  # Adjust as needed
                    plt.tight_layout()

                    # Save the histogram plot
                    histogram_plot_path = os.path.join(
                        plots_directory,
                        f"{file.replace('.csv', '')}_{cls.replace(': ', '_').replace(' ', '_')}_Num_Spots_Histogram.png"
                    )
                    plt.savefig(histogram_plot_path)
                    plt.close()

        except UnicodeDecodeError:
            print(f"Encoding error with file {file}. Skipping.")
        except Exception as e:
            print(f"Error processing {file}: {e}")

# Convert distribution data to DataFrame
distribution_df = pd.DataFrame(distribution_data)

# Save the distribution data to CSV
output_path = os.path.join(output_directory, "spots_per_cell_per_image.csv")
distribution_df.to_csv(output_path, index=False)
print(f"Distribution data saved to {output_path}.")
