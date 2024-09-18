from modules.IModule import Module
import pygame
from controllers.HandGestureController import HandGestureController


class FingerDraw(Module):
    def __init__(self, img, detector):
        h, w, c = img.shape
        self.img_canvas = pygame.Surface((w, h), pygame.SRCALPHA)
        self.yp, self.xp = 0, 0
        self.detector = detector
        self.draw_commands = []
        self.current_color = (255, 0, 255)  # Default color: fuchsia
        self.eraser_color = (30, 30, 30)  # Eraser color matches the background
        self.color_buttons = [
            {"color": (255, 0, 255), "pos": (w // 2 - 120, 50), "radius": 20},  # Fuchsia
            {"color": (255, 255, 0), "pos": (w // 2, 50), "radius": 20},  # Yellow
            {"color": (0, 255, 255), "pos": (w // 2 + 120, 50), "radius": 20},  # Cyan
        ]
        self.menu_button = {"center": (50, 50), "radius": 40, "text": "menu", "key": "menu"}
        self.module_finished = False

    def run(self, img, **kwargs):
        self.module_finished = False
        img = self.detector.find_hands(img)
        n_fingers, index_fingers = self.detector.fingers_up()

        if n_fingers == 1:
            position = self.detector.get_finger_position(img, index_fingers[0])
            if position is not None:
                x1, y1 = position
                for button in self.color_buttons:
                    if pygame.math.Vector2(x1, y1).distance_to(button["pos"]) < button["radius"]:
                        self.current_color = button["color"]
                        return  # Exit early to avoid drawing while changing color
                if self.xp == 0 and self.yp == 0:
                    self.xp, self.yp = x1, y1
                self.draw_commands.append(('line', (self.xp, self.yp), (x1, y1), self.current_color, 15))
                self.xp, self.yp = x1, y1
        elif n_fingers == 4:  # Modalità gomma attivata
            position = self.detector.get_finger_position(img, index_fingers[0])
            if position is not None:
                x1, y1 = position
                self.draw_commands.append(('circle', (x1, y1), 30, self.eraser_color, -1))
        else:
            self.xp, self.yp = 0, 0  # Resetta la posizione se nessun dito o più di due dita sono alzate

        fingers = self.detector.find_all_positions(img, fingers=[(8, True), (4, True)])
        clicking, click_index = HandGestureController.check_if_click(fingers, [self.menu_button])
        if clicking:
            self.module_finished = True

    def draw(self, screen, **kwargs):
        for command in self.draw_commands:
            if command[0] == 'line':
                pygame.draw.line(self.img_canvas, command[3], command[1], command[2], command[4])
            elif command[0] == 'circle':
                pygame.draw.circle(self.img_canvas, command[3], command[1], command[2])

        screen.blit(self.img_canvas, (0, 0))

        # Draw color selection buttons
        for button in self.color_buttons:
            pygame.draw.circle(screen, button["color"], button["pos"], button["radius"])

        # Draw menu button
        pygame.draw.circle(screen, (255, 0, 0), self.menu_button["center"], self.menu_button["radius"])
        font = pygame.font.Font(None, 32)
        text_surface = font.render(self.menu_button["text"], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.menu_button["center"])
        screen.blit(text_surface, text_rect)

        return screen

    def destroy(self, **kwargs):
        print("FingerDraw destroyed")

    def get_module_name(self):
        return 'FingerDraw'

    def isModuleFinished(self):
        return self.module_finished
