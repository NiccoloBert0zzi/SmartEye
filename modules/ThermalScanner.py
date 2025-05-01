from geometry.AppCirlce import AppCircle
from modules.IModule import Module
import numpy as np
import cv2
import pygame
from controllers.HandGestureController import HandGestureController


def convert_to_gray8(gray16_image):
    gray8_image = np.zeros((gray16_image.shape[0], gray16_image.shape[1]), dtype=np.uint8)
    gray8_image = cv2.normalize(gray16_image, gray8_image, 0, 255, cv2.NORM_MINMAX)
    return np.uint8(gray8_image)


class ThermalScanner(Module):
    def __init__(self):
        self.img = None
        self.gray8_image = None
        self.gray16_image = None
        self.menu_circle = AppCircle((80, 80), 80, "menu", (80, 80), is_visible=True)
        self.module_finished = False

    def run(self, image_data, **kwargs):
        self.module_finished = False
        palette = kwargs.get('palette', '')
        self.gray16_image = image_data
        self.gray8_image = convert_to_gray8(self.gray16_image)
        self.img = self.apply_palette(palette)

        fingers = kwargs.get('fingers', [])
        if HandGestureController.is_finger_touching_circle(fingers, self.menu_circle):
            self.module_finished = True

    def draw(self, screen, **kwargs):
        if self.img is None:
            return screen  # Skip drawing if self.img is not set

        # Flip the image vertically
        flipped_img = cv2.flip(self.img, 1)

        # Convert the OpenCV image to a Pygame surface
        img_rgb = cv2.cvtColor(flipped_img, cv2.COLOR_BGR2RGB)
        img_surface = pygame.surfarray.make_surface(np.rot90(img_rgb))

        # Blit the Pygame surface onto the screen
        screen.blit(img_surface, (0, 0))

        # Draw menu circle
        self.menu_circle.draw(screen)

        return screen

    def destroy(self, **kwargs):
        pass

    def apply_palette(self, palette):
        if palette == 'inferno':
            return cv2.applyColorMap(self.gray8_image, cv2.COLORMAP_INFERNO)
        elif palette == 'jet':
            return cv2.applyColorMap(self.gray8_image, cv2.COLORMAP_JET)
        elif palette == 'viridis':
            return cv2.applyColorMap(self.gray8_image, cv2.COLORMAP_VIRIDIS)
        else:
            raise ValueError("Unsupported palette")

    def get_module_name(self):
        return 'Thermal Scanner'

    def isModuleFinished(self):
        return self.module_finished
