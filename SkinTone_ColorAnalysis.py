import cv2
import numpy as np

'''
IN PROGRESS

A simple, fun project inspired by the trend of Personal Color Analysis popular in Korea.

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

    mask_bool = skin_mask.astype(bool)
    skin_pixels = image[mask_bool]

    # Compute the average color of skin pixels
    average_color = np.mean(skin_pixels, axis=0).astype(np.uint8)
    print("Average skin color (BGR):", average_color)

    # Convert average skin color to HSV
    average_color_hsv = cv2.cvtColor(np.uint8([[average_color]]), cv2.COLOR_BGR2HSV)[0][0]

    # Function to adjust hue value
    def adjust_hue(hue, amount):
        return (hue + amount) % 180

    # Calculate complementary, analogous, and triadic colors in HSV
    complementary_hue = adjust_hue(average_color_hsv[0], 90)  # 180 degrees opposite on the color wheel, using 90 for simplicity in HSV
    analogous_hue1 = adjust_hue(average_color_hsv[0], 30)  # 30 degrees apart
    analogous_hue2 = adjust_hue(average_color_hsv[0], -30) # -30 degrees apart
    triadic_hue1 = adjust_hue(average_color_hsv[0], 120)  # 120 degrees apart
    triadic_hue2 = adjust_hue(average_color_hsv[0], -120) # -120 degrees apart

    # Create images for each color harmony
    complementary_color = cv2.cvtColor(np.uint8([[[complementary_hue, average_color_hsv[1], average_color_hsv[2]]]]), cv2.COLOR_HSV2BGR)[0][0]
    analogous_color1 = cv2.cvtColor(np.uint8([[[analogous_hue1, average_color_hsv[1], average_color_hsv[2]]]]), cv2.COLOR_HSV2BGR)[0][0]
    analogous_color2 = cv2.cvtColor(np.uint8([[[analogous_hue2, average_color_hsv[1], average_color_hsv[2]]]]), cv2.COLOR_HSV2BGR)[0][0]
    triadic_color1 = cv2.cvtColor(np.uint8([[[triadic_hue1, average_color_hsv[1], average_color_hsv[2]]]]), cv2.COLOR_HSV2BGR)[0][0]
    triadic_color2 = cv2.cvtColor(np.uint8([[[triadic_hue2, average_color_hsv[1], average_color_hsv[2]]]]), cv2.COLOR_HSV2BGR)[0][0]

    print("Complementary Color (BGR):", complementary_color)
    print("Analogous Colors (BGR):", analogous_color1, analogous_color2)
    print("Triadic Colors (BGR):", triadic_color1, triadic_color2)

    # Display the original image, the mask, the detected skin, and color harmonies
    cv2.imshow('Original Image', image)
    cv2.imshow('Skin Mask', skin_mask)
    cv2.imshow('Skin Detection Result', skin)
    cv2.imshow('Complementary Color', np.full((100, 100, 3), complementary_color, np.uint8))
    cv2.imshow('Analogous Color 1', np.full((100, 100, 3), analogous_color1, np.uint8))
    cv2.imshow('Analogous Color 2', np.full((100, 100, 3), analogous_color2, np.uint8))
    cv2.imshow('Triadic Color 1', np.full((100, 100, 3), triadic_color1, np.uint8))
    cv2.imshow('Triadic Color 2', np.full((100, 100, 3), triadic_color2, np.uint8))

    cv2.waitKey(0)
    cv2.destroyAllWindows()

create_skin_mask('/Users/jamieannemortel/Desktop/main-qimg-134e3bf89fff27bf56bdbd04e7dbaedf.webp')
