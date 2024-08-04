import math

import numpy as np


def is_touch(finger1, finger2):
    finger1 = np.array(finger1[1:])
    finger2 = np.array(finger2[1:])
    length = math.hypot(finger2[0] - finger1[0], finger2[1] - finger1[1])
    if length < 50:
        return True
    return False


class HandTrackingController:

    @staticmethod
    def is_touch_square(finger1, top_left, bottom_right):
        # Check if the finger is inside the rectangle
        x1, y1 = finger1[1:]
        top_left_x, top_left_y = top_left
        bottom_right_x, bottom_right_y = bottom_right
        offset = -40
        if (top_left_x + offset) <= x1 <= (bottom_right_x - offset) and (top_left_y + offset) <= y1 <= (
                bottom_right_y - offset):
            return True
        else:
            return False

    @staticmethod
    def check_if_hovering(fingers, buttons):
        if len(fingers) == 0:
            return False, None

        for index, button in enumerate(buttons):
            if HandTrackingController.is_touch_square(fingers[1], button["top_left"], button["bottom_right"]):
                return True, index
        return False, None

    @staticmethod
    def check_if_click(fingers, buttons):
        if len(fingers) == 0:
            return False, None

        if is_touch(fingers[0], fingers[1]):
            return HandTrackingController.check_if_hovering(fingers, buttons)

        return False, None
