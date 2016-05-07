import cv2
import sys
import numpy as np

# All image transformations.
import pipeline

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # We read from a pre-recorded video
        cap = cv2.VideoCapture(sys.argv[1])
    else:
        cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Press Q to quit, or when video is over.
        if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Image dimensions. Not likely to change over time, but still.
        img_h, img_w = frame.shape[:2]
        img_max = max(img_h, img_w)
        img_min = min(img_h, img_w)

        # Minimum expected size of the board (arbitrary)
        min_board_size = 0.7 * img_min

        # Grayscale version
        bw = pipeline.to_gray(frame)
        cv2.imshow("bw", bw)

        # Tracking features, hopefully finding lots of corners
        corners = pipeline.get_corners(bw, 100, min_board_size / 12)
        if corners:
            for x,y in corners:
                cv2.circle(frame, (x,y), 5, 255, -1) 

        cv2.imshow("frame", frame)

    cap.release()
    cv2.destroyAllWindows()  
