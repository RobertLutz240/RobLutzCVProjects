import cv2
import os
import numpy as np
from PIL import Image

# Set input/output directories
input_folder = r"C:\Users\Superleggera\Downloads"
output_folder = r"C:\Users\Superleggera\Desktop\dump"

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

# Process each image
for image_file in os.listdir(input_folder):
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
        image_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, "edge_" + image_file)

        # Open and convert image to grayscale
        image = Image.open(image_path).convert("L")
        image_array = np.array(image)

        # Apply Canny edge detection
        edges = cv2.Canny(image_array, 50, 150)

        # Save edge-detected image
        Image.fromarray(edges).save(output_path)

        print(f"Processed: {image_file} → {output_path}")

print("Edge detection applied to all images!")
