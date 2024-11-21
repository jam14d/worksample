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
        print(QPpink_only)

        # Calculate areas only if there are any cells
        posPinkArea = QPpink_only['Cell: Area µm^2'].sum() / 1e6 if not QPpink_only.empty else None
        posBlueArea = QPblue_only['Cell: Area µm^2'].sum() / 1e6 if not QPblue_only.empty else None
        posBothArea = QPboth['Cell: Area µm^2'].sum() / 1e6 if not QPboth.empty else None

        totalCellArea = (posPinkArea if posPinkArea else 0) + (posBlueArea if posBlueArea else 0) + (posBothArea if posBothArea else 0)

        realAnnotations = read_data_ano[read_data_ano['Name'].isin(["Annotation", "PathAnnotationObject"])]
        anoArea = realAnnotations['Area µm^2'].sum() / 1e6 if not realAnnotations.empty else None

        # Calculate mean intensity for each channel only if there are any cells
        pinkIntensity = QPpink_only['AF488: Cell: Mean'].mean() if not QPpink_only.empty else None
        blueIntensity = QPblue_only['AF647: Cell: Mean'].mean() if not QPblue_only.empty else None

        # Calculate cell count only if there are any cells
        totalCells = len(QPpink_only) + len(QPblue_only) + len(QPboth)

        # Prevent division by zero and fill in DataDraft with meaningful values
        DataDraft.loc[k, "Sample"] = filename
        DataDraft.loc[k, "vglut2-: vgat+ Cell Density (cells/mm^2)"] = (len(QPblue_only) / totalCellArea) if totalCellArea and len(QPblue_only) > 0 else None
        DataDraft.loc[k, "vglut2-: vgat+ Cell Count"] = len(QPblue_only)
        DataDraft.loc[k, "vglut2-: vgat+ Cell Area (mm^2)"] = posBlueArea if posBlueArea else None
        DataDraft.loc[k, "vglut2-: vgat+ Intensity"] = blueIntensity if blueIntensity else None

        DataDraft.loc[k, "vglut2+: vgat- Cell Density (cells/mm^2)"] = (len(QPpink_only) / totalCellArea) if totalCellArea and len(QPpink_only) > 0 else None
        DataDraft.loc[k, "vglut2+: vgat- Cell Count"] = len(QPpink_only)
        DataDraft.loc[k, "vglut2+: vgat- Cell Area (mm^2)"] = posPinkArea if posPinkArea else None
        DataDraft.loc[k, "vglut2+: vgat- Intensity"] = pinkIntensity if pinkIntensity else None

        DataDraft.loc[k, "Double Positive Cell Density (cells/mm^2)"] = (len(QPboth) / totalCellArea) if totalCellArea and len(QPboth) > 0 else None
        DataDraft.loc[k, "Double Positive Cell Count"] = len(QPboth)
        DataDraft.loc[k, "Double Positive Cell Area (mm^2)"] = posBothArea if posBothArea else None

        DataDraft.loc[k, "Total Cell Area (mm^2)"] = totalCellArea if totalCellArea else None
        DataDraft.loc[k, "Total Annotation Area (mm^2)"] = anoArea if anoArea else None

        print(f"Processed {file}")
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Write the results to a CSV and XLSX file
DataDraft.to_csv("pls_work.csv", index=False)
DataDraft.to_excel("Data_1.xlsx", index=False)
