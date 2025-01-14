import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu

# Define paths for VGAT and VGLUT2 data
paths = {
    "vgat_positive_oprm1_positive": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGAT_OPRM1_COMPOSITE/detections_iteration4_vgatwithMu_12.13.24",
    "vglut2_positive_oprm1_positive": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGLUT2_OPRM1_COMPOSITE/detections_iteration4_vglut2withMu_12.13.24",
}

# Create a "plots" directory
script_dir = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(script_dir, "oprm1VGATvsVGLUT2_plots")
os.makedirs(plots_dir, exist_ok=True)

# Define classifications and parent values
classifications = {
    "vgat_positive_oprm1_positive": ["vgat_Pos: oprm1_Pos"],
    "vglut2_positive_oprm1_positive": ["vglut2_Pos: oprm1_Pos"],
}
parent_values = {
    "vgat_positive_oprm1_positive": "Cell (vgat_Pos: oprm1_Pos)",
    "vglut2_positive_oprm1_positive": "Cell (vglut2_Pos: oprm1_Pos)",
}

# Initialize a dictionary to collect data for each classification
data = {key: pd.DataFrame() for key in classifications.keys()}

# Helper function to read data
def read_data(file_path):
    try:
        return pd.read_csv(file_path, sep="\t", encoding="utf-8")
    except UnicodeDecodeError:
        print(f"Error reading file {file_path}: Unable to decode.")
        return None

# Collect intensity data
def collect_intensity_data(raw_detection_path, labels):
    filelist = [f for f in os.listdir(raw_detection_path) if f.endswith(".txt")]

    intensity_data = []
    for file in filelist:
        file_path = os.path.join(raw_detection_path, file)
        det_data = read_data(file_path)
        if det_data is None or "Classification" not in det_data.columns or "AF568: Cell: Mean" not in det_data.columns:
            print(f"Skipping file {file}: Required columns for intensity are missing.")
            continue

        filtered_data = det_data[det_data["Classification"].isin(labels)]
        intensity_data.append(filtered_data[["AF568: Cell: Mean"]].dropna())

    if intensity_data:
        return pd.concat(intensity_data, ignore_index=True)
    else:
        return pd.DataFrame(columns=["AF568: Cell: Mean"])

# Collect puncta data
def collect_puncta_data(raw_detection_path, parent_value):
    filelist = [f for f in os.listdir(raw_detection_path) if f.endswith(".txt")]

    puncta_data = []
    for file in filelist:
        file_path = os.path.join(raw_detection_path, file)
        det_data = read_data(file_path)
        if det_data is None or "Parent" not in det_data.columns or "Num spots" not in det_data.columns:
            print(f"Skipping file {file}: Required columns for puncta are missing.")
            continue

        filtered_data = det_data[det_data["Parent"] == parent_value]
        puncta_data.append(filtered_data[["Num spots"]].dropna())

    if puncta_data:
        return pd.concat(puncta_data, ignore_index=True)
    else:
        return pd.DataFrame(columns=["Num spots"])

# Collect data for each classification
for key in classifications.keys():
    raw_detection_path = paths[key]
    intensity_df = collect_intensity_data(raw_detection_path, classifications[key])
    puncta_df = collect_puncta_data(raw_detection_path, parent_values[key])

    if not intensity_df.empty and not puncta_df.empty:
        merged_data = pd.concat([intensity_df, puncta_df], axis=1)
        data[key] = merged_data.dropna()
    else:
        print(f"No data for classification: {key}")

# File to save statistics
stats_file_path = os.path.join(plots_dir, "vgat_vs_vglut2_stats.txt")
with open(stats_file_path, "w") as stats_file:
    stats_file.write("VGAT vs VGLUT2 Statistical Comparison\n")
    stats_file.write("=" * 50 + "\n\n")

    # Compare VGAT vs VGLUT2 for intensity
    vgat_intensity = data["vgat_positive_oprm1_positive"]["AF568: Cell: Mean"]
    vglut2_intensity = data["vglut2_positive_oprm1_positive"]["AF568: Cell: Mean"]
    
    if not vgat_intensity.empty and not vglut2_intensity.empty:
        intensity_stats = mannwhitneyu(vgat_intensity, vglut2_intensity, alternative="two-sided")
        stats_file.write(f"Intensity Comparison:\n")
        stats_file.write(f"  U-statistic: {intensity_stats.statistic}, p-value: {intensity_stats.pvalue}\n\n")

    # Compare VGAT vs VGLUT2 for puncta
    vgat_puncta = data["vgat_positive_oprm1_positive"]["Num spots"]
    vglut2_puncta = data["vglut2_positive_oprm1_positive"]["Num spots"]

    if not vgat_puncta.empty and not vglut2_puncta.empty:
        puncta_stats = mannwhitneyu(vgat_puncta, vglut2_puncta, alternative="two-sided")
        stats_file.write(f"Puncta Comparison:\n")
        stats_file.write(f"  U-statistic: {puncta_stats.statistic}, p-value: {puncta_stats.pvalue}\n\n")

    # Write subpopulation statistics for each classification
    for key, df in data.items():
        if not df.empty:
            stats_file.write(f"Statistics for {key.replace('_', ' ').title()}\n")
            stats_file.write(f"Total Cells: {len(df)}\n")

            df["Subpopulation"] = pd.cut(
                df["AF568: Cell: Mean"],
                bins=[-float("inf"), 150, float("inf")],
                labels=["Low Intensity", "High Intensity"]
            ).astype(str) + " | " + pd.cut(
                df["Num spots"],
                bins=[-float("inf"), 2, float("inf")],
                labels=["Low Puncta", "High Puncta"]
            ).astype(str)

            subpop_counts = df["Subpopulation"].value_counts()
            for subpop, count in subpop_counts.items():
                stats_file.write(f"  {subpop}: {count}\n")

            stats_file.write("\n")

# Visualization
subpop_comparison = []
for cell_type, df in data.items():
    if not df.empty:
        subpop_comparison.extend([
            {"Cell Type": cell_type.replace("_", " ").title(), "Intensity": row["AF568: Cell: Mean"], "Puncta": row["Num spots"]}
            for _, row in df.iterrows()
        ])

if subpop_comparison:
    subpop_comparison_df = pd.DataFrame(subpop_comparison)

    # Scatter plots
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=subpop_comparison_df,
        x="Puncta",
        y="Intensity",
        hue="Cell Type",
        palette="Set2",
        alpha=0.7
    )
    plt.title("Puncta vs Intensity: VGAT vs VGLUT2", fontsize=14)
    plt.xlabel("Puncta Count")
    plt.ylabel("Intensity")
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "VGAT_vs_VGLUT2_Scatter.png"))
    plt.close()
