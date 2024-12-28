import os
import pandas as pd
import matplotlib.pyplot as plt

# Define the input directory
input_directory = "/Volumes/backup driv/VP_qp_LF - ITERATION4/detections_iteration4_withMu_12.23.24"
output_csv_directory = os.path.join(input_directory, "detections_csv")
os.makedirs(output_csv_directory, exist_ok=True)

# Ensure the output directories exist
os.makedirs(output_csv_directory, exist_ok=True)

# Function to convert text files to CSV
def convert_text_to_csv(input_path, output_path):
    print(f"Looking for files in: {input_path}")
    for file in os.listdir(input_path):
        if file.endswith(".txt"):
            input_file = os.path.join(input_path, file)
            output_file = os.path.join(output_path, file.replace(".txt", ".csv"))
            try:
                # Assuming tab-delimited text files
                df = pd.read_csv(input_file, sep="\t")
                df.to_csv(output_file, index=False)
                print(f"Converted {file} to {output_file}")
            except Exception as e:
                print(f"Error converting {file}: {e}")

# Convert raw detection files
convert_text_to_csv(input_directory, output_csv_directory)

# Get all converted detection CSV files
filelist = [f for f in os.listdir(output_csv_directory) if f.endswith(".csv")]

# Define Qupath colors and classifications
QPink = "AF488"  # QP Pink
QPBlue = "AF647"  # QP Blue

Pink_posName = "vglut2_Pos"
Pink_posName_2 = "vglut2_Pos: vgat_Neg"
Blue_posName = "vgat_Pos"
Blue_posName_2 = "vglut2_Neg: vgat_Pos"
double_positive = "vglut2_Pos: vgat_Pos"

double_negative = "vglut2_Neg: vgat_Neg"

# Initialize an empty dataframe with relevant columns
DataDraft = pd.DataFrame(columns=[
    "Sample", 
    "vglut2-: vgat+ Cell Density (cells/mm^2)", 
    "vglut2-: vgat+ Cell Count", 
    "vglut2-: vgat+ Cell Area (mm^2)", 
    "vglut2-: vgat+ Cell Percentage", 
    "vglut2-: vgat+ Intensity", 
    "vglut2+: vgat- Cell Density (cells/mm^2)", 
    "vglut2+: vgat- Cell Count", 
    "vglut2+: vgat- Cell Area (mm^2)", 
    "vglut2+: vgat- Cell Percentage", 
    "vglut2+: vgat- Intensity", 
    "Double Positive Cell Density (cells/mm^2)", 
    "Double Positive Cell Count", 
    "Double Positive Cell Area (mm^2)", 
    "Double Positive Cell Percentage", 
    "Double Negative Cell Density (cells/mm^2)",
    "Double Negative Cell Count", 
    "Double Negative Cell Area (mm^2)", 
    "Double Negative Cell Percentage", 
    "Total Cell Area (mm^2)", 
    "Total Annotation Area (mm^2)"
])

