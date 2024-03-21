import streamlit as st
import cv2
import numpy as np
from skimage.filters import threshold_otsu
from PIL import Image
import json

def basic_tissue_detection(image):
    # Convert PIL image to OpenCV format
    image = np.array(image)
    image = image[:, :, ::-1].copy()

    # Convert to Grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Threshold (Otsu's method)
    thresh_val = threshold_otsu(gray_image)
    _, binary_mask = cv2.threshold(gray_image, thresh_val, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return binary_mask, contours

def generate_geojson(contours):
    # Create the base GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for contour in contours:
        # Simplify contour to a list of [x, y] coordinates
        # GeoJSON uses [longitude, latitude], but here it will be [x, y] since it's not geographical data
        coordinates = contour.squeeze().tolist()

        # GeoJSON Polygon coordinates should be in a specific nesting structure and closed (first == last)
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])

        # Append a new feature for each contour
        geojson["features"].append({
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]  # Note the extra brackets as GeoJSON expects an array of linear rings
            },
            "properties": {}  # Empty properties, could be extended with relevant info
        })

    return json.dumps(geojson, indent=2)

st.title("Simple Tissue Detection with GeoJSON Annotation Download")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    st.write("Detecting tissue...")
    result, contours = basic_tissue_detection(image)
    
    # Display detection result
    result_display = Image.fromarray(result)
    st.image(result_display, caption='Tissue Detection Result', use_column_width=True)

    # Generate GeoJSON annotations
    geojson_annotations = generate_geojson(contours)
    
    # Download button for GeoJSON annotations
    st.download_button(label="Download Annotations as GeoJSON",
                       data=geojson_annotations,
                       file_name="annotations.geojson",
                       mime="application/json")