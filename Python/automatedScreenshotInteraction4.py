import pytesseract
from PIL import Image, ImageDraw, ImageFont
import pyautogui
import cv2
import numpy as np

# Define the function to get the screenshot and convert it for OpenCV
def get_screenshot():
    # Set up Tesseract OCR path (adjust for your system)
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # Take a screenshot using pyautogui
    screenshot = pyautogui.screenshot()
    # Convert the screenshot to a numpy array
    
    data = pytesseract.image_to_data(screenshot, lang="eng", output_type=pytesseract.Output.DICT)
    # Create a draw object to overlay text
    draw = ImageDraw.Draw(screenshot)
    font = ImageFont.load_default()  # Use a default font

    # Iterate over detected text data
    for i in range(len(data["text"])):
        if int(data["conf"][i]) > 50:  # Confidence threshold to filter noise
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            text = data["text"][i]

        # Draw a rectangle around the detected text
            draw.rectangle([x, y, x + w, y + h], outline="red", width=2)

        # Overlay the text
            draw.text((x, y - 10), text, fill="blue", font=font)
    frame = np.array(screenshot)
    # Convert RGB to BGR (OpenCV uses BGR format)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame

# Main loop to display the "desktop capture"
while True:
    # Get the current frame
    cam = get_screenshot()
    # Display the frame
    cv2.imshow("Desktop View", cam)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()