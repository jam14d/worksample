import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = '/Users/jamieannemortel/Downloads/IMG_0365.jpg'
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Convert to HSV for color-based segmentation
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define a wider color range for the cat’s fur in HSV
# The hue range (0-180 in OpenCV) is adjusted to capture grayish to light brownish tones
# Adjust based on the specific fur color, expanding the range slightly
lower_color = np.array([0, 10, 40])  # Adjust lower limit to capture more hues and brightness
upper_color = np.array([40, 120, 255])  # Adjust upper limit to cover a broader range

# Create a color mask based on the broader HSV range
color_mask = cv2.inRange(hsv_image, lower_color, upper_color)

# Apply morphological operations to refine the mask
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, kernel)  # Close small gaps
color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_DILATE, kernel, iterations=3)  # Expand the mask further

# Find contours and select the largest contour (assuming it’s the cat)
contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if contours:  # Check if any contours are found
    largest_contour = max(contours, key=cv2.contourArea)

    # Create a refined mask for the cat based on the largest contour
    cat_mask = np.zeros_like(color_mask)
    cv2.drawContours(cat_mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
else:
    cat_mask = color_mask  # If no contours, fallback to original color mask

# Apply the cat mask to the RGB image to focus on the cat area only
cat_segmented = cv2.bitwise_and(image_rgb, image_rgb, mask=cat_mask)

# Step 2: Detect Gray Regions within the Segmented Cat Area
# Set tolerance for grayscale detection and brightness range
tolerance = 10          # How close R, G, and B values need to be to consider as gray
min_brightness = 50     # Minimum brightness to consider as gray
max_brightness = 200    # Maximum brightness to consider as gray

# Calculate brightness as the average of R, G, and B channels
brightness = np.mean(cat_segmented, axis=2)

# Detect gray regions based on RGB closeness and brightness within the cat mask
gray_mask = (np.abs(cat_segmented[:, :, 0] - cat_segmented[:, :, 1]) < tolerance) & \
            (np.abs(cat_segmented[:, :, 1] - cat_segmented[:, :, 2]) < tolerance) & \
            (brightness >= min_brightness) & (brightness <= max_brightness)

# Combine gray mask with cat mask to ensure we're analyzing only the cat area
gray_mask = gray_mask & (cat_mask > 0)

# Calculate gray area percentage within the cat area
gray_area = np.sum(gray_mask)
cat_area = np.sum(cat_mask > 0)
gray_percentage = (gray_area / cat_area) * 100 if cat_area > 0 else 0

# Create an overlay to visualize gray areas within the cat
overlay = cat_segmented.copy()
overlay[~gray_mask] = [255, 255, 255]  # Set non-gray areas to white for contrast

# Plot original, cat segmentation, and gray overlay
fig, axes = plt.subplots(1, 4, figsize=(20, 6))
axes[0].imshow(image_rgb)
axes[0].set_title("Original Image")
axes[0].axis("off")

axes[1].imshow(cat_segmented)
axes[1].set_title("Refined Segmented Cat Area")
axes[1].axis("off")

axes[2].imshow(color_mask, cmap="gray")
axes[2].set_title("Expanded Color Mask in HSV Space")
axes[2].axis("off")

axes[3].imshow(overlay)
axes[3].set_title("Gray Areas in Cat Coat")
axes[3].axis("off")

plt.suptitle(f"Gray Area in Cat Coat: {gray_percentage:.2f}% of the segmented area", fontsize=16)
plt.show()