# Process each file
for k, file in enumerate(filelist):
    try:
        # Read detection data
        det_data = pd.read_csv(os.path.join(output_csv_directory, file))
        filename = file.replace(" Detections", "")

        # Debug: Print the first few rows
        print(f"Processing {file}")
        print("Detection Data:")
        print(det_data.head())

        # Subset data for specific cell populations
        QPpink_only = det_data[det_data['Classification'].isin([Pink_posName, Pink_posName_2])]
        QPblue_only = det_data[det_data['Classification'].isin([Blue_posName, Blue_posName_2])]
        QPboth = det_data[det_data['Classification'] == double_positive]
        QPnone = det_data[det_data['Classification'] == double_negative]

        # Calculate areas and statistics
        posPinkArea = QPpink_only['Cell: Area µm^2'].sum() / 1e6 if not QPpink_only.empty else 0
        posBlueArea = QPblue_only['Cell: Area µm^2'].sum() / 1e6 if not QPblue_only.empty else 0
        posBothArea = QPboth['Cell: Area µm^2'].sum() / 1e6 if not QPboth.empty else 0
        posNoneArea = QPnone['Cell: Area µm^2'].sum() / 1e6 if not QPnone.empty else 0
        totalCellArea = posPinkArea + posBlueArea + posBothArea + posNoneArea

        pinkCellCount = len(QPpink_only)
        blueCellCount = len(QPblue_only)
        bothCellCount = len(QPboth)
        noneCellCount = len(QPnone)
        totalCells = pinkCellCount + blueCellCount + bothCellCount + noneCellCount

        pinkPercentage = (pinkCellCount / totalCells * 100) if totalCells > 0 else None
        bluePercentage = (blueCellCount / totalCells * 100) if totalCells > 0 else None
        bothPercentage = (bothCellCount / totalCells * 100) if totalCells > 0 else None
        nonePercentage = (noneCellCount / totalCells * 100) if totalCells > 0 else None

        # Populate DataDraft
        DataDraft.loc[k, "Sample"] = filename
        DataDraft.loc[k, "vglut2-: vgat+ Cell Density (cells/mm^2)"] = (blueCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "vglut2-: vgat+ Cell Count"] = blueCellCount
        DataDraft.loc[k, "vglut2-: vgat+ Cell Area (mm^2)"] = posBlueArea
        DataDraft.loc[k, "vglut2-: vgat+ Cell Percentage"] = bluePercentage

        DataDraft.loc[k, "vglut2+: vgat- Cell Density (cells/mm^2)"] = (pinkCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "vglut2+: vgat- Cell Count"] = pinkCellCount
        DataDraft.loc[k, "vglut2+: vgat- Cell Area (mm^2)"] = posPinkArea
        DataDraft.loc[k, "vglut2+: vgat- Cell Percentage"] = pinkPercentage

        DataDraft.loc[k, "Double Positive Cell Density (cells/mm^2)"] = (bothCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "Double Positive Cell Count"] = bothCellCount
        DataDraft.loc[k, "Double Positive Cell Area (mm^2)"] = posBothArea
        DataDraft.loc[k, "Double Positive Cell Percentage"] = bothPercentage

        DataDraft.loc[k, "Double Negative Cell Density (cells/mm^2)"] = (noneCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "Double Negative Cell Count"] = noneCellCount
        DataDraft.loc[k, "Double Negative Cell Area (mm^2)"] = posNoneArea
        DataDraft.loc[k, "Double Negative Cell Percentage"] = nonePercentage

        DataDraft.loc[k, "Total Cell Area (mm^2)"] = totalCellArea

        print(f"Processed {file}")
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Write the results to a CSV and XLSX file
DataDraft.to_csv("processed_data_with_percentages.csv", index=False)
DataDraft.to_excel("processed_data_with_percentages.xlsx", index=False)

# Define the output directory for plots
plot_output_dir = os.path.join(input_directory, "cell_type_plots")
os.makedirs(plot_output_dir, exist_ok=True)

# Define a function to generate a single bar plot with all cell types
def plot_all_cell_types(data, cell_types, output_dir):
    """
    Create a bar plot for all cell types with error bars.

    Parameters:
        data (pd.DataFrame): The dataframe containing cell count data.
        cell_types (list): List of cell type columns to plot.
        output_dir (str): Directory to save the plot.
    """
    means = []
    lower_errors = []
    upper_errors = []
    for cell_type in cell_types:
        counts = data[cell_type]
        mean = counts.mean()
        std = counts.std()
        means.append(mean)
        lower_errors.append(max(0, mean - std))
        upper_errors.append(mean + std)

    plt.figure(figsize=(10, 6))
    plt.bar(cell_types, means, yerr=[
        [mean - low for mean, low in zip(means, lower_errors)],
        [high - mean for mean, high in zip(means, upper_errors)]
    ], capsize=5, alpha=0.7, color=["black", "blue", "red", "purple"]
    plt.ylabel("Cell Count", fontweight="bold", fontsize=12)
    plt.title("Cell Counts with Error Bars for All Types", fontweight="bold", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontweight="bold", fontsize=10)
    plt.yticks(fontweight="bold", fontsize=10)
    plt.tight_layout()

    plot_path = os.path.join(output_dir, "all_cell_types_plot.png")
    plt.savefig(plot_path)
    plt.close()

    print(f"Plot saved to {plot_path}")

# Define cell types for plotting
cell_type_columns = [
    "vglut2_Neg: vgat_Neg Cell Count",
    "vglut2_Neg: vgat_Pos Cell Count",
    "vglut2_Pos: vgat_Neg Cell Count",
    "vglut2_Pos: vgat_Pos Cell Count"
]

# Generate the plot
plot_all_cell_types(DataDraft, cell_type_columns, plot_output_dir)

print("All plots generated and saved.")
