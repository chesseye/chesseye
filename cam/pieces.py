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
# Returns a dictionary with two, two-dimensional, boolean arrays:
# {
#    "white": [ ... ]
#    "black": [ ... ]
# }
# The positions are enumerated by A-file first, 1st to 8th rank, so:
# a1, a2, a3... a8, b1, ... b8, c1, ... h8
def find_pieces(img):
    debug = True

    contours = apply_per_square_and_recombine(img, pipeline.get_contours)

    piece_mask = apply_per_square(contours, lambda x: count_white(x) > 20)
    average_centers = apply_per_square(img, avg_center)

    white_mask = []
    black_mask = []
    for i in xrange(0,8):
        for j in xrange (0,8):
            if piece_mask[7-i][7-j]:
                if average_centers[7-i][7-j] < 128:
                    white_mask.append(False)
                    black_mask.append(True)
                else:
                    white_mask.append(True)
                    black_mask.append(False)
            else:
                white_mask.append(False)
                black_mask.append(False)

    return {
        "white": white_mask,
        "black": black_mask
    }


# Return False if the masks are obviously not from a valid position (likely to be from
# camera obstruction)
def sanity_check(masks):
    count = lambda l: sum(map(lambda p: 1 if p else 0, l))

    total_white = count(masks["white"])
    total_black = count(masks["black"])

    # arbitrary criterion for now
    return total_white < 20 and total_black < 20 and (total_white + total_black < 37)

def masks_to_string(masks):
    stringify = lambda l: "".join(map(lambda p: "1" if p else "0", l))

    return stringify(masks["white"]) + stringify(masks["black"])

# Img should be 800x800 and color
def draw_pieces(img, masks):
    for i in xrange(0,8):
        for j in xrange(0,8):
            c = 8*i + j

            x = 700 - (100*j)
            y = 700 - (100*i)

            if masks["white"][c]:
                cv2.rectangle(img, (x+10,y+10), (x+90,y+90), (255,0,0), 2)
            elif masks["black"][c]:
                cv2.rectangle(img, (x+10,y+10), (x+90,y+90), (0,0,255), 2)

