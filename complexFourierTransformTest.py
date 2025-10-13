import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Correct file path handling
image_path = r"C:\Users\Superleggera\Desktop\dump\edge_20240531_141538.jpg"

# Open image and convert to grayscale
image = Image.open(image_path).convert("L")
image_array = np.array(image)

# Compute 2D FFT and shift zero frequency to the center
fft_result = np.fft.fft2(image_array)
fft_shifted = np.fft.fftshift(fft_result)

# Extract Magnitude and Phase
magnitude = np.abs(fft_shifted)  # Magnitude spectrum
phase = np.angle(fft_shifted)    # Phase spectrum

# User Selection
print("Choose an option:")
print("1 - Display Magnitude & Phase Spectra")
print("2 - Reconstruct Image from Magnitude Only")
print("3 - Reconstruct Image from Phase Only")
print("4 - Print FFT Coefficients")
choice = input("Enter the number of your choice: ")

if choice == "1":
    # Display the magnitude and phase spectra
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(np.log(1 + magnitude), cmap="gray")
    plt.title("Magnitude Spectrum")
    plt.colorbar()

    plt.subplot(1, 2, 2)
    plt.imshow(phase, cmap="gray")
    plt.title("Phase Spectrum")
    plt.colorbar()

    plt.show()

elif choice == "2":
    # Reconstruct image using only magnitude
    reconstructed = np.fft.ifft2(np.fft.ifftshift(magnitude * np.exp(1j * np.zeros_like(phase))))
    reconstructed_image = np.abs(reconstructed)

    # Display reconstructed image
    plt.imshow(reconstructed_image, cmap="gray")
    plt.title("Reconstructed Image (Magnitude Only)")
    plt.show()

elif choice == "3":
    # Reconstruct image using only phase
    reconstructed = np.fft.ifft2(np.fft.ifftshift(np.exp(1j * phase)))
    reconstructed_image = np.abs(reconstructed)

    # Display reconstructed image
    plt.imshow(reconstructed_image, cmap="gray")
    plt.title("Reconstructed Image (Phase Only)")
    plt.show()

elif choice == "4":
    # Print a small section of FFT coefficients
    print("Sample FFT Coefficients (Complex Values):")
    print(fft_shifted[:5, :5])  # Print a small 5x5 section

else:
    print("Invalid choice. Please enter 1, 2, 3, or 4.")
