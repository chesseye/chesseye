import cv2
import sys
import numpy as np
import time
import json

# All image transformations.
import pipeline
import homography
import pieces

def now():
    millis = int(round(time.time() * 1000))
    return millis

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # We read from a pre-recorded video
        cap = cv2.VideoCapture(sys.argv[1])
    else:
        cap = cv2.VideoCapture(1)

    # The homography
    H = None
    H_ts = None

    while True:
        ret, frame = cap.read()

        # Press Q to quit, or when video is over.
        if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("frame", frame)

        if H is None:
            new_h = homography.find_homography(frame)
            if new_h is not None:
                H = new_h
                H_ts = now()

        if H is None:
            # We can't do anything until we have a lock on the board
            continue

        # Reprojecting to get a nice square
        reproj = cv2.warpPerspective(frame, H, (800, 800))
        bw_reproj = pipeline.to_gray(reproj)

        # Some lame attempt at sharpening.
        blurred = cv2.GaussianBlur(bw_reproj, (0,0), 3)
        sharp = cv2.addWeighted(bw_reproj, 1.5, blurred, -0.5, 0)

        masks = pieces.find_pieces(sharp)

        if pieces.sanity_check(masks):
            print "MASK %s" % pieces.masks_to_string(masks)
            sys.stdout.flush()
        else:
            print "OBST"
            sys.stdout.flush()

        feedback = pipeline.to_color(sharp)

        if pieces.sanity_check(masks):
            pieces.draw_pieces(feedback, masks)

        cv2.imshow("feedback", feedback)
        # END OF WHILE LOOP

    cap.release()
    cv2.destroyAllWindows()  
