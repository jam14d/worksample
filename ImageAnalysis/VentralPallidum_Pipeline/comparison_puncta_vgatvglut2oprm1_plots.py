import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu, ks_2samp
from statannotations.Annotator import Annotator

# Define paths for VGAT and VGLUT2 data
paths = {
    "vgat": {
        "raw_detection": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGAT_OPRM1_COMPOSITE/detections_iteration4_vgatwithMu_12.13.24",
    },
    "vglut2": {
        "raw_detection": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGLUT2_OPRM1_COMPOSITE/detections_iteration4_vglut2withMu_12.13.24",
    },
}

# Create a "plots" directory
script_dir = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(script_dir, "oprm1VGATvsVGLUT2_plots_puncta")
os.makedirs(plots_dir, exist_ok=True)

# Define Parent values
cell_types = {
    "vgat_positive_oprm1_positive": "Cell (vgat_Pos: oprm1_Pos)",
    "vglut2_positive_oprm1_positive": "Cell (vglut2_Pos: oprm1_Pos)",
}

# Initialize a dictionary to collect data for each cell type
data = {key: [] for key in cell_types.keys()}

# Function to collect data for each cell type
def collect_data(group, cell_type_key, parent_value):
    raw_detection_path = paths[group]["raw_detection"]
    filelist = [f for f in os.listdir(raw_detection_path) if f.endswith(".txt") and not f.startswith("._")]

    for file in filelist:
        try:
            det_data = pd.read_csv(os.path.join(raw_detection_path, file), sep="\t", encoding="utf-8")

            if "Parent" not in det_data.columns or "Num spots" not in det_data.columns:
                print(f"Skipping file {file}: Required columns are missing.")
                continue

            # Filter rows by Parent column for the specific cell type
            filtered_data = det_data[det_data["Parent"] == parent_value]
            if not filtered_data.empty:
                data[cell_type_key].extend(filtered_data["Num spots"].dropna().tolist())
            else:
                print(f"No matching data in {file} for {parent_value}.")

        except Exception as e:
            print(f"Error processing file {file}: {e}")

# Collect data for each cell type
collect_data("vgat", "vgat_positive_oprm1_positive", cell_types["vgat_positive_oprm1_positive"])
collect_data("vglut2", "vglut2_positive_oprm1_positive", cell_types["vglut2_positive_oprm1_positive"])

# Perform statistical tests
vgat_data = pd.Series(data["vgat_positive_oprm1_positive"])
vglut2_data = pd.Series(data["vglut2_positive_oprm1_positive"])

stat_results = {}
if not vgat_data.empty and not vglut2_data.empty:
    # Mann-Whitney U Test
    u_stat, u_p_value = mannwhitneyu(vgat_data, vglut2_data, alternative='two-sided')
    stat_results["Mann-Whitney"] = (u_stat, u_p_value)

    # Kolmogorov-Smirnov Test
    ks_stat, ks_p_value = ks_2samp(vgat_data, vglut2_data)
    stat_results["Kolmogorov-Smirnov"] = (ks_stat, ks_p_value)

    # Save statistical test results and descriptive stats to a text file
    stats_results_path = os.path.join(plots_dir, "statistical_tests_results.txt")
    with open(stats_results_path, "w") as f:
        f.write("Statistical Test Results and Distribution Statistics:\n")
        f.write("=" * 50 + "\n\n")

        # Statistical test results
        for test_name, (stat, p_val) in stat_results.items():
            f.write(f"{test_name}: Statistic = {stat}, p-value = {p_val}\n")
        f.write("\n")

        # Descriptive statistics
        for cell_type, values in data.items():
            if values:
                values_series = pd.Series(values)
                f.write(f"Cell Type: {cell_type.replace('_', ' ').title()}\n")
                f.write(f"  Total Cells: {len(values_series)}\n")
                f.write(f"  Min Puncta Count: {values_series.min()}\n")
                f.write(f"  Median Puncta Count: {values_series.median()}\n")
                f.write(f"  Max Puncta Count: {values_series.max()}\n")
                f.write(f"  Mean Puncta Count: {values_series.mean()}\n")
                f.write(f"  25th Percentile (Q1): {values_series.quantile(0.25)}\n")
                f.write(f"  75th Percentile (Q3): {values_series.quantile(0.75)}\n")
                f.write(f"  Interquartile Range (IQR): {values_series.quantile(0.75) - values_series.quantile(0.25)}\n")
                f.write("\n")
    print(f"Statistical test results and stats saved to {stats_results_path}")

# Updated palette to match Cell Type labels
formatted_colors = {
    "VGAT Positive OPRM1 Positive": "green",
    "VGLUT2 Positive OPRM1 Positive": "orange",
}

# Create box plot with annotations
if not vgat_data.empty and not vglut2_data.empty:
    comparison_data = pd.DataFrame({
        "Cell Type": ["VGAT Positive OPRM1 Positive"] * len(vgat_data) + ["VGLUT2 Positive OPRM1 Positive"] * len(vglut2_data),
        "Puncta Count": pd.concat([vgat_data, vglut2_data])
    })

    plt.figure(figsize=(10, 6))
    ax = sns.boxplot(data=comparison_data, x="Cell Type", y="Puncta Count", palette=formatted_colors)
    pairs = [("VGAT Positive OPRM1 Positive", "VGLUT2 Positive OPRM1 Positive")]
    annotator = Annotator(ax, pairs, data=comparison_data, x="Cell Type", y="Puncta Count")
    annotator.set_pvalues([u_p_value])
    annotator.annotate()

    plt.title("Comparison of Puncta Count for VGAT+ and VGLUT2+ Cells", fontsize=14)
    plt.xlabel("Cell Type")
    plt.ylabel("Puncta Count")
    plt.tight_layout()

    box_plot_path = os.path.join(plots_dir, "Box_Comparison_VGAT_vs_VGLUT2_with_annotations.png")
    plt.savefig(box_plot_path)
    plt.close()

    print(f"Box plot with annotations saved to {box_plot_path}.")
