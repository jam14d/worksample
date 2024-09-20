import os
import pandas as pd
import streamlit as st

import os
import pandas as pd
import streamlit as st

# Streamlit app title and creator info
st.title("Image Analysis Assistant")
st.write("Created by Jamie Anne Mortel")
st.write("For questions, please contact: [jmortel@health.ucsd.edu](mailto:jmortel@health.ucsd.edu)")

# Section 1: Classification names in QuPath
st.header("Section 1: Classification Names in QuPath")
st.write("Please enter the classification names used in QuPath for your analysis.")
cell_name = st.text_input("Cell Name in QuPath:", value="PathCellObject")
pink_pos_name_1 = st.text_input("Marker 1 Positive Name:", value="DRD1_Pos")
pink_pos_name_2 = st.text_input("Marker 1 Positive Name 2:", value="DRD1_Pos: A2A_Neg")
blue_pos_name_1 = st.text_input("Marker 2 Positive Name:", value="A2A_Pos")
blue_pos_name_2 = st.text_input("Marker 2 Positive Name 2:", value="DRD1_Neg: A2A_Pos")
double_positive_name = st.text_input("Double Positive Name:", value="DRD1_Pos: A2A_Pos")
yellow_pos_name = st.text_input("Marker 3 Positive Name:", value="oprm1_Pos")

# Section 2: String values used by QuPath
st.header("Section 2: QuPath String Values")
st.write("Enter the column names that QuPath uses for intensity measurements. These names may differ from your native color names.")
pink_intensity_col = st.text_input("Column Name for Pink Intensity:", value="TurboYFP: Mean")
blue_intensity_col = st.text_input("Column Name for Blue Intensity:", value="mRFP1: Mean")

# Section 3: Upload data files
st.header("Section 3: Upload Your QuPath Exported Data")
st.write("Please upload your exported detection and annotation files from QuPath.")
uploaded_det = st.file_uploader("Upload Detection Files", type="txt", accept_multiple_files=True)
uploaded_ano = st.file_uploader("Upload Annotation Files", type="txt", accept_multiple_files=True)

# Section 4: Saving the output CSV
st.header("Section 4: Save Your Output CSV")
st.write("Specify the path where you would like to save the generated CSV file. Remember to include 'Data.csv' at the end!")
csv_save_path = st.text_input("Path to Save CSV (e.g., /path/to/save/Data.csv):", value="Data.csv")

# Initialize DataDraft DataFrame and processing logic here...
# [Rest of your processing logic goes here]




# Initialize an empty dataframe with relevant columns
columns = [
    "Sample", 
    "DRD1-: A2A+ Cell Density (cells/mm^2)", 
    "DRD1-: A2A+ Cell Count", 
    "DRD1-: A2A+ Cell Area (mm^2)", 
    "DRD1-: A2A+ Cell Percentage", 
    "DRD1-: A2A+ Intensity", 
    "DRD1+: A2A- Cell Density (cells/mm^2)", 
    "DRD1+: A2A- Cell Count", 
    "DRD1+: A2A- Cell Area (mm^2)", 
    "DRD1+: A2A- Cell Percentage", 
    "DRD1+: A2A- Intensity", 
    "Double Positive Cell Density (cells/mm^2)", 
    "Double Positive Cell Count", 
    "Double Positive Cell Area (mm^2)", 
    "Double Positive Cell Percentage", 
    "Total Cell Count", 
    "Total Cell Area (mm^2)", 
    "Total Annotation Area (mm^2)"
]
data_draft = pd.DataFrame(columns=columns)

# Button to process files
if st.button("Process Files"):
    if uploaded_det and uploaded_ano:
        for det_file, ano_file in zip(uploaded_det, uploaded_ano):
            # Read the detection and annotation data
            detection_data = pd.read_csv(det_file, sep="\t")
            annotation_data = pd.read_csv(ano_file, sep="\t")
            filename = det_file.name.replace(" Detections", "")

            # Subset data for specific cell populations
            qp_pink_only = detection_data[detection_data['Name'].isin([pink_pos_name_1, pink_pos_name_2])]
            qp_blue_only = detection_data[detection_data['Name'].isin([blue_pos_name_1, blue_pos_name_2])]
            qp_both = detection_data[detection_data['Name'] == double_positive_name]
            qp_neg = detection_data[detection_data['Name'] == cell_name]

            # Calculate areas
            negative_area = qp_neg['Area µm^2'].sum() / 1e6
            pos_pink_area = qp_pink_only['Area µm^2'].sum() / 1e6
            pos_blue_area = qp_blue_only['Area µm^2'].sum() / 1e6
            pos_both_area = qp_both['Area µm^2'].sum() / 1e6
            total_cell_area = negative_area + pos_pink_area + pos_blue_area + pos_both_area

            # Calculate annotation area
            real_annotations = annotation_data[annotation_data['Name'].isin(["Annotation", "PathAnnotationObject"])]
            annotation_area = real_annotations['Area µm^2'].sum() / 1e6

            # Calculate mean intensity for each channel using user-defined column names
            pink_intensity = qp_pink_only[pink_intensity_col].mean() if pink_intensity_col in qp_pink_only.columns else 0
            blue_intensity = qp_blue_only[blue_intensity_col].mean() if blue_intensity_col in qp_blue_only.columns else 0

            total_cells = len(qp_pink_only) + len(qp_blue_only) + len(qp_both) + len(qp_neg)

            # Fill in DataDraft
            data_draft.loc[len(data_draft)] = [
                filename,
                len(qp_blue_only) / total_cell_area,
                len(qp_blue_only),
                pos_blue_area,
                len(qp_blue_only) / total_cells,
                blue_intensity,
                len(qp_pink_only) / total_cell_area,
                len(qp_pink_only),
                pos_pink_area,
                len(qp_pink_only) / total_cells,
                pink_intensity,
                len(qp_both) / total_cell_area,
                len(qp_both),
                pos_both_area,
                len(qp_both) / total_cells,
                total_cells,
                total_cell_area,
                annotation_area
            ]

            st.write(f"Processed {det_file.name}")

        # Write the results to a CSV file
        data_draft.to_csv(csv_save_path, index=False)
        st.success(f"Processing complete! File saved as {csv_save_path}.")
    else:
        st.error("Please upload both detection and annotation files.")
