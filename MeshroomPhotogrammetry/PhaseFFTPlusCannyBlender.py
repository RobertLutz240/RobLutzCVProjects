import os
import numpy as np
import cv2
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
        output_path = os.path.join(output_folder, "blended_" + image_file)

        # Open image and convert to grayscale
        image = Image.open(image_path).convert("L")
        image_array = np.array(image)

        # --- FFT Phase-Only Reconstruction ---
        fft_result = np.fft.fft2(image_array)
        fft_shifted = np.fft.fftshift(fft_result)
        phase_only = np.exp(1j * np.angle(fft_shifted))
        reconstructed = np.fft.ifft2(np.fft.ifftshift(phase_only))
        fft_phase_image = np.abs(reconstructed)

        # Normalize FFT Phase-Only Image (0-255)
        fft_phase_image = (fft_phase_image / np.max(fft_phase_image) * 255).astype(np.uint8)

        # --- Canny Edge Detection ---
        edges = cv2.Canny(image_array, 50, 150)

        # --- Blend the Images ---
        blended = cv2.addWeighted(fft_phase_image, 0.9, edges, 0.1, 0)

        # Save blended image
        Image.fromarray(blended).save(output_path)

        print(f"Processed: {image_file} → {output_path}")

print("Blended images created successfully!")
