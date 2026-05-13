import cv2
import numpy as np
import time

# ------------------------------------------------------------
# Helper functions
def preprocess(frame, blur_ksize=5):
    """Apply Gaussian blur and convert to HSV.
    Returns blurred frame and HSV image.
    """
    blurred = cv2.GaussianBlur(frame, (blur_ksize, blur_ksize), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    return blurred, hsv

# -------------------------------------------------
# Color masks
# -------------------------------------------------

def red_mask(hsv):
    """Return binary mask for red colors (both hue intervals)."""
    lower1 = np.array([0, 120, 70], dtype=np.uint8)
    upper1 = np.array([10, 255, 255], dtype=np.uint8)
    lower2 = np.array([170, 120, 70], dtype=np.uint8)
    upper2 = np.array([180, 255, 255], dtype=np.uint8)
    mask1 = cv2.inRange(hsv, lower1, upper1)
    mask2 = cv2.inRange(hsv, lower2, upper2)
    mask = cv2.bitwise_or(mask1, mask2)
    # Morphological cleaning
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)
    return mask


def blue_mask(hsv):
    """Return binary mask for blue colors."""
    lower = np.array([100, 150, 50], dtype=np.uint8)
    upper = np.array([140, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)
    return mask

# -------------------------------------------------
# Object detection (red & blue)
# -------------------------------------------------

def detect_target_objects(frame, hsv, min_area=500):
    """Detect red and blue objects, draw bounding boxes and label.
    Returns list of detections [(cx, cy, w, h, label)]."""
    detections = []
    # Red
    red = red_mask(hsv)
    contours, _ = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) < min_area:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy = x + w // 2, y + h // 2
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # green
        cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)  # blue centroid
        cv2.putText(frame, "Hedef Nesne", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        detections.append((cx, cy, w, h, "red"))
    # Blue
    blue = blue_mask(hsv)
    contours, _ = cv2.findContours(blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) < min_area:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy = x + w // 2, y + h // 2
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # blue box
        cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)  # green centroid
        cv2.putText(frame, "Hedef Nesne", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        detections.append((cx, cy, w, h, "blue"))
    return detections

# -------------------------------------------------
# Geometric area detection (equilateral triangle & hexagon)
# -------------------------------------------------

def is_equilateral(tri_pts, tolerance=0.15):
    """Check if three points form an approximately equilateral triangle.
    tolerance is relative difference allowed between longest and shortest side.
    """
    if len(tri_pts) != 3:
        return False
    # Compute side lengths
    pts = tri_pts.reshape((3, 2))
    a = np.linalg.norm(pts[0] - pts[1])
    b = np.linalg.norm(pts[1] - pts[2])
    c = np.linalg.norm(pts[2] - pts[0])
    sides = np.array([a, b, c])
    max_side = sides.max()
    min_side = sides.min()
    return (max_side - min_side) / max_side < tolerance


def detect_target_areas(frame, min_area=300):
    """Detect equilateral triangles and hexagons, draw and label.
    Returns list of detections [(cx, cy, label)]."""
    detections = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) < min_area:
            continue
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
        if len(approx) == 3:
            # Potential triangle – verify equilateral
            if is_equilateral(approx):
                M = cv2.moments(approx)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.drawContours(frame, [approx], -1, (0, 255, 255), 2)  # cyan
                    cv2.putText(frame, "Hedef Alan", (cx - 30, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
                    detections.append((cx, cy, "triangle"))
        elif len(approx) == 6:
            # Hexagon – assume valid if area is reasonable
            M = cv2.moments(approx)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.drawContours(frame, [approx], -1, (255, 255, 0), 2)  # light blue
                cv2.putText(frame, "Hedef Alan", (cx - 30, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                detections.append((cx, cy, "hexagon"))
    return detections

# -------------------------------------------------
# Main loop – video capture and FPS display
# -------------------------------------------------

def run():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    fps = 0.0
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame")
            break

        # Pre‑process
        blurred, hsv = preprocess(frame)

        # Detect coloured objects
        detect_target_objects(frame, hsv)

        # Detect geometric target areas
        detect_target_areas(frame)

        # FPS calculation
        cur_time = time.time()
        fps = 1.0 / (cur_time - prev_time)
        prev_time = cur_time
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow('Icaron UAV Vision', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
