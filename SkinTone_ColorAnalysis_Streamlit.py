import streamlit as st
import cv2
import numpy as np
from PIL import Image

'''IN PROGRESS'''

def create_skin_mask(image):
    # Convert the image from PIL to CV2 format
    image = np.array(image.convert('RGB'))
    image = image[:, :, ::-1]  # Convert RGB to BGR, which CV2 uses

    # Convert the image from BGR to YCrCb color space
    ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

    # Define the minimum and maximum YCrCb values for skin tones
    min_YCrCb = np.array([0, 133, 77], np.uint8)
    max_YCrCb = np.array([255, 173, 127], np.uint8)

    # Create a mask that identifies the skin based on YCrCb range
    skin_mask = cv2.inRange(ycrcb_image, min_YCrCb, max_YCrCb)

    # Apply the mask to the image to get the skin region
    skin = cv2.bitwise_and(image, image, mask=skin_mask)

    # Find the average color of skin
    mask_bool = skin_mask.astype(bool)
    skin_pixels = image[mask_bool]
    average_color = np.mean(skin_pixels, axis=0).astype(np.uint8)

    # Calculate the complementary color of the average skin tone
    complementary_color = np.array([255, 255, 255], np.uint8) - average_color

    # Create an image filled with the complementary color
    complementary_color_image = np.full((100, 100, 3), complementary_color, np.uint8)

    return image, skin_mask, skin, complementary_color_image

def main():
    st.title("Skin Tone Analysis and Complementary Color Finder")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        st.write("")
        st.write("Processing...")

        original, mask, detected_skin, complementary_color = create_skin_mask(image)

        # Convert BGR to RGB for display
        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        detected_skin_rgb = cv2.cvtColor(detected_skin, cv2.COLOR_BGR2RGB)
        complementary_color_rgb = cv2.cvtColor(complementary_color, cv2.COLOR_BGR2RGB)

        st.image(original_rgb, caption='Original Image', use_column_width=True)
        
        # Convert mask to a 3-channel image for proper display
        mask_display = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        st.image(mask_display, caption='Skin Mask', use_column_width=True)
        
        st.image(detected_skin_rgb, caption='Skin Detection Result', use_column_width=True)
        st.image(complementary_color_rgb, caption='Complementary Color', use_column_width=True)

if __name__ == "__main__":
    main()
