import os
import cv2
import numpy as np


# ADJUST AS NEEDED
# Pixels per cm—measure.py will help
PX_PER_CM = 100
# Minimum area to display in square pixels
MIN_AREA = 10000


# Read the image
img = cv2.imread('images/data.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
# Apply adaptive thresholding to better handle variations in lighting
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                             cv2.THRESH_BINARY_INV, 21, 10)

# Clean up noise with morphological operations
kernel = np.ones((3,3), np.uint8)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# Find contours - use RETR_TREE to get hierarchical contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

result = img.copy()
text_positions = []

# First pass - draw all contours
for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)

    if area < MIN_AREA:  # Skip tiny contours
        continue
        
    # Get hierarchy info for this contour
    h = hierarchy[0][i]
    # h[2] is first child, h[3] is parent
    
    # Different colors for nested contours
    color = (0, 255, 0) if h[3] == -1 else (0, 0, 255)
    
    # Check if there's a child with similar area
    child_idx = h[2]
    skip = False
    while child_idx != -1:
        child_cnt = contours[child_idx]
        child_area = cv2.contourArea(child_cnt)
        if abs(area - child_area) < 10000:
            skip = True
            break
        child_idx = hierarchy[0][child_idx][0]  # Move to next sibling
    
    if skip:
        continue
        
    # Draw the contour
    cv2.drawContours(result, [cnt], -1, color, 2)
    
    # Calculate centroid
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])
    else:
        x, y = cnt[0][0]  # Fallback to first point if moments fail

    # Draw the text immediately after drawing contour
    text_color = (255, 0, 0) if h[3] == -1 else (255, 255, 0)
    
    # Calculate text position
    text_x = int(x)
    text_y = int(y)
    
    # Check for nearby text positions and adjust if needed
    while any(abs(text_y - pos[1]) < 20 and abs(text_x - pos[0]) < 100 for pos in text_positions):
        text_y += 20
    
    # Add position to list
    text_positions.append((text_x, text_y))
    
    area_cm2 = area / (PX_PER_CM * PX_PER_CM)
    cv2.putText(result, f'Area: {area_cm2:.3f} cm^2',
               (text_x, text_y - 20),
               cv2.FONT_HERSHEY_SIMPLEX,
               0.5, text_color, 2)

# Show results
os.makedirs('images', exist_ok=True)
cv2.imwrite('images/ellipses_detected.jpg', result)
cv2.imshow('Detected Ellipses', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
