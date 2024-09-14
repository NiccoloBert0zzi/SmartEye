from modules.IModule import Module
import pygame


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
            {"color": (0, 255, 255), "pos": (w // 2 + 120, 50), "radius": 20}  # Cyan
        ]

    def run(self, img, **kwargs):
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

        return screen

    def destroy(self, **kwargs):
        print("FingerDraw destroyed")

    def get_module_name(self):
        return 'FingerDraw'
