import cv2
import numpy as np

# Resizes an image so that it fits in the "box"
def resize_bounded(img, max_width, max_height):
    h, w = img.shape[:2]
    if w <= max_width and h <= max_height:
        return img


    f = min(float(max_height) / float(h), float(max_width) / float(w))
    print f
    return cv2.resize(img, (int(w * f), int(h * f)))


# Converts an image to grayscale.
def to_gray(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Converts to a color image
def to_color(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# Img should be BW
def get_corners(img, how_many, min_dist):
    # FIXME make sure the result stays a np.array throughout all uses.
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

# Distance between a set of points and a line in hough-transform coordinates
def hough_dist(points, rho, theta):
    # The idea is to rotate the set of points so that the line is vertical.
    # Distance is then read out as the absolute value of the horizontal
    # coordinate minus rho.

    rot_matrix = np.array([
        [ np.cos(-theta), -np.sin(-theta) ],
        [ np.sin(-theta),  np.cos(-theta) ]
    ], np.float64)

    point_matrix = np.array(points, np.float64)
    assert(point_matrix.shape == (len(points), 2))

    rotated_points = np.dot(rot_matrix, point_matrix.T)
    distances = np.abs(rotated_points.T[:, 0] - rho)

    return distances

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

def apply_clahe(img):
    median = cv2.medianBlur(img, 11)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(median)
    return cl

def apply_otsu(img):
    _,thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return thresh

# Img must be BW
def get_contours(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(img)
    edges = cv2.Canny(cl, 100, 250, apertureSize = 3)
    return edges
