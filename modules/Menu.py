import pygame
import math
import time

from controllers.HandGestureController import HandGestureController
from modules.IModule import Module

NAVY_BLUE = (20, 20, 40)
LIGHT_BLUE = (173, 216, 230)
SCREEN_SIZE = (1920, 1080)


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


class AppCircle:
    def __init__(self, center, radius, app_name, final_pos, is_main=False, is_visible=False):
        self.center = center
        self.radius = radius
        self.text = app_name
        self.hover_time = 0
        self.is_hovered_flag = False
        self.is_main = is_main
        self.visible = is_visible
        self.final_pos = final_pos
        self.animation_start_time = time.time()
        self.is_animating = False
        self.image = None
        self.click_start_time = None

    def draw(self, screen):
        if self.is_hovered_flag:
            current_radius = self.radius + min((time.time() - self.hover_time) * 10, self.radius * 0.5)
        else:
            current_radius = self.radius

        if self.animation_start_time is not None:
            elapsed_time = time.time() - self.animation_start_time
            if elapsed_time < 0.5:
                t = elapsed_time / 0.5
                if self.visible:
                    self.center = (
                        int((1 - t) * SCREEN_SIZE[0] // 2 + t * self.final_pos[0]),
                        int((1 - t) * SCREEN_SIZE[1] // 2 + t * self.final_pos[1])
                    )
                else:
                    self.center = (
                        int(t * SCREEN_SIZE[0] // 2 + (1 - t) * self.final_pos[0]),
                        int(t * SCREEN_SIZE[1] // 2 + (1 - t) * self.final_pos[1])
                    )
            else:
                self.center = self.final_pos if self.visible else (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
                self.animation_start_time = None
                self.is_animating = False

        if self.visible or self.is_animating:
            if self.image:
                top_left = (self.center[0] - self.radius, self.center[1] - self.radius)
                screen.blit(self.image, top_left)
            else:
                pygame.draw.circle(screen, NAVY_BLUE, self.center, int(current_radius))
            pygame.draw.circle(screen, LIGHT_BLUE, self.center, int(current_radius), 5)

            if not self.image:
                font = pygame.font.Font(None, 32)
                text_surface = font.render(self.text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=self.center)

                # Check if text width is greater than the circle diameter
                if text_rect.width > 2 * self.radius:
                    words = self.text.split()
                    lines = []
                    current_line = words[0]
                    for word in words[1:]:
                        test_line = current_line + ' ' + word
                        test_surface = font.render(test_line, True, (255, 255, 255))
                        if test_surface.get_width() <= 2 * self.radius:
                            current_line = test_line
                        else:
                            lines.append(current_line)
                            current_line = word
                    lines.append(current_line)

                    # Draw each line of text
                    for i, line in enumerate(lines):
                        line_surface = font.render(line, True, (255, 255, 255))
                        line_rect = line_surface.get_rect(
                            center=(self.center[0], self.center[1] - (len(lines) - 1) * 16 + i * 32))
                        screen.blit(line_surface, line_rect)
                else:
                    screen.blit(text_surface, text_rect)
