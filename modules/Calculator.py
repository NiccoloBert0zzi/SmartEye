from modules.IModule import Module
from geometry.Geometry import Geometry

from controllers.HandTrackingController import HandTrackingController

SCREEN_SIZE = (1920, 1080)
LIGHT_BLUE = (173, 216, 230)


class Calculator(Module):
    def __init__(self, detector):
        self.width = SCREEN_SIZE[0]
        self.height = SCREEN_SIZE[1]
        self.buttons = self.create_buttons()
        self.detector = detector

    def create_buttons(self):
        button_size = self.width // 18  # Fixed size for square buttons
        margin = self.width // 66  # Some space between buttons

        # Calculate total grid size
        total_grid_width = 4 * button_size + 3 * margin
        total_grid_height = 4 * button_size + 3 * margin

        # Calculate starting position to center grid
        start_x = (self.width - total_grid_width) // 2
        start_y = (self.height - total_grid_height) // 2

        buttons_text = [
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["AC", "0", "=", "/"]
        ]

        buttons = []
        for i in range(4):
            for j in range(4):
                top_left = (
                    start_x + j * (button_size + margin), start_y + i * (button_size + margin))
                bottom_right = (
                    start_x + (j + 1) * button_size + j * margin, start_y + (i + 1) * button_size + i * margin)
                text = buttons_text[i][j]
                # Add the button to the list
                buttons.append({
                    "top_left": top_left,
                    "bottom_right": bottom_right,
                    "text": text,
                    "key": text
                })
        rectangle_top_left = (start_x, start_y - button_size - margin)
        rectangle_bottom_right = (start_x + total_grid_width, start_y - margin)
        buttons.append({
            "top_left": rectangle_top_left,
            "bottom_right": rectangle_bottom_right,
            "text": "",
            "key": "result"
        })
        return buttons

    def draw_calculator(self, screen):
        for button in self.buttons:
            Geometry.draw_square_with_text(screen, button["top_left"], button["bottom_right"], button["text"],
                                           font_color=LIGHT_BLUE)

    def run(self, img, **kwargs):
        fingers = self.detector.find_all_positions(img, fingers=[(8, True), (4, True)])
        clicking, click_index = HandTrackingController.check_if_click(fingers, self.buttons)
        if clicking:
            if self.buttons[click_index]["key"] == "AC":
                self.buttons[-1]["text"] = ""
            elif self.buttons[click_index]["key"] != "result":
                # Append the value to the last button
                self.buttons[-1]["text"] += self.buttons[click_index]["text"]
            else:
                # Calculate the result
                try:
                    self.buttons[-1]["text"] = str(eval(self.buttons[-1]["text"]))
                except (SyntaxError, ZeroDivisionError):
                    self.buttons[-1]["text"] = "Error"

    def draw(self, screen, **kwargs):
        self.draw_calculator(screen)
        return screen

    def destroy(self, **kwargs):
        pass

    def get_module_name(self):
        return 'Calculator'
