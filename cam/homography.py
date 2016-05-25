import cv2
import numpy as np
import random

import pipeline
import pieces

def r():
    return int(random.uniform(10000, 99999))

# M must be a n x m boolean matrix.
def covering_rows(M):
    rows = [ 1 ]
    mask = M[0]

    for i in xrange(1, M.shape[0]):
        new_mask = np.logical_or(mask, M[i])
        if not np.array_equal(mask, new_mask):
            rows.append(i)
        mask = new_mask

    return M[np.array(rows),:]

# http://stackoverflow.com/a/16973510/358642
def unique_rows(M):
    N = np.ascontiguousarray(M).view(np.dtype((np.void, M.dtype.itemsize * M.shape[1])))
    _, idx = np.unique(N, return_index=True)
    return M[idx]

# Takes a set of points and two sets of lines. Filters out every point that is
# not on one line from each set, and return a mapping from the remaining point to a line id.
def filter_corner_and_lines(corners, h_lines, v_lines, max_dist):
    if not corners or len(corners) < 3 or not h_lines or len(h_lines) < 2 or not v_lines or len(v_lines) < 2:
        return None

    # Matrices storing the distances between every line and every point.
    h_dists = np.vstack([ pipeline.hough_dist(corners, rho, theta) for rho,theta in h_lines ])
    v_dists = np.vstack([ pipeline.hough_dist(corners, rho, theta) for rho,theta in v_lines ])

    # Matrices storing which points are considered "close" to each line.
    h_close = h_dists <= max_dist
    v_close = v_dists <= max_dist

    # Counts the number of lines to which each point is close.
    h_points_to_lines = np.sum(h_close, axis=0) > 0
    v_points_to_lines = np.sum(v_close, axis=0) > 0
    # Points that are at intersections.
    points_at_inter = np.logical_and(h_points_to_lines, v_points_to_lines)

    print "there are %d points on intersections." % np.sum(points_at_inter)

    print "BEFORE"
    print h_close.shape
    print v_close.shape

    # We recompute distances with more slack, and only for points that were on intersections
    h_close = h_dists[:, points_at_inter] <= (2 * max_dist)
    v_close = v_dists[:, points_at_inter] <= (2 * max_dist)

    # We drop lines with a single point.
    h_close = h_close[np.sum(h_close, axis=1) > 1, :]
    v_close = v_close[np.sum(v_close, axis=1) > 1, :]
    # We deduplicate rows
    h_close = unique_rows(h_close)
    v_close = unique_rows(v_close)
    print "AFTER"
    print h_close.shape
    print v_close.shape

    return None

# Returns a homography to project onto a 800x800 image.
def find_homography(frame, debug=False):
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
    # FIXME check constants? which ones depend on image size?
    edges = cv2.Canny(binary, 100, 250, apertureSize = 3) 

    # Thicker edges.
    # FIXME depends on image size?
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
                    color = (0,255,0) # also green
                else:
                    color = (80,80,80) # some gray

                (x1,y1),(x2,y2) = pipeline.hough_to_two_points(rho, theta)
                cv2.line(debug_frame,(x1,y1),(x2,y2),color,1)

    # Not ready for prime time
    filter_corner_and_lines(corners, h_lines, v_lines, 4)

    if h_lines and v_lines and corners:
        good_corners = []

        all_h_dists = np.vstack([ pipeline.hough_dist(corners, rho, theta) for rho,theta in h_lines ])
        all_v_dists = np.vstack([ pipeline.hough_dist(corners, rho, theta) for rho,theta in v_lines ])

        # FIXME should really depend on size of image
        all_h_close = all_h_dists < 5
        all_v_close = all_v_dists < 5

        all_h_agg = np.sum(all_h_close, axis=0)
        all_v_agg = np.sum(all_v_close, axis=0)

        is_at_inter = (all_h_agg * all_v_agg) > 0

        for i,(x,y) in enumerate(corners):
            if is_at_inter[i]:
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
    
            if ratio > 0.8 and ratio < 1.2:
                if debug:
                    cv2.rectangle(debug_frame, (min(good_corners_xs), min(good_corners_ys)), (max(good_corners_xs), max(good_corners_ys)), (0,0,255), 2)

                src_points = np.zeros((len(good_corners),1,2), np.float32)
                dst_points = np.zeros((len(good_corners),1,2), np.float32)

                for i,(x,y) in enumerate(good_corners):
                    src_points[i][0][0] = x
                    src_points[i][0][1] = y

                    xr = np.round(8.0 * float(x - top_left[0]) / float(dim1))
                    yr = np.round(8.0 * float(y - top_left[1]) / float(dim2)) 

                    dst_points[i][0][0] = xr
                    dst_points[i][0][1] = yr

                H, _ = cv2.findHomography(src_points, dst_points * 100.0, cv2.LMEDS)
                # TODO check somehow that the homography is not completely bogus.

                if debug:
                    cv2.imshow("debug-%d" % r(), debug_frame)
                return H

    if debug:
        cv2.imshow("debug", debug_frame)

    return None

def check_homography(img, H):
    bw = pipeline.to_gray(img)
    reproj = cv2.warpPerspective(bw, H, (800, 800))
    binary = pipeline.binarize(reproj, 0.2)
    cv2.imshow("binarized-%d" % r(), binary)
