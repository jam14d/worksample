import cv2
import numpy as np

'''
IN PROGRESS

A simple, fun project inspired by the trend of Personal Color Analysis popular in Korea.
This script finds the average skin tone in an image, determines its complementary color, 
and then displays the original image, its mask, and a block of the complementary color.

'''

def create_skin_mask(image_path):
    # Load the image
    image = cv2.imread(image_path)

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
    # We first convert the mask to boolean, then find indices where mask is True
    mask_bool = skin_mask.astype(bool)
    skin_pixels = image[mask_bool]

    # Compute the average color of skin pixels
    average_color = np.mean(skin_pixels, axis=0).astype(np.uint8)
    print("Average skin color (BGR):", average_color)

    # Calculate the complementary color of the average skin tone
    complementary_color = np.array([255, 255, 255], np.uint8) - average_color
    print("Complementary color (BGR):", complementary_color)

    # Create an image filled with the complementary color
    complementary_color_image = np.full((100, 100, 3), complementary_color, np.uint8)

    # Display the original image, the mask, the detected skin, and the complementary color
    cv2.imshow('Original Image', image)
    cv2.imshow('Skin Mask', skin_mask)
    cv2.imshow('Skin Detection Result', skin)
    cv2.imshow('Complementary Color', complementary_color_image)

    # Wait for a key press and then close all windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Replace 'path_to_your_image.jpg' with the path to the image you want to process
create_skin_mask('path_to_your_image.jpg')

