import pygame


class Geometry:
    @staticmethod
    def draw_text_centered(screen,
                           top_left,
                           bottom_right,
                           text,
                           font=None,
                           font_size=30,
                           font_color=(255, 255, 255)):
        # Calculate the center of the rectangle
        center_x = top_left[0] + (bottom_right[0] - top_left[0]) // 2
        center_y = top_left[1] + (bottom_right[1] - top_left[1]) // 2

        # Create font object
        if font is None:
            font = pygame.font.Font(None, font_size)
        else:
            font = pygame.font.Font(font, font_size)

        # Render the text
        text_surface = font.render(text, True, font_color)
        text_rect = text_surface.get_rect(center=(center_x, center_y))

        # Draw the text
        screen.blit(text_surface, text_rect)

    @staticmethod
    def draw_cross(screen, cx, cy, color=(255, 255, 255), thickness=2):
        pygame.draw.line(screen, color, (cx - 10, cy), (cx + 10, cy), thickness)
        pygame.draw.line(screen, color, (cx, cy - 10), (cx, cy + 10), thickness)

    @staticmethod
    def draw_circle(screen, cx, cy, radius, color=(255, 255, 255), thickness=2):
        pygame.draw.circle(screen, color, (cx, cy), radius, thickness)

    @staticmethod
    def draw_menu_button(screen, top_left, bottom_right, text, font=None, font_size=30,
                         font_color=(255, 255, 255), radius=20, thickness=2):
        # Draw the rounded rectangle
        pygame.draw.line(screen, font_color, (top_left[0] + radius, top_left[1]),
                         (bottom_right[0] - radius, top_left[1]), thickness)
        pygame.draw.line(screen, font_color, (top_left[0] + radius, bottom_right[1]),
                         (bottom_right[0] - radius, bottom_right[1]), thickness)
        pygame.draw.line(screen, font_color, (top_left[0], top_left[1] + radius),
                         (top_left[0], bottom_right[1] - radius), thickness)
        pygame.draw.line(screen, font_color, (bottom_right[0], top_left[1] + radius),
                         (bottom_right[0], bottom_right[1] - radius), thickness)
        pygame.draw.arc(screen, font_color, (top_left[0], top_left[1], radius * 2, radius * 2), 3.14, 4.71, thickness)
        pygame.draw.arc(screen, font_color, (bottom_right[0] - radius * 2, top_left[1], radius * 2, radius * 2), 4.71,
                        6.28, thickness)
        pygame.draw.arc(screen, font_color,
                        (bottom_right[0] - radius * 2, bottom_right[1] - radius * 2, radius * 2, radius * 2), 0, 1.57,
                        thickness)
        pygame.draw.arc(screen, font_color, (top_left[0], bottom_right[1] - radius * 2, radius * 2, radius * 2), 1.57,
                        3.14, thickness)

        Geometry.draw_text_centered(screen, top_left, bottom_right, text, font, font_size, font_color)

    @staticmethod
    def draw_square_with_text(screen, top_left, bottom_right, text, font=None, font_size=30,
                              font_color=(255, 255, 255), thickness=2):
        # Draw the square
        pygame.draw.rect(screen, font_color, (*top_left, bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]),
                         thickness)

        # Draw the text
        Geometry.draw_text_centered(screen, top_left, bottom_right, text, font, font_size, font_color)

    @staticmethod
    def draw_circle_with_text(screen, center, radius, text, font_color=(255, 255, 255), circle_color=(20, 20, 40),
                              border_color=(173, 216, 230), border_width=5):
        # Draw the circle
        pygame.draw.circle(screen, circle_color, center, radius)
        pygame.draw.circle(screen, border_color, center, radius, border_width)

        # Render the text
        font = pygame.font.Font(None, 32)
        text_surface = font.render(text, True, font_color)
        text_rect = text_surface.get_rect(center=center)

        # Check if text width is greater than the circle diameter
        if text_rect.width > 2 * radius:
            words = text.split()
            lines = []
            current_line = words[0]
            for word in words[1:]:
                test_line = current_line + ' ' + word
                test_surface = font.render(test_line, True, font_color)
                if test_surface.get_width() <= 2 * radius:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)

            # Draw each line of text
            for i, line in enumerate(lines):
                line_surface = font.render(line, True, font_color)
                line_rect = line_surface.get_rect(center=(center[0], center[1] - (len(lines) - 1) * 16 + i * 32))
                screen.blit(line_surface, line_rect)
        else:
            screen.blit(text_surface, text_rect)
