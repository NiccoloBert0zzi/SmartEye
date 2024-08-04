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
    return cv2.cvtColor(warped_image, cv2.COLOR_BGR2RGB)


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
    cap = cv2.VideoCapture(0)
    _, img = cap.read()
    # img = calibrate_image(img, width, height)
    pygame.display.set_caption("SmartEye")

    manager = ModuleManager()
    detector = HandTrackingModule.handDetector(detectionCon=0.65, maxHands=1)

    active_module = initialize_modules(manager, img, detector)

    while True:
        success, img = cap.read()
        if not success:
            continue

        # img = calibrate_image(img, width, height)
        hand_img = detector.findHands(img)
        fingers = detector.find_all_positions(hand_img, fingers=[(8, True), (4, True)])
        # Flip the image vertically
        img = cv2.flip(img, 1)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('1'):
            active_module = manager.modules[0]
        elif key == ord('2'):
            active_module = manager.modules[1]
        elif key == ord('3'):
            active_module = manager.modules[2]
        elif key == ord('4'):
            active_module = manager.modules[3]
        elif key == ord('5'):
            active_module = manager.modules[4]

        if active_module:
            screen.fill((0, 0, 0))

            active_module.run(img, palette='jet' if active_module == manager.modules[1] else None)
            active_module.draw(screen)

        # Draw fingers 8 and 4
        detector.draw_fingers(screen, fingers, draw_line=True, draw_center=True)

        # Display the Pygame window
        pygame.display.update()
        pygame.display.flip()
        pygame.time.delay(50)

        # Show the OpenCV window with the camera feed
        cv2.imshow("Camera Feed", img)
        if key == ord('q'):
            break

    manager.destroy_all()
    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # os.environ['SDL_VIDEO_WINDOW_POS'] = '-3440,0'
    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    pygame.display.set_caption('Home Screen')
    main()
