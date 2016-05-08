import sys
import cv2
import numpy as np

import pipeline

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

    return squares

def apply_per_square_and_recombine(bw, f):
    assert(bw.shape == (800,800))

    squares = apply_per_square(bw, f)

    rows = [ np.hstack(r) for r in squares ]
    return np.vstack(rows)

def count_white(bw):
    return cv2.countNonZero(bw[25:75,25:75])

def avg_center(bw):
    return np.mean(bw[40:60,40:60])


# Expects a 800x800 BW image.
def find_pieces(img):
    debug = True

    contours = apply_per_square_and_recombine(img, pipeline.get_contours)
    cv2.imshow("contours", contours)

    piece_mask = apply_per_square(contours, lambda x: count_white(x) > 20)
    average_centers = apply_per_square(img, avg_center)
    
    for i in xrange(0,8):
        for j in xrange (0,8):
            if piece_mask[i][j]:
                if average_centers[i][j] < 128:
                    sys.stdout.write("B ")
                else:
                    sys.stdout.write("W ")
            else:
                sys.stdout.write(". ")
        sys.stdout.write("\n")
    print ""

