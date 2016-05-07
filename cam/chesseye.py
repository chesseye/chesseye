import cv2
import sys
import numpy as np
import time

# All image transformations.
import pipeline

def now():
    millis = int(round(time.time() * 1000))
    return millis

# Applies a closure on all bw square sub-images, and returns the re-patched image.
def apply_per_square(bw, f):
    assert(bw.shape == (800,800))

    # i = 0, j = 0 = top left = a8 if board is straight
    squares = []
    for i in range(0,8):
        row = []
        for j in range(0,8):
            s = bw[(i*100):((i+1)*100),(j*100):((j+1)*100)]
            fs = f(s)
            row.append(fs)

        squares.append(row)

    rows = [ np.hstack(r) for r in squares ]
    return np.vstack(rows)

# Frame should be BW
def find_homography(frame):
    debug = True

    if debug:
        debug_frame = np.copy(frame)

    # Image dimensions. Not likely to change over time, but still.
    img_h, img_w = frame.shape[:2]
    img_max = max(img_h, img_w)
    img_min = min(img_h, img_w)

    # Minimum expected size of the board (arbitrary)
    min_board_size = 0.7 * img_min
    
    # Grayscale
    bw = pipeline.to_gray(frame)
    
    # Tracking features, hopefully finding lots of corners
    corners = pipeline.get_corners(bw, 100, min_board_size / 12)

    # Thresholded. The chessboard should be black/white after this step.
    binary = pipeline.binarize(bw, 0.2)
    # Edge detector.
    edges = cv2.Canny(binary, 100, 250, apertureSize = 3)
    # Thicker edges.
    thick_edges = cv2.dilate(edges, cv2.getStructuringElement(cv2.MORPH_CROSS,(4,4)))

    # Looking for lines now
    lines = cv2.HoughLines(thick_edges, 1, np.pi / 180, int(min_board_size))
    h_lines = []
    v_lines = []
    if lines is not None:
        lines = lines.reshape(-1, 2)
        for rho,theta in lines:
            is_v = False
            is_h = False
            a = np.cos(theta)
            # A value of `a` close to 1 or -1 means vertical
            # A value of `a` close to 0 means horizontal
            if abs(a) < 0.1:
                h_lines.append((rho,theta))
                is_h = True
            elif abs(1.0 - abs(a)) < 0.1:
                v_lines.append((rho,theta))
                is_v = True

            if debug:
                if is_v:
                    color = (0,255,0) # green
                elif is_h:
                    color = (0,255,0) # red
                else:
                    color = (80,80,80) # some gray

                (x1,y1),(x2,y2) = pipeline.hough_to_two_points(rho, theta)
                cv2.line(debug_frame,(x1,y1),(x2,y2),color,1)

    if h_lines and v_lines and corners:
        good_corners = []
        # Check all the ones close to a h_line
        is_on_h = np.array(False * len(corners), np.bool_)

        for rho,theta in h_lines:
            distances = pipeline.hough_dist(corners, rho, theta)
            close = distances < 5 # arbitrary
            is_on_h = np.bitwise_or(is_on_h, close)

        # Check all the ones close to a v_line
        is_on_v = np.array(False * len(corners), np.bool_)
        for rho,theta in v_lines:
            distances = pipeline.hough_dist(corners, rho, theta)
            close = distances < 5 # arbitrary
            is_on_v = np.bitwise_or(is_on_v, close)

        for i,(x,y) in enumerate(corners):
            if is_on_h[i] and is_on_v[i]:
                if debug:
                    cv2.circle(debug_frame, (x,y), 5, 255, -1)
                good_corners.append((x,y))
            else:
                if debug:
                    cv2.circle(debug_frame, (x,y), 5, 255)

        if good_corners:
            good_corners_xs, good_corners_ys = [ list(t) for t in zip(*good_corners) ]

            top_left = (min(good_corners_xs), min(good_corners_ys))
            bot_right = (max(good_corners_xs), max(good_corners_ys))

            dim1 = bot_right[0] - top_left[0]
            dim2 = bot_right[1] - top_left[1]
            ratio = float(dim1) / float(dim2)
    
            if ratio > 1.1 and ratio < 1.3:
                cv2.rectangle(frame, (min(good_corners_xs), min(good_corners_ys)), (max(good_corners_xs), max(good_corners_ys)), (0,0,255), 2)

                src_points = np.zeros((len(good_corners),1,2), np.float32)
                dst_points = np.zeros((len(good_corners),1,2), np.float32)

                for i,(x,y) in enumerate(good_corners):
                    src_points[i][0][0] = x
                    src_points[i][0][1] = y

                    xr = np.round(8.0 * float(x - top_left[0]) / float(dim1))
                    yr = np.round(8.0 * float(y - top_left[1]) / float(dim2)) 

                    dst_points[i][0][0] = xr * 100.0
                    dst_points[i][0][1] = yr * 100.0

                H, _ = cv2.findHomography(src_points, dst_points, cv2.LMEDS)
                # TODO check somehow that the homography is not completely bogus.

                if debug:
                    cv2.imshow("debug", debug_frame)
                return H

    if debug:
        cv2.imshow("debug", debug_frame)

    return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # We read from a pre-recorded video
        cap = cv2.VideoCapture(sys.argv[1])
    else:
        cap = cv2.VideoCapture(1)

    homography = None
    homography_ts = None

    while True:
        ret, frame = cap.read()

        # Press Q to quit, or when video is over.
        if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("frame", frame)

        if homography is None: # or now() - homography_ts > 5000:
            new_h = find_homography(frame)
            if new_h is not None:
                homography = new_h
                homography_ts = now()

        if homography is None:
            continue # We can't do anything until we have a lock on the board

        reproj = cv2.warpPerspective(frame, homography, (800, 800))
        bw_reproj = pipeline.to_gray(reproj)
        cv2.imshow("reproj", reproj)

        # equalized = apply_per_square(bw_reproj, lambda f: cv2.equalizeHist(f))
        equalized = cv2.equalizeHist(bw_reproj)
        cv2.imshow("equalized", equalized)

        # END OF WHILE LOOP

    cap.release()
    cv2.destroyAllWindows()  
