import numpy as np
import pandas as pd
import math

def generate_brain_contours(z_slices, radius, points_per_contour):
    """
    Generates circular contours to represent brain slices.
    """
    data = []
    for z in range(z_slices):
        for i in range(points_per_contour):
            angle = 2 * math.pi * i / points_per_contour
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            data.append([5, z + 1, x, y, z, 0, 1, z + 1])  # Type 5 for contour points
    return data

def generate_random_points(z_slices, num_points, x_range, y_range):
    """
    Generates random points within each slice to simulate cell types and positions.
    """
    data = []
    for z in range(z_slices):
        for _ in range(num_points):
            x = np.random.uniform(-x_range, x_range)
            y = np.random.uniform(-y_range, y_range)
            cell_type = np.random.randint(1, 5)  # Random cell type between 1 and 4
            data.append([cell_type, z + 1, x, y, z, 1, 0, 0])  # Normal points
    return data

# Parameters
z_slices = 10
radius = 1000
points_per_contour = 20
num_points = 50
x_range, y_range = 800, 800

# Generate data
contour_data = generate_brain_contours(z_slices, radius, points_per_contour)
point_data = generate_random_points(z_slices, num_points, x_range, y_range)

# Combine and create DataFrame
complete_data = contour_data + point_data
df = pd.DataFrame(complete_data, columns=['Type', 'Slice', 'X', 'Y', 'Z', 'isPoint', 'isContour', 'contourID'])

# Save to CSV
df.to_csv('simulated_brain_data.csv', index=False)

print("Data generated")