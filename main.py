import os

import cv2
import pygame
import numpy as np

from controllers.ModuleController import ModuleManager
from modules import HandTracking as HandTrackingModule
from modules.FingerDraw import FingerDraw
from modules.ThermalScanner import ThermalScanner
from modules.ObjectRecognition import ObjectRecognition
from modules.Measure import Measure
from modules.Calculator import Calculator
from modules.Menu import Menu

# read in M
M = np.load("calibration/M.npy")


def calibrate_image(frame, width, height):
    warped_image = cv2.warpPerspective(frame, M, (width, height))
    return warped_image


def initialize_modules(manager, img, detector):
    finger_draw = FingerDraw(img, detector)
    thermal_scanner = ThermalScanner()
    object_recognition = ObjectRecognition()
    measure = Measure()
    calculator = Calculator(detector)

    manager.add_module(finger_draw)
    manager.add_module(thermal_scanner)
    manager.add_module(object_recognition)
    manager.add_module(measure)
    manager.add_module(calculator)

    menu = Menu(initial_radius=100, modules=manager.get_modules_name())
    manager.add_module(menu)

    return menu


def main():
    cap = cv2.VideoCapture(1)
    _, img = cap.read()
    img = calibrate_image(img, 1920, 1080)
    pygame.display.set_caption("SmartEye")

    manager = ModuleManager()
    detector = HandTrackingModule.HandDetector(detection_con=0.65, max_hands=1)

    active_module = initialize_modules(manager, img, detector)

    # Set up a clock to limit the frame rate
    clock = pygame.time.Clock()

    while True:
        success, img = cap.read()
        if not success:
            continue

        img = calibrate_image(img, 1920, 1080)
        hand_img = detector.find_hands(img, draw=False)
        fingers = detector.find_all_positions(hand_img, fingers=[(8, True), (4, True)])

        if active_module:
            screen.fill((0, 0, 0))
            if active_module.get_module_name() == 'Menu':
                index, text = active_module.run(img, fingers=fingers)
                if index is not None:
                    active_module = manager.modules[index]
            else:
                active_module.run(img, palette='jet' if active_module == manager.modules[1] else None)
            active_module.draw(screen)

        # Draw fingers 8 and 4
        if fingers:
            HandTrackingModule.draw_fingers(screen, fingers, draw_line=True, draw_center=True)

        # Display the Pygame window
        pygame.display.update()
        pygame.display.flip()

        # Limit the frame rate to 30 FPS
        clock.tick(30)

    manager.destroy_all()
    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    os.environ['SDL_VIDEO_WINDOW_POS'] = '1920,0'
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    pygame.display.set_caption('Home Screen')
    main()
