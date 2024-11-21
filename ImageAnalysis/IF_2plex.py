import os
import pandas as pd

# Set the paths
path_det = "/Users/jamieannemortel/Downloads/RawData_Composite/detection results"
path_ano = "/Users/jamieannemortel/Downloads/RawData_Composite/annotation results"

# Get all .txt files from the directory
filelist = [f for f in os.listdir(path_det) if f.endswith(".txt")]

# Define Qupath colors
QPink = "AF488"  # QP Pink
QPBlue = "AF647"   # QP Blue

# QP string names
Pink_posName = "vglut2_Pos"
Pink_posName_2 = "vglut2_Pos: vgat_Neg"
Blue_posName = "vgat_Pos"
Blue_posName_2 = "vglut2_Neg: vgat_Pos"
double_positive = "vglut2_Pos: vgat_Pos"

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
    "Total Cell Area (mm^2)", 
    "Total Annotation Area (mm^2)"
])

# Loop through each file
for k, file in enumerate(filelist):
    try:
        # Read the detection and annotation data
        read_data = pd.read_csv(os.path.join(path_det, file), sep="\t")
        filename = file.replace(" Detections", "")
        read_data_ano = pd.read_csv(os.path.join(path_ano, filename), sep="\t")

        # Subset data for specific cell populations
        QPpink_only = read_data[read_data['Name'].isin([Pink_posName, Pink_posName_2])]
        QPblue_only = read_data[read_data['Name'].isin([Blue_posName, Blue_posName_2])]
        QPboth = read_data[read_data['Name'] == double_positive]

        # Calculate areas
        posPinkArea = QPpink_only['Cell: Area µm^2'].sum() / 1e6 if not QPpink_only.empty else 0
        posBlueArea = QPblue_only['Cell: Area µm^2'].sum() / 1e6 if not QPblue_only.empty else 0
        posBothArea = QPboth['Cell: Area µm^2'].sum() / 1e6 if not QPboth.empty else 0

        totalCellArea = posPinkArea + posBlueArea + posBothArea

        realAnnotations = read_data_ano[read_data_ano['Name'].isin(["Annotation", "PathAnnotationObject"])]
        anoArea = realAnnotations['Area µm^2'].sum() / 1e6 if not realAnnotations.empty else 0

        # Calculate mean intensity for each channel
        pinkIntensity = QPpink_only['AF488: Cell: Mean'].mean() if not QPpink_only.empty else 0
        blueIntensity = QPblue_only['AF647: Cell: Mean'].mean() if not QPblue_only.empty else 0

        totalCells = len(QPpink_only) + len(QPblue_only) + len(QPboth)

        # Fill in DataDraft
        DataDraft.loc[k, "Sample"] = filename
        DataDraft.loc[k, "vglut2-: vgat+ Cell Density (cells/mm^2)"] = len(QPblue_only) / totalCellArea if totalCellArea > 0 else 0
        DataDraft.loc[k, "vglut2-: vgat+ Cell Count"] = len(QPblue_only)
        DataDraft.loc[k, "vglut2-: vgat+ Cell Area (mm^2)"] = posBlueArea
        DataDraft.loc[k, "vglut2-: vgat+ Intensity"] = blueIntensity

        DataDraft.loc[k, "vglut2+: vgat- Cell Density (cells/mm^2)"] = len(QPpink_only) / totalCellArea if totalCellArea > 0 else 0
        DataDraft.loc[k, "vglut2+: vgat- Cell Count"] = len(QPpink_only)
        DataDraft.loc[k, "vglut2+: vgat- Cell Area (mm^2)"] = posPinkArea
        DataDraft.loc[k, "vglut2+: vgat- Intensity"] = pinkIntensity

        DataDraft.loc[k, "Double Positive Cell Density (cells/mm^2)"] = len(QPboth) / totalCellArea if totalCellArea > 0 else 0
        DataDraft.loc[k, "Double Positive Cell Count"] = len(QPboth)
        DataDraft.loc[k, "Double Positive Cell Area (mm^2)"] = posBothArea

        DataDraft.loc[k, "Total Cell Area (mm^2)"] = totalCellArea
        DataDraft.loc[k, "Total Annotation Area (mm^2)"] = anoArea

        print(f"Processed {file}")
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Write the results to a CSV and XLSX file
DataDraft.to_csv("Data.csv", index=False)
DataDraft.to_excel("Data.xlsx", index=False)
