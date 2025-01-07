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

# Function to convert Windows paths to Unix-like paths if running in a Unix environment
def convert_to_unix_path(win_path):
    if os.name != "nt":
        win_path = win_path.replace("\\", "/")
        if win_path[1:3] == ":/":
            return f"/mnt/{win_path[0].lower()}{win_path[2:]}"
    return win_path

# Convert all paths to Unix-like if necessary
for group in paths:
    paths[group] = {key: convert_to_unix_path(value) for key, value in paths[group].items()}

# Create a "plots" directory in the same location as the script
script_dir = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(script_dir, "oprm1VGATvsVGLUT2_plots_puncta")
os.makedirs(plots_dir, exist_ok=True)

# Define classifications and colors
classifications = {
    "vgat_positive_oprm1_positive": ["vgat_Pos: oprm1_Pos"],
    "vglut2_positive_oprm1_positive": ["vglut2_Pos: oprm1_Pos"],
}
colors = {
    "vgat_positive_oprm1_positive": "green",
    "vglut2_positive_oprm1_positive": "orange",
}

# Initialize a dictionary to collect data for each classification
data = {key: [] for key in classifications.keys()}

# Helper function to process files and extract relevant data
def collect_data(paths, classification_key, labels):
    for file in os.listdir(paths["raw_detection"]):
        if file.endswith(".txt"):
            try:
                det_data = pd.read_csv(os.path.join(paths["raw_detection"], file), sep="\t", encoding="utf-8")
                if "Classification" not in det_data.columns:
                    print(f"Skipping file {file}: 'Classification' column is missing.")
                    continue
                cell_data = det_data[det_data["Classification"].isin(labels)]
                data[classification_key].append(cell_data[[
                    "AF568: Cell: Mean", 
                    "Subcellular: Channel 2: Num spots estimated"
                ]].dropna())
            except UnicodeDecodeError:
                print(f"Encoding error in file {file}: Skipping.")
            except Exception as e:
                print(f"Error processing {file}: {e}")

# Collect data for each classification
collect_data(paths["vgat"], "vgat_positive_oprm1_positive", classifications["vgat_positive_oprm1_positive"])
collect_data(paths["vglut2"], "vglut2_positive_oprm1_positive", classifications["vglut2_positive_oprm1_positive"])

# Combine data for each classification into a single DataFrame
for key in data:
    if data[key]:
        data[key] = pd.concat(data[key], ignore_index=True)
    else:
        data[key] = pd.DataFrame(columns=["AF568: Cell: Mean", "Subcellular: Channel 2: Num spots estimated"])

# Perform statistical tests between VGAT+ and VGLUT2+ groups
vgat_data = data["vgat_positive_oprm1_positive"]
vglut2_data = data["vglut2_positive_oprm1_positive"]

stat_results = {}

if not vgat_data.empty and not vglut2_data.empty:
    vgat_subcellularspots = vgat_data["Subcellular: Channel 2: Num spots estimated"]
    vglut2_subcellularspots = vglut2_data["Subcellular: Channel 2: Num spots estimated"]

    # Mann-Whitney U Test
    u_stat, u_p_value = mannwhitneyu(vgat_subcellularspots, vglut2_subcellularspots, alternative='two-sided')
    stat_results["Mann-Whitney"] = (u_stat, u_p_value)

    # Kolmogorov-Smirnov Test
    ks_stat, ks_p_value = ks_2samp(vgat_subcellularspots, vglut2_subcellularspots)
    stat_results["Kolmogorov-Smirnov"] = (ks_stat, ks_p_value)

    # Save results to a text file
    stats_results_path = os.path.join(plots_dir, "statistical_tests_results.txt")
    with open(stats_results_path, "w") as f:
        f.write("Statistical Test Results:\n")
        for test_name, (stat, p_val) in stat_results.items():
            f.write(f"{test_name}: Statistic = {stat}, p-value = {p_val}\n")
    print(f"Statistical test results saved to {stats_results_path}")

#comparisondata storage
comparison_data = []
for cell_type, df in data.items():
    if not df.empty:
        comparison_data.extend([{"Cell Type": cell_type.replace("_", " ").title(), "Puncta Count": val} for val in df["Subcellular: Channel 2: Num spots estimated"]])

if comparison_data:
    comparison_df = pd.DataFrame(comparison_data)

# # KDE Plot
    # plt.figure(figsize=(10, 6))
    # for cell_type, df in data.items():
    #     if not df.empty:
    #         sns.kdeplot(df["Subcellular: Channel 2: Num spots estimated"], label=cell_type.replace("_", ":").title(), color=colors[cell_type], fill=True, alpha=0.5)

#     plt.title("Density Distribution of OPRM1 Subcellular Spots for VGAT+ and VGLUT2+ Cells", fontsize=16)
#     plt.xlabel("OPRM1 Subcellular Spots")
#     plt.ylabel("Density")
#     plt.legend(title="Cell Type")
#     plt.tight_layout()

#     kde_path = os.path.join(plots_dir, "KDE_Comparison_VGAT_vs_VGLUT2.png")
#     plt.savefig(kde_path)
#     plt.close()
#     print(f"KDE comparison plot saved to {kde_path}.")

#boxplot
# Define a formatted palette that matches the DataFrame's "Cell Type" column
formatted_colors = {
    "Vgat Positive Oprm1 Positive": "green",
    "Vglut2 Positive Oprm1 Positive": "orange",
}

# Box Plot with Statistical Annotation
plt.figure(figsize=(10, 6))
ax = sns.boxplot(
    data=comparison_df,
    x="Cell Type",
    y="Puncta Count",
    palette=formatted_colors  # Use the corrected palette
)

# Annotator setup
pairs = [("Vgat Positive Oprm1 Positive", "Vglut2 Positive Oprm1 Positive")]
annotator = Annotator(ax, pairs, data=comparison_df, x="Cell Type", y="Puncta Count")
annotator.set_pvalues([u_p_value])  # Use the Mann-Whitney U-test p-value
annotator.annotate()

plt.title("Comparative Distribution of Puncta Count for VGAT+:OPRM1+ and VGLUT2+:OPRM1+ Cells", fontsize=12)
plt.xlabel("Cell Type")
plt.ylabel("OPRM1 Puncta Count")
plt.tight_layout()

box_plot_path = os.path.join(plots_dir, "Box_Comparison_VGAT_vs_VGLUT2_with_annotations.png")
plt.savefig(box_plot_path)
plt.close()
print(f"Box plot with statistical annotations saved to {box_plot_path}.")
