import os
import cv2
import numpy as np

drawing = False
points = []
img_copy = None

def draw_line(event, x, y, flags, param):
    global drawing, points, img_copy
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points = [(x, y)]
        img_copy = img.copy()
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.line(img_copy, points[0], (x,y), (0,255,0), 2)
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        points.append((x,y))
        
        # Calculate length
        length = np.sqrt((points[1][0] - points[0][0])**2 + 
                        (points[1][1] - points[0][1])**2)
        
        # Draw final line and length
        cv2.line(img, points[0], points[1], (0,255,0), 2)
        mid_point = (int((points[0][0] + points[1][0])/2), 
                    int((points[0][1] + points[1][1])/2))
        cv2.putText(img, f'{length:.1f} px', mid_point,
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

# Read image
img = cv2.imread('images/data.jpg')
cv2.namedWindow('Draw Lines')
cv2.setMouseCallback('Draw Lines', draw_line)

# Main loop
while True:
    cv2.imshow('Draw Lines', img_copy if drawing else img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

os.makedirs('images', exist_ok=True)
cv2.imwrite('images/measured_lines.jpg', img)
cv2.destroyAllWindows()
