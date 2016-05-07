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
