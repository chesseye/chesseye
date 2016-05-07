import cv2
import sys
import numpy as np

# All image transformations.
import pipeline

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # We read from a pre-recorded video
        cap = cv2.VideoCapture(sys.argv[1])
    else:
        cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()

        # Press Q to quit, or when video is over.
        if not ret or cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Image dimensions. Not likely to change over time, but still.
        img_h, img_w = frame.shape[:2]
        img_max = max(img_h, img_w)
        img_min = min(img_h, img_w)

        # Minimum expected size of the board (arbitrary)
        min_board_size = 0.7 * img_min

        # Grayscale version
        bw = pipeline.to_gray(frame)
        cv2.imshow("bw", bw)

        # Tracking features, hopefully finding lots of corners
        corners = pipeline.get_corners(bw, 100, min_board_size / 12)
        if corners:
            for x,y in corners:
                cv2.circle(frame, (x,y), 5, 255, -1) 

        # Thresholded. The chessboard should be black/white after this step.
        binary = pipeline.binarize(bw, 0.2)
        # Edge detector.
        edges = cv2.Canny(binary, 100, 250, apertureSize = 3)
        # Thicker edges.
        thick_edges = cv2.dilate(edges, cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3)))

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
                # A value of `a` close to 1 or -1 means horizontal
                # A value of `a` close to 0 means vertical
                if abs(a) < 0.1:
                    v_lines.append((rho,theta))
                    is_v = True
                elif abs(1.0 - abs(a)) < 0.1:
                    h_lines.append((rho,theta))
                    is_h = True

                b = np.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                if is_v:
                    color = (0,255,0) # green
                elif is_h:
                    color = (0,0,255) # red
                else:
                    color = (80,80,80) # some gray

                cv2.line(frame,(x1,y1),(x2,y2),color,1)

        if h_lines and v_lines and corners:
            # TODO: check distance between corners and lines and filter out corners not on both v and h lines
            pass

        cv2.imshow("frame", frame)

        # END OF WHILE LOOP

    cap.release()
    cv2.destroyAllWindows()  
