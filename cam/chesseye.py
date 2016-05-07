import cv2
import sys
import numpy as np

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # We read from a pre-recorded video
        cap = cv2.VideoCapture(sys.argv[1])
    else:
        cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if not ret:
            # Video is over.
            break

        cv2.imshow("frame", frame)

    cap.release()
    cv2.destroyAllWindows()  
