import cv2
import json
import numpy as np
import os
import random
import unittest

import homography
import pipeline

class HomographyTests(unittest.TestCase):
    def r(self):
        return int(random.uniform(100000, 999999))

    def setUp(self):
        # Loads the test (meta)data.
        here = os.path.dirname(os.path.abspath(__file__))
        test_images_dir = os.path.join(here, "../test-frames")

        with open("%s/data.json" % test_images_dir) as fp:
            self.test_data = json.load(fp)

        # Makes paths to images absolute.
        for i in xrange(0, len(self.test_data)):
            self.test_data[i]["filename"] = os.path.join(test_images_dir, self.test_data[i]["filename"])

    def test_homography(self):
        for d in self.test_data:
            fn = d["filename"]
            img = cv2.imread(fn)

            H = homography.find_homography(img, debug=True)

            # Checks that we find a chessboard.
            self.assertTrue(H is not None, "In image '%s', could not find homography." % d["filename"])

            # If the corner positions in the original image are available in
            # the metadata, we invert the homography to compute where we would
            # see them, and check that it's "close enough". The order of
            # corners in the metadata doesn't matter.
            if "corners" in d:
                # The corner positions in the metadata.
                img_corner_positions = np.array(
                    [ [ c["x"], c["y"], 1.0 ] for c in d["corners"] ],
                    np.float64)

                # The corner positions in the idealized image.
                proj_corner_positions = np.array([
                    [   0.0,   0.0, 1.0 ],
                    [ 800.0,   0.0, 1.0 ],
                    [ 800.0, 800.0, 1.0 ],
                    [   0.0, 800.0, 1.0 ]
                ], np.float64)

                invertible, Hinv = cv2.invert(H)
                self.assertTrue(invertible) # OpenCV's problem.

                back_projected_corners = np.dot(Hinv, proj_corner_positions.T).T

                # Compute best match for each point, and ensures it's "close enough"
                min_img_dim = float(min(img.shape[0], img.shape[1]))
                # The distance from a corner of a square to the center of that
                # square if the chessboard occupied the full image. Arbitrary :)
                max_tolerated_distance = (min_img_dim / 8.0) * np.sqrt(2.0) / 2.0
                for i in xrange(0, img_corner_positions.shape[0]):
                    m_dist = 1e10
                    for j in xrange(0, 4):
                        dist = np.linalg.norm(img_corner_positions[i] - back_projected_corners[j])
                        m_dist = min(m_dist, dist)

                    self.assertTrue(m_dist < max_tolerated_distance, "In img '%s', corners should match metadata." % d["filename"])

            # TODO check that this really looks like a chessboard...
            # Maybe count squares that are "mostly black/white" in binarized img?

            # reproj = cv2.warpPerspective(img, H, (800, 800))
            # cv2.imshow("reproj-%d" % self.r(), reproj)

            # binary = pipeline.binarize(pipeline.to_gray(reproj), 0.2)
            # cv2.imshow("binary-%d" % self.r(), binary)

            # FIXME not ready for prime time
            # homography.check_homography(img, H)

            r = raw_input()

if __name__ == "__main__":
    unittest.main()
