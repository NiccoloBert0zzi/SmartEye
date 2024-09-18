import pygame
import math
import time
from controllers.HandGestureController import HandGestureController
from geometry.AppCirlce import AppCircle
from modules.IModule import Module
from data.Constants import SCREEN_SIZE


class Menu(Module):
    def __init__(self, initial_radius, modules):
        self.radius = initial_radius
        self.num_circles = len(modules)
        self.circles = self.create_circles(modules=modules)
        pygame.init()

    def run(self, img, **kwargs):
        fingers = kwargs.get('fingers', [])
        if not fingers:
            return None, None
        for index, circle in enumerate(self.circles):
            if HandGestureController.is_finger_touching_circle(fingers, circle):
                if circle.click_start_time is None:
                    circle.click_start_time = time.time()
                elif time.time() - circle.click_start_time >= 2:
                    return index, circle.text
            else:
                circle.click_start_time = None
        return None, None

    def draw(self, screen, **kwargs):
        for circle in self.circles:
            circle.is_hovered_flag = False
            circle.draw(screen)
        return screen

    def destroy(self, **kwargs):
        pygame.quit()

    def create_circles(self, modules=None):
        circles = []
        center_x, center_y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2
        main_circle_radius = 100
        app_circle_radius = 75
        distance = 250

        angle_step = 360 / self.num_circles
        for i in range(self.num_circles):
            angle = math.radians(angle_step * i)
            x = center_x + int(distance * math.cos(angle))
            y = center_y + int(distance * math.sin(angle))
            circles.append(AppCircle((center_x, center_y), app_circle_radius, modules[i], (x, y), is_visible=True))

        main_circle = AppCircle((center_x, center_y),
                                main_circle_radius,
                                self.get_module_name(),
                                (center_x, center_y),
                                is_main=True,
                                is_visible=True)
        circles.append(main_circle)
        return circles

    def get_module_name(self):
        return 'Menu'

    def isModuleFinished(self):
        return False
