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
