import cv2
import numpy as np

print(cv2.__version__)

width = 1280
height = 720

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

# Initialize previous frame for motion differencing
ret, prev_frame = cam.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Create a black canvas for motion trails (floating point for decay effect)
trail_canvas = np.zeros_like(prev_frame, dtype=np.float32)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # --- Motion Detection ---
    diff = cv2.absdiff(prev_gray, gray)
    _, motion_mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # --- Edge Detection ---
    edges = cv2.Canny(gray, 80, 200)

    # --- Enhance Neon Effect ---
    edges_dilated = cv2.dilate(edges, None, iterations=1)
    edges_blurred = cv2.GaussianBlur(edges_dilated, (7, 7), 0)

    # Combine edges with motion mask
    neon_mask = cv2.bitwise_and(edges_blurred, motion_mask)

    # Apply color map for neon glow
    neon_colored = cv2.applyColorMap(neon_mask, cv2.COLORMAP_HOT)  # Try JET, INFERNO, etc.

    # --- Motion Trail Accumulation ---
    # Add new neon to trail canvas
    cv2.accumulateWeighted(neon_colored, trail_canvas, 0.2)  # Adjust alpha for trail persistence
    trail_display = cv2.convertScaleAbs(trail_canvas)

    # Show combined result
    cv2.imshow('Neon Motion Trails', trail_display)
    cv2.moveWindow('Neon Motion Trails', 0, 0)

    # Update previous frame
    prev_gray = gray.copy()

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
