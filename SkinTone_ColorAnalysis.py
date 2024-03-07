import cv2
import numpy as np

def adjust_hue(hue, amount):
    return (hue + amount) % 180

def create_skin_mask(image_path):
    image = cv2.imread(image_path)
    original_image = image.copy()

    # Face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        face_img = image[y:y+h, x:x+w]
        ycrcb_image = cv2.cvtColor(face_img, cv2.COLOR_BGR2YCrCb)
        min_YCrCb = np.array([0, 133, 77], np.uint8)
        max_YCrCb = np.array([255, 173, 127], np.uint8)
        mask = cv2.inRange(ycrcb_image, min_YCrCb, max_YCrCb)

        # Apply morphological operations
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=1)
        mask = cv2.erode(mask, kernel, iterations=2)

        # Find the largest contour as the main face region
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            mask = np.zeros_like(mask)
            cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)

        skin = cv2.bitwise_and(face_img, face_img, mask=mask)
        mask_bool = mask.astype(bool)
        skin_pixels = face_img[mask_bool]

        # Compute the average color of skin pixels
        if skin_pixels.size == 0:
            continue
        average_color = np.mean(skin_pixels, axis=0).astype(np.uint8)
        print("Average skin color (BGR):", average_color)

        average_color_hsv = cv2.cvtColor(np.uint8([[average_color]]), cv2.COLOR_BGR2HSV)[0][0]
        complementary_hue = adjust_hue(average_color_hsv[0], 90)
        analogous_hue1 = adjust_hue(average_color_hsv[0], 30)
        analogous_hue2 = adjust_hue(average_color_hsv[0], -30)
        triadic_hue1 = adjust_hue(average_color_hsv[0], 120)
        triadic_hue2 = adjust_hue(average_color_hsv[0], -120)

        # Create images for each color harmony
        complementary_color = cv2.cvtColor(np.uint8([[[complementary_hue, average_color_hsv[1], average_color_hsv[2]]]]), cv2.COLOR_HSV2BGR)[0][0]
        analogous_color1 = cv2.cvtColor(np.uint8([[[analogous_hue1, average_color_hsv[1], average_color_hsv[2]]]]), cv2.COLOR_HSV2BGR)[0][0]
        analogous_color2 = cv2.cvtColor(np.uint8([[[analogous_hue2, average_color_hsv[1], average_color_hsv[2]]]]), cv2.COLOR_HSV2BGR)[0][0]
        triadic_color1 = cv2.cvtColor(np.uint8([[[triadic_hue1, average_color_hsv[1], average_color_hsv[2]]]]), cv2.COLOR_HSV2BGR)[0][0]
        triadic_color2 = cv2.cvtColor(np.uint8([[[triadic_hue2, average_color_hsv[1], average_color_hsv[2]]]]), cv2.COLOR_HSV2BGR)[0][0]

        print("Complementary Color (BGR):", complementary_color)
        print("Analogous Colors (BGR):", analogous_color1, analogous_color2)
        print("Triadic Colors (BGR):", triadic_color1, triadic_color2)

    # Display
    cv2.imshow('Original Image', original_image)
    cv2.imshow('Skin Detection Result', skin)
    cv2.imshow('Complementary Color', np.full((100, 100, 3), complementary_color, np.uint8))
    cv2.imshow('Analogous Color 1', np.full((100, 100, 3), analogous_color1, np.uint8))
    cv2.imshow('Analogous Color 2', np.full((100, 100, 3), analogous_color2, np.uint8))
    cv2.imshow('Triadic Color 1', np.full((100, 100, 3), triadic_color1, np.uint8))
    cv2.imshow('Triadic Color 2', np.full((100, 100, 3), triadic_color2, np.uint8))

    cv2.waitKey(0)
    cv2.destroyAllWindows()

create_skin_mask('/Users/jamieannemortel/Desktop/dicaprio_33418505_ver1.0.webp')
