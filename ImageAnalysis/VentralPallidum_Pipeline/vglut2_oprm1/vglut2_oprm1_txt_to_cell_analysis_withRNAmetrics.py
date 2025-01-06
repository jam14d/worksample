import os
import pandas as pd

##SPECIFIC TO vglut22: OPRM1 COMPOSITE
##IN PROGRESS!


# Define all paths in a single dictionary (Windows-style)
paths = {
    "raw_detection": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGLUT2_OPRM1_COMPOSITE/detections_iteration4_vglut2withMu_12.13.24",
    "raw_annotation": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGLUT2_OPRM1_COMPOSITE/annotations_iteration4_vglut2withMu_12.13.24",
    "detection_csv": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGLUT2_OPRM1_COMPOSITE/detections_iteration4_vglut2withMu_12.13.24_csv",
    "annotation_csv": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGLUT2_OPRM1_COMPOSITE/annotations_iteration4_vglut2withMu_12.13.24_csv"
}

# Function to convert Windows paths to Unix-like paths if running in a Unix environment
def convert_to_unix_path(win_path):
    if os.name != "nt":
        win_path = win_path.replace("\\", "/")
        if win_path[1:3] == ":/":
            return f"/mnt/{win_path[0].lower()}{win_path[2:]}"
    return win_path

# Convert all paths to Unix-like if necessary
paths = {key: convert_to_unix_path(value) for key, value in paths.items()}

# Ensure the output directories exist
os.makedirs(paths["detection_csv"], exist_ok=True)
os.makedirs(paths["annotation_csv"], exist_ok=True)

# Function to convert text files to CSV
def convert_text_to_csv(input_path, output_path):
    for file in os.listdir(input_path):
        if file.endswith(".txt"):
            input_file = os.path.join(input_path, file)
            output_file = os.path.join(output_path, file.replace(".txt", ".csv"))
            try:
                df = pd.read_csv(input_file, sep="\t")
                df.to_csv(output_file, index=False)
            except Exception as e:
                print(f"Error converting {file}: {e}")

# Convert raw detection and annotation files
convert_text_to_csv(paths["raw_detection"], paths["detection_csv"])
convert_text_to_csv(paths["raw_annotation"], paths["annotation_csv"])

# Get all converted detection CSV files
filelist = [f for f in os.listdir(paths["detection_csv"]) if f.endswith(".csv")]

# Define Qupath colors and classifications
QYellow = "AF568"
QPPink = "AF647"

Yellow_posName = "oprm1_Pos"
Yellow_posName_2 = "vglut2_Neg: oprm1_Pos"
Pink_posName = "vglut2_Pos"
Pink_posName_2 = "vglut2_Pos: oprm1_Neg"
double_positive = "vglut2_Pos: oprm1_Pos"
double_negative = "vglut2_Neg: oprm1_Neg"

# Additional subcellular metric columns
subcellular_metrics = [
    "Subcellular cluster: Channel 2: Area",
    "Subcellular cluster: Channel 2: Mean channel intensity",
    "Subcellular: Channel 2: Num spots estimated",
    "Subcellular: Channel 2: Num single spots",
    "Subcellular: Channel 2: Num clusters"
]

# Initialize an empty dataframe with relevant columns
DataDraft = pd.DataFrame(columns=[
    "Sample",
    "oprm1-: vglut2+ Cell Density (cells/mm^2)",
    "oprm1-: vglut2+ Cell Count",
    "oprm1-: vglut2+ Cell Area (mm^2)",
    "oprm1-: vglut2+ Cell Percentage",
    "oprm1-: vglut2+ Intensity",
    "oprm1+: vglut2- Cell Density (cells/mm^2)",
    "oprm1+: vglut2- Cell Count",
    "oprm1+: vglut2- Cell Area (mm^2)",
    "oprm1+: vglut2- Cell Percentage",
    "oprm1+: vglut2- Intensity",
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
] + [f"{metric} ({cls})" for metric in subcellular_metrics for cls in [Yellow_posName_2, Pink_posName_2, double_positive]])

