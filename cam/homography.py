import cv2
import numpy as np
import random

import pipeline
import pieces

def r():
    return int(random.uniform(10000, 99999))


def draw_line_from_vector_and_point(img, quadruple, color):
    vx = quadruple[0]
    vy = quadruple[1]
    x0 = quadruple[2]
    y0 = quadruple[3]

    x1 = x0 + 1000.0 * vx
    y1 = y0 + 1000.0 * vy
    x2 = x0 - 1000.0 * vx
    y2 = y0 - 1000.0 * vy

    cv2.line(img,(x1,y1),(x2,y2),color,1)

def intersects_from_vector_and_point(quadruple):
    vx = quadruple[0]
    vy = quadruple[1]
    x0 = quadruple[2]
    y0 = quadruple[3]

    return (x0 - (y0 * vx / vy), y0 - (x0 * vy / vx))

# Takes a set of points and two sets of lines. Filters out every point that is
# not on one line from each set, and return a mapping from the remaining point to a line id.
def filter_corner_and_lines(corners, h_lines, v_lines, max_dist):
    if not corners or len(corners) < 3 or not h_lines or len(h_lines) < 2 or not v_lines or len(v_lines) < 2:
        return None

    # num(corners) * 2 matrix with x,y coords.
    points = np.array(corners, np.float64)
    assert(points.shape == (len(corners), 2))

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

    # Let's group vertically/horizontally aligned points into classes.
    h_classes = []
    for i in xrange(0, h_close.shape[1]):
        h_l_is = h_close[:,i] # A column indicating which lines are close.
        h_l_s = h_close[h_l_is, :] # All rows for lines to which point is close
        companions = np.nonzero(np.any(h_l_s, axis=0))[0]
        if companions.size > 1 and i == np.min(companions):
            h_classes.append({ "point_ids": companions.tolist() })

    v_classes = []
    for i in xrange(0, v_close.shape[1]):
        v_l_is = v_close[:,i] # A column indicating which lines are close.
        v_l_s = v_close[v_l_is, :] # All rows for lines to which point is close
        companions = np.nonzero(np.any(v_l_s, axis=0))[0]
        if companions.size > 1 and i == np.min(companions):
            v_classes.append({ "point_ids": companions.tolist() })

    def line_from_point_ids(point_ids):
        class_points = points[np.array(point_ids), :]
        return cv2.fitLine(class_points, cv2.DIST_L2, 0, 0.01, 0.01)

    for k in h_classes:
        l = line_from_point_ids(k["point_ids"])
        _, yi = intersects_from_vector_and_point(l)
        k["interpolated"] = l
        k["y_intersect"] = yi

    for k in v_classes:
        l = line_from_point_ids(k["point_ids"])
        xi, _ = intersects_from_vector_and_point(l)
        k["interpolated"] = l
        k["x_intersect"] = xi

    h_classes.sort(key=lambda e: e["y_intersect"])
    v_classes.sort(key=lambda e: e["x_intersect"])

    h_assignment = {}
    v_assignment = {}

    for i, k in enumerate(h_classes):
        for pid in k["point_ids"]:
            h_assignment[pid] = i

    for i, k in enumerate(v_classes):
        for pid in k["point_ids"]:
            v_assignment[pid] = i

    return (h_assignment, v_assignment, h_classes, v_classes)

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
                if is_v or is_h:
                    color = (80,80,80) # some gray

                (x1,y1),(x2,y2) = pipeline.hough_to_two_points(rho, theta)
                cv2.line(debug_frame,(x1,y1),(x2,y2),color,1)

    # work in progress
    if h_lines and v_lines and corners:
        h_assignment, v_assignment, h_classes, v_classes = filter_corner_and_lines(corners, h_lines, v_lines, 4)
        num_h_classes = len(h_classes)
        num_v_classes = len(v_classes)

        if debug:
            for k in v_classes:
                draw_line_from_vector_and_point(debug_frame, k["interpolated"], (0,255,0))
                cv2.circle(debug_frame, (k["x_intersect"],0), 5, (0,0,255), -1)
            for k in h_classes:
                draw_line_from_vector_and_point(debug_frame, k["interpolated"], (0,255,0))
                cv2.circle(debug_frame, (0,k["y_intersect"]), 5, (0,255,0), -1)

        if num_h_classes < 8 or num_h_classes > 9 or num_v_classes < 8 or num_v_classes > 9:
            return None

        picked_corners = [ i for i,(x,y) in enumerate(corners) if i in h_assignment and i in v_assignment ]

        if debug:
            for i,(x,y) in enumerate(corners):
                if i in picked_corners:
                    cv2.circle(debug_frame, (x,y), 5, 255, -1)
                else:
                    cv2.circle(debug_frame, (x,y), 5, 255)

        src_points = np.zeros((len(picked_corners),1,2), np.float32)
        dst_points = np.zeros((len(picked_corners),1,2), np.float32)

        for j,i in enumerate(picked_corners):
            x = corners[i][0]
            y = corners[i][1]

            src_points[j][0][0] = x
            src_points[j][0][1] = y

            dst_points[j][0][0] = v_assignment[i] + (9 - num_v_classes) # FIXME
            dst_points[j][0][1] = h_assignment[i] + (9 - num_h_classes) # Complete Hack

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

def draw_reprojected_chessboard(img, H, color=(0,255,0), thickness=1):
    """Inverts the homography to display the image with the reprojected chessboard outline."""
    invertible, Hinv = cv2.invert(H)
    assert(invertible)

    for i in xrange(0,9):
        points = np.array([
            [       0.0, i * 100.0, 1.0 ],
            [     800.0, i * 100.0, 1.0 ],
            [ i * 100.0,       0.0, 1.0 ],
            [ i * 100.0,     800.0, 1.0 ]
        ], np.float64)

        bpc = np.dot(points, Hinv.T)

        # Convert back from homogeneous to cartesian
        n = np.divide(bpc, bpc[:,2].reshape(-1,1)).astype(int)

        cv2.line(img, (n[0][0], n[0][1]), (n[1][0], n[1][1]), color, thickness)
        cv2.line(img, (n[2][0], n[2][1]), (n[3][0], n[3][1]), color, thickness)

