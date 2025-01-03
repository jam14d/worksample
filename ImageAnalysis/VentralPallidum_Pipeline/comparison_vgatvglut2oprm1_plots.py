import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu, ks_2samp

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
plots_dir = os.path.join(script_dir, "oprm1VGATvsVGLUT2_plots")
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


##STATS


# Perform statistical tests between VGAT+ and VGLUT2+ groups
vgat_data = data["vgat_positive_oprm1_positive"]
vglut2_data = data["vglut2_positive_oprm1_positive"]

if not vgat_data.empty and not vglut2_data.empty:
    # Extract intensity values
    vgat_intensity = vgat_data["AF568: Cell: Mean"]
    vglut2_intensity = vglut2_data["AF568: Cell: Mean"]

    # Mann-Whitney U Test (non-parametric comparison of medians)
    u_stat, u_p_value = mannwhitneyu(vgat_intensity, vglut2_intensity, alternative='two-sided')
    print(f"Mann-Whitney U Test: U-statistic = {u_stat}, p-value = {u_p_value}")

    # Kolmogorov-Smirnov Test (non-parametric comparison of distributions)
    ks_stat, ks_p_value = ks_2samp(vgat_intensity, vglut2_intensity)
    print(f"Kolmogorov-Smirnov Test: KS-statistic = {ks_stat}, p-value = {ks_p_value}")

    # Save results to a text file
    stats_results_path = os.path.join(plots_dir, "statistical_tests_results.txt")
    with open(stats_results_path, "w") as f:
        f.write("Statistical Test Results:\n")
        f.write(f"Mann-Whitney U Test: U-statistic = {u_stat}, p-value = {u_p_value}\n")
        f.write(f"Kolmogorov-Smirnov Test: KS-statistic = {ks_stat}, p-value = {ks_p_value}\n")
    print(f"Statistical test results saved to {stats_results_path}")
else:
    print("One or both datasets are empty. Cannot perform statistical tests.")



##PLOTS




# KDE Plot for OPRM1 Intensity
comparison_data = []
for cell_type, df in data.items():
    if not df.empty:
        comparison_data.extend([{"Cell Type": cell_type.replace("_", " ").title(), "Intensity": val} for val in df["AF568: Cell: Mean"]])

if comparison_data:
    comparison_df = pd.DataFrame(comparison_data)

    plt.figure(figsize=(10, 6))
    for cell_type, df in data.items():
        if not df.empty:
            sns.kdeplot(df["AF568: Cell: Mean"], label=cell_type.replace("_", ":").title(), color=colors[cell_type], fill=True, alpha=0.5)

    plt.title("Density Distribution of OPRM1 Intensity for VGAT+ and VGLUT2+ Cells", fontsize=16)
    plt.xlabel("OPRM1 Intensity")
    plt.ylabel("Density")
    plt.legend(title="Cell Type")
    plt.tight_layout()

    kde_path = os.path.join(plots_dir, "KDE_Comparison_VGAT_vs_VGLUT2.png")
    plt.savefig(kde_path)
    plt.close()
    print(f"KDE comparison plot saved to {kde_path}.")

    # Box Plot
    formatted_colors = {
        "Vgat Positive Oprm1 Positive": "green",
        "Vglut2 Positive Oprm1 Positive": "orange",
    }

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=comparison_df, x="Cell Type", y="Intensity", palette=formatted_colors)
    plt.title("Comparative Distribution of OPRM1 Intensity for VGAT+ and VGLUT2+ Cells", fontsize=16)
    plt.xlabel("Cell Type")
    plt.ylabel("OPRM1 Intensity")
    plt.tight_layout()

    box_plot_path = os.path.join(plots_dir, "Box_Comparison_VGAT_vs_VGLUT2.png")
    plt.savefig(box_plot_path)
    plt.close()
    print(f"Box plot saved to {box_plot_path}.")

# Scatter plots for Intensity vs. Number of Spots
for cell_type, df in data.items():
    if not df.empty:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=df,
            x="AF568: Cell: Mean",
            y="Subcellular: Channel 2: Num spots estimated",
            alpha=0.6,
            color=colors[cell_type]
        )
        plt.title(f"Intensity vs. Number of Puncta for {cell_type.replace('_', ':').title()}")
        plt.xlabel("OPRM1 Intensity")
        plt.ylabel("Number of Puncta")
        plt.grid(True)
        plt.tight_layout()

        scatter_path = os.path.join(plots_dir, f"Intensity_vs_Puncta_{cell_type}.png")
        plt.savefig(scatter_path)
        plt.close()
        print(f"Scatter plot for {cell_type.replace('_', ':').title()} saved to {plots_dir}")

# Joint plots for combined density and scatter
for cell_type, df in data.items():
    if not df.empty:
        joint_plot = sns.jointplot(
            data=df,
            x="AF568: Cell: Mean",
            y="Subcellular: Channel 2: Num spots estimated",
            kind="kde",
            fill=True,
            color=colors[cell_type]
        )
        joint_plot.plot_joint(sns.scatterplot, color=colors[cell_type], alpha=0.5)
        joint_plot.ax_joint.set_title(f"Intensity vs. Puncta Density for {cell_type.replace('_', ':').title()}", fontsize=12)
        joint_plot.set_axis_labels("OPRM1 Intensity", "Number of Puncta")

        joint_path = os.path.join(plots_dir, f"Density_vs_Puncta_{cell_type}.png")
        joint_plot.savefig(joint_path)
        plt.close()
        print(f"Joint plot for {cell_type.replace('_', ':').title()} saved to {plots_dir}")