# Process each file
for k, file in enumerate(filelist):
    try:
        det_data = pd.read_csv(os.path.join(paths["detection_csv"], file))
        filename = file.replace(" Detections", "")
        ano_file = os.path.join(paths["annotation_csv"], filename)
        if not os.path.exists(ano_file):
            continue
        ano_data = pd.read_csv(ano_file)

        # Subset data for specific cell populations
        QPYellow_only = det_data[det_data['Classification'].isin([Yellow_posName, Yellow_posName_2])]
        QPPink_only = det_data[det_data['Classification'].isin([Pink_posName, Pink_posName_2])]
        QPboth = det_data[det_data['Classification'] == double_positive]
        QPnone = det_data[det_data['Classification'] == double_negative]

        # Calculate areas and statistics
        posYellowArea = QPYellow_only['Cell: Area µm^2'].sum() / 1e6 if not QPYellow_only.empty else 0
        posPinkArea = QPPink_only['Cell: Area µm^2'].sum() / 1e6 if not QPPink_only.empty else 0
        posBothArea = QPboth['Cell: Area µm^2'].sum() / 1e6 if not QPboth.empty else 0
        posNoneArea = QPnone['Cell: Area µm^2'].sum() / 1e6 if not QPnone.empty else 0
        totalCellArea = posYellowArea + posPinkArea + posBothArea

        realAnnotations = ano_data[ano_data['Object type'].isin(["Annotation", "PathAnnotationObject"])]
        anoArea = realAnnotations['Area µm^2'].sum() / 1e6 if not realAnnotations.empty else 0

        YellowIntensity = QPYellow_only['AF568: Cell: Mean'].mean() if not QPYellow_only.empty else None
        PinkIntensity = QPPink_only['AF647: Cell: Mean'].mean() if not QPPink_only.empty else None

        YellowCellCount = len(QPYellow_only)
        PinkCellCount = len(QPPink_only)
        bothCellCount = len(QPboth)
        noneCellCount = len(QPnone)
        totalCells = YellowCellCount + PinkCellCount + bothCellCount

        YellowPercentage = (YellowCellCount / totalCells * 100) if totalCells > 0 else None
        PinkPercentage = (PinkCellCount / totalCells * 100) if totalCells > 0 else None
        bothPercentage = (bothCellCount / totalCells * 100) if totalCells > 0 else None
        nonePercentage = (noneCellCount / totalCells * 100) if totalCells > 0 else None

        # Populate DataDraft
        DataDraft.loc[k, "Sample"] = filename
        DataDraft.loc[k, "oprm1-: vglut2+ Cell Density (cells/mm^2)"] = (PinkCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "oprm1-: vglut2+ Cell Count"] = PinkCellCount
        DataDraft.loc[k, "oprm1-: vglut2+ Cell Area (mm^2)"] = posPinkArea
        DataDraft.loc[k, "oprm1-: vglut2+ Cell Percentage"] = PinkPercentage
        DataDraft.loc[k, "oprm1-: vglut2+ Intensity"] = PinkIntensity

        DataDraft.loc[k, "oprm1+: vglut2- Cell Density (cells/mm^2)"] = (YellowCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "oprm1+: vglut2- Cell Count"] = YellowCellCount
        DataDraft.loc[k, "oprm1+: vglut2- Cell Area (mm^2)"] = posYellowArea
        DataDraft.loc[k, "oprm1+: vglut2- Cell Percentage"] = YellowPercentage
        DataDraft.loc[k, "oprm1+: vglut2- Intensity"] = YellowIntensity

        DataDraft.loc[k, "Double Positive Cell Density (cells/mm^2)"] = (bothCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "Double Positive Cell Count"] = bothCellCount
        DataDraft.loc[k, "Double Positive Cell Area (mm^2)"] = posBothArea
        DataDraft.loc[k, "Double Positive Cell Percentage"] = bothPercentage

        DataDraft.loc[k, "Double Negative Cell Density (cells/mm^2)"] = (noneCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "Double Negative Cell Count"] = noneCellCount
        DataDraft.loc[k, "Double Negative Cell Area (mm^2)"] = posNoneArea
        DataDraft.loc[k, "Double Negative Cell Percentage"] = nonePercentage

        DataDraft.loc[k, "Total Cell Area (mm^2)"] = totalCellArea
        DataDraft.loc[k, "Total Annotation Area (mm^2)"] = anoArea

        # Subcellular metrics
        for cls in [Yellow_posName_2, Pink_posName_2, double_positive, double_negative]:
            cls_data = det_data[det_data['Classification'] == cls]
            for metric in subcellular_metrics:
                DataDraft.loc[k, f"{metric} ({cls})"] = cls_data[metric].sum() if metric in cls_data.columns else None

    except Exception as e:
        print(f"Error processing {file}: {e}")

# Write the results to CSV and XLSX
DataDraft.to_csv("vglut2_oprm1_subcellular_metrics.csv", index=False)
DataDraft.to_excel("vglut2_oprm1_subcellular_metrics.xlsx", index=False)
