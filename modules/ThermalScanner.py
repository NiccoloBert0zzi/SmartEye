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
        self.menu_button = {"center": (50, 50), "radius": 40, "text": "menu", "key": "menu"}
        self.module_finished = False

    def run(self, image_data, **kwargs):
        self.module_finished = False
        palette = kwargs.get('palette', '')
        self.gray16_image = image_data
        self.gray8_image = convert_to_gray8(self.gray16_image)
        self.img = self.apply_palette(palette)

        fingers = kwargs.get('fingers', [])
        clicking, click_index = HandGestureController.check_if_click(fingers, [self.menu_button])
        if clicking:
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

        # Draw menu button
        pygame.draw.circle(screen, (255, 0, 0), self.menu_button["center"], self.menu_button["radius"])
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.menu_button["text"], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.menu_button["center"])
        screen.blit(text_surface, text_rect)

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
