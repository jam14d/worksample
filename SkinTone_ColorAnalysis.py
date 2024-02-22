import cv2
import numpy as np

'''

A simple, fun project inspired by the trend of Personal Color Analysis popular in Korea.
This script finds the average skin tone in an image, determines its complementary color, 
and then displays the original image alongside a block of the complementary color.

'''


def find_average_skin_tone(image_path):
    # Load image
    image = cv2.imread(image_path)
    
    # Convert to YCbCr color space
    ycbcr_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    
    # Define skin tone range in YCbCr
    min_YCrCb = np.array([0, 133, 77], np.uint8)
    max_YCrCb = np.array([255, 173, 127], np.uint8)
    
    # Find skin pixels
    skin_mask = cv2.inRange(ycbcr_image, min_YCrCb, max_YCrCb)
    skin_pixels = image[skin_mask == 255]
    
    # Calculate average color
    average_color = np.mean(skin_pixels, axis=0)
    
    return np.uint8(average_color)

def find_complementary_color(rgb_color):
    # Convert RGB to HSV
    hsv_color = cv2.cvtColor(np.uint8([[rgb_color]]), cv2.COLOR_RGB2HSV)
    
    # Adjust Hue to get the complementary color
    hsv_color[0][0][0] = (hsv_color[0][0][0] + 90) % 180  # Adjust if necessary
    
    # Convert back to RGB
    complementary_rgb = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2RGB)
    
    return complementary_rgb[0][0]

def display_image_with_complementary_color(image_path, complementary_color):
    # Load the original image
    original_image = cv2.imread(image_path)
    
    # Create a blank image with the same height as the original and double the width
    height, width, channels = original_image.shape
    new_image = np.zeros((height, 2*width, channels), np.uint8)
    
    # Fill the right half with the complementary color
    new_image[:, width:] = complementary_color
    
    # Copy the original image to the left half of the new image
    new_image[:, :width] = original_image
    
    # Display the result
    cv2.imshow("Original + Complementary Color", new_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = "/Users/jamieannemortel/Downloads/IMG_6440 (1).jpg"
    average_skin_tone = find_average_skin_tone(image_path)
    print("Average Skin Tone (RGB):", average_skin_tone)
    
    complementary_color = find_complementary_color(average_skin_tone)
    print("Complementary Color (RGB):", complementary_color)
    
    display_image_with_complementary_color(image_path, complementary_color)
