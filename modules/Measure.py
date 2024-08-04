from scipy.spatial import distance as dist
import numpy as np
import imutils
from imutils import contours
import cv2
import pygame

from modules.IModule import Module


def find_aruco_markers(img, marker_size=5, total_markers=50):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(cv2.aruco, f'DICT_{marker_size}X{marker_size}_{total_markers}')

    aruco_dict = cv2.aruco.getPredefinedDictionary(key)
    aruco_param = cv2.aruco.DetectorParameters()
    bbox, ids, rejected = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_param)
    return bbox, ids, rejected


class Measure(Module):
    def __init__(self):
        self.objects = []
        self.is_analyzing = False

    def run(self, img, **kwargs):
        self.analyze_image(img)

    def draw(self, screen, **kwargs):
        self.draw_results(screen)
        return screen

    def destroy(self, **kwargs):
        # Implement any cleanup logic here
        pass

    def analyze_image(self, img):
        image = img
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.GaussianBlur(img_gray, (7, 7), 0)

        edged = cv2.Canny(img_gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        contours_find = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_find = imutils.grab_contours(contours_find)
        (contours_find, _) = contours.sort_contours(contours_find)

        aruco_found = find_aruco_markers(image, total_markers=50)
        if len(aruco_found[0]) != 0:
            aruco_perimeter = cv2.arcLength(aruco_found[0][0][0], True)
            pixels_per_metric = aruco_perimeter / 20
        else:
            pixels_per_metric = 38.0

        self.objects = []
        for c in contours_find:
            if cv2.contourArea(c) < 2000:
                continue

            box = cv2.minAreaRect(c)
            box = cv2.boxPoints(box)
            box = np.intp(box)

            m = cv2.moments(c)
            c_x = int(m["m10"] / m["m00"])
            c_y = int(m["m01"] / m["m00"])

            (tl, tr, br, bl) = box
            width_1 = (dist.euclidean(tr, tl))
            height_1 = (dist.euclidean(bl, tl))
            d_wd = width_1 / pixels_per_metric
            d_ht = height_1 / pixels_per_metric

            self.objects.append({
                "box": box,
                "centroid": (c_x, c_y),
                "width": d_wd,
                "height": d_ht
            })
        self.is_analyzing = True

    def draw_results(self, screen):
        for obj in self.objects:
            box = obj["box"]
            d_wd = obj["width"]
            d_ht = obj["height"]

            # Define the margin
            margin = 20

            # Calculate the points for the width line with margin
            p1 = (int(box[0][0] - margin), int(box[0][1] - margin))
            p2 = (int(box[1][0] + margin), int(box[1][1] - margin))

            # Draw a line for the width with arrow
            pygame.draw.line(screen, (255, 255, 255), p2, p1, 2)

            # Calculate the points for the height line with margin
            p3 = (int(box[1][0] + margin), int(box[1][1] - margin))
            p4 = (int(box[2][0] + margin), int(box[2][1] + margin))

            # Draw a line for the height with arrow
            pygame.draw.line(screen, (255, 255, 255), p3, p4, 2)

            # Define the text offset
            text_offset = 10

            # Create font object
            font = pygame.font.Font(None, 24)

            # Put the width text in the middle of the width line with offset
            width_text = font.render("{:.1f}cm".format(d_wd), True, (255, 255, 255))
            screen.blit(width_text, (int((p1[0] + p2[0]) * 0.5), int((p1[1] + p2[1]) * 0.5) - text_offset))

            # Put the height text in the middle of the height line with offset
            height_text = font.render("{:.1f}cm".format(d_ht), True, (255, 255, 255))
            screen.blit(height_text, (int((p3[0] + p4[0]) * 0.5) + text_offset, int((p3[1] + p4[1]) * 0.5)))

    def get_module_name(self):
        return 'Measure'
