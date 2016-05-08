import cv2
import numpy as np

# Converts an image to grayscale.
def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Img should be BW
def get_corners(img, how_many, min_dist):
    ftt = cv2.goodFeaturesToTrack(img, how_many, 0.05, min_dist)

    if ftt is None:
        return []
    else:
        ftt = np.int0(ftt)
        return [ i.ravel() for i in ftt ]

# Img should be BW. Context_frac is the ratio of the minimal dimension that should be used
# as block size for the adaptive part.
def binarize(img, context_frac):
    h, w = img.shape[:2]
    m = float(min(h, w))
    block_size = int(m * context_frac)

    if block_size % 2 == 0:
        # blocksize needs to be odd (since the blocks are centered on the pixel)
        block_size += 1

    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, 2)

def single_hough_dist(x, y, rho, theta):
    R = np.array([
        [ np.cos(-theta), -np.sin(-theta) ],
        [ np.sin(-theta), np.cos(-theta) ]
    ], np.float64)

    xv1 = np.array([ x, y ], np.float64)

    xv2 = np.dot(R, xv1)

    return abs(xv2[0] - rho)

# Distance between a set of points and a line in hough-transform coordinates
def hough_dist(points, rho, theta):
    # idea is to rotate the set of points so that the line is vertical.
    # Distance is then read out as the absolute value of the horizontal
    # coordinate

    # PS: no idea why this doesn't work. Going point-by-point instead (see below)
    # rot_matrix = np.array([
    #     [ np.cos(-theta), -np.sin(-theta) ],
    #     [ np.sin(-theta),  np.cos(-theta) ]
    # ], np.float64)

    # point_matrix = np.array(points, np.float64)
    # assert(point_matrix.shape == (len(points), 2))

    # rotated_points = np.dot(rot_matrix, point_matrix.T)
    # distances = np.abs(rotated_points.T[:, 1] - rho)
    # return distances

    # return distances
    return np.array([ single_hough_dist(x,y,rho,theta) for (x,y) in points ], np.float64)
        
def hough_to_two_points(rho, theta):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    
    return ((x1,y1),(x2,y2))

# Img must be BW
def get_contours(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(img)
    edges = cv2.Canny(cl, 100, 250, apertureSize = 3)
    return edges
