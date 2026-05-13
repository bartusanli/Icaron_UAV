import cv2
import numpy as np
import imutils
def red_mask(image):
    """
    Return a binary mask where only *definitely red* pixels are white.
    Uses two HSV hue intervals to avoid white/bright regions.
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Red hue spans the hue circle boundary, so we need two ranges.
    lower_red1 = np.array([0, 120, 70], dtype=np.uint8)
    upper_red1 = np.array([10, 255, 255], dtype=np.uint8)
    lower_red2 = np.array([170, 120, 70], dtype=np.uint8)
    upper_red2 = np.array([180, 255, 255], dtype=np.uint8)

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Clean up small noise
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    return mask


def main():
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        # Generate mask for current frame
        mask = red_mask(frame)

        # Find contours of red regions (definitely red)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Define minimum area to consider a region as a target (adjust as needed)
        min_area = 500

        # Iterate over contours and draw bounding boxes around confident red targets
        for cnt in contours:
            if cv2.contourArea(cnt) >= min_area:
                x, y, w, h = cv2.boundingRect(cnt)
                # Draw rectangle on original frame
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Compute centroid for guidance
                cx = x + w // 2
                cy = y + h // 2
                # Mark centroid
                cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)
                # Print target coordinates (could be sent to drone controller)
                print(f"Target at ({cx}, {cy}) with size ({w}x{h})")

        # Show original frame and mask side-by-side
        cv2.imshow('Original', frame)
        cv2.imshow('Red Mask', mask)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
