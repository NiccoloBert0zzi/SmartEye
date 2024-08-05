from modules.IModule import Module
import numpy as np
import cv2
import pygame


def convert_to_gray8(gray16_image):
    gray8_image = np.zeros((gray16_image.shape[0], gray16_image.shape[1]), dtype=np.uint8)
    gray8_image = cv2.normalize(gray16_image, gray8_image, 0, 255, cv2.NORM_MINMAX)
    return np.uint8(gray8_image)


class ThermalScanner(Module):
    def __init__(self):
        self.img = None
        self.gray8_image = None
        self.gray16_image = None

    def run(self, image_data, **kwargs):
        palette = kwargs.get('palette', '')
        self.gray16_image = image_data
        self.gray8_image = convert_to_gray8(self.gray16_image)
        self.img = self.apply_palette(palette)

    def draw(self, screen, **kwargs):
        if self.img is None:
            return screen  # Skip drawing if self.img is not set

        # Convert the OpenCV image to a Pygame surface
        img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        img_surface = pygame.surfarray.make_surface(np.rot90(img_rgb))

        # Blit the Pygame surface onto the screen
        screen.blit(img_surface, (0, 0))
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
