from modules.IModule import Module
import cv2
import numpy as np
import pygame


class FingerDraw(Module):
    def __init__(self, img, detector):
        h, w, c = img.shape
        self.img_canvas = np.zeros((h, w, c), np.uint8)
        self.yp, self.xp = 0, 0
        self.detector = detector

    def run(self, img, **kwargs):
        img = self.detector.findHands(img)
        n_fingers, index_fingers = self.detector.fingersUp()

        if n_fingers == 1:
            position = self.detector.getFingerPosition(img, index_fingers[0])
            if position is not None:
                x1, y1 = position
                if self.xp == 0 and self.yp == 0:
                    self.xp, self.yp = x1, y1
                cv2.line(self.img_canvas, (self.xp, self.yp), (x1, y1), (255, 0, 255), 15)
                self.xp, self.yp = x1, y1
        elif n_fingers == 4:  # Modalità gomma attivata
            position = self.detector.getFingerPosition(img, index_fingers[0])
            if position is not None:
                x1, y1 = position
                cv2.circle(self.img_canvas, (x1, y1), 30, (0, 0, 0), -1)  # Cancella con un cerchio nero
        else:
            self.xp, self.yp = 0, 0  # Resetta la posizione se nessun dito o più di due dita sono alzate

    def draw(self, screen, **kwargs):
        # Convert the OpenCV image to a Pygame surface
        img_rgb = cv2.cvtColor(self.img_canvas, cv2.COLOR_BGR2RGB)
        img_surface = pygame.surfarray.make_surface(np.rot90(img_rgb))

        # Blit the Pygame surface onto the screen
        screen.blit(img_surface, (0, 0))
        return screen

    def destroy(self, **kwargs):
        print("FingerDraw destroyed")

    def get_module_name(self):
        return 'FingerDraw'
