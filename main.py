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
from modules.SpaceInvader import SpaceInvader

# read in M
M = np.load("calibration/M.npy")


def calibrate_image(frame, width, height):
    warped_image = cv2.warpPerspective(frame, M, (width, height))

    flipped_image = cv2.flip(warped_image, -1)
    return flipped_image


def initialize_modules(manager, img, detector):

    manager.add_module(FingerDraw(img, detector))
    manager.add_module(ThermalScanner())
    manager.add_module(ObjectRecognition())
    manager.add_module(Measure())
    manager.add_module(Calculator(detector))
    manager.add_module(SpaceInvader(1920, 1080))

    menu = Menu(initial_radius=100, modules=manager.get_modules_name())
    manager.add_module(menu)

    return menu


def main():
    cap = cv2.VideoCapture(0)
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
            screen.fill((30, 30, 30))
            if active_module.get_module_name() == 'Menu':
                index, text = active_module.run(img, fingers=fingers)
                if index is not None:
                    active_module = manager.modules[index]
            elif active_module.get_module_name() == 'Space Invader':
                active_module.run(img, fingers=fingers)
            else:
                active_module.run(img, palette='jet' if active_module == manager.modules[1] else None)
            active_module.draw(screen)

        # Draw fingers 8 and 4
        if fingers:
            HandTrackingModule.draw_fingers(screen, fingers, draw_line=True, draw_center=True)

        # Flip the screen content horizontally before displaying
        flipped_screen = pygame.transform.flip(screen, True, True)
        pygame.display.get_surface().blit(flipped_screen, (0, 0))

        # Display the Pygame window
        pygame.display.update()

        # Limit the frame rate to 30 FPS
        clock.tick(30)

    manager.destroy_all()
    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    os.environ['SDL_VIDEO_WINDOW_POS'] = '1920,0'
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    pygame.display.set_caption('Home Screen')
    main()
