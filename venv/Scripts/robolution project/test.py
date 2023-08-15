import cv2
import numpy as np

def calculate_angle(p1, p2, p3):
    vector1 = np.array([p1[0] - p2[0], p1[1] - p2[1]])
    vector2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
    dot_product = np.dot(vector1, vector2)
    magnitude_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    cos_angle = dot_product / magnitude_product
    angle_radians = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees

clicked_points = []

def eventclick(event, x, y, flags, params):
    global clicked_points

    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        print("Clicked points:", clicked_points)

cv2.namedWindow('video')
cv2.setMouseCallback('video', eventclick)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Draw lines on clicked points
    for point in clicked_points:
        cv2.circle(frame, point, radius=5, color=(0, 0, 255), thickness=-1)

    # Calculate and display angle if there are at least three clicked points
    if len(clicked_points) >= 3:
        angle = calculate_angle(clicked_points[-3], clicked_points[-2], clicked_points[-1])
        cv2.putText(frame, f"Angle: {angle:.2f} degrees", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()