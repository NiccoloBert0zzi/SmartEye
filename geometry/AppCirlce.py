import time
import pygame
from data.Constants import SCREEN_SIZE, NAVY_BLUE, LIGHT_BLUE


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

                    for i, line in enumerate(lines):
                        line_surface = font.render(line, True, (255, 255, 255))
                        line_rect = line_surface.get_rect(
                            center=(self.center[0], self.center[1] - (len(lines) - 1) * 16 + i * 32))
                        screen.blit(line_surface, line_rect)
                else:
                    screen.blit(text_surface, text_rect)
