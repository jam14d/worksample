import streamlit as st
import cv2
import numpy as np
from skimage.filters import threshold_otsu
from PIL import Image
import io

def basic_tissue_detection(image):
    # Convert PIL image to OpenCV format
    image = np.array(image)
    image = image[:, :, ::-1].copy() 

    # Convert to Grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Threshold (Otsu's method)
    thresh_val = threshold_otsu(gray_image)
    _, binary_mask = cv2.threshold(gray_image, thresh_val, 255, cv2.THRESH_BINARY_INV)
    
    return binary_mask

st.title("Simple Tissue Detection")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    st.write("Detecting tissue...")
    result = basic_tissue_detection(image)
    
    # Convert the processed image to display it with Streamlit
    result_display = Image.fromarray(result)
    st.image(result_display, caption='Tissue Detection Result', use_column_width=True)
