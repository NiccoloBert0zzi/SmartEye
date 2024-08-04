import cv2
import mediapipe as mp
import pygame
from geometry.Geometry import Geometry


def draw_fingers(screen, fingers, draw_line=False, draw_center=False):
    for i in range(len(fingers)):
        cx, cy = fingers[i][1], fingers[i][2]
        Geometry.draw_cross(screen, cx, cy)
        if i < len(fingers) - 1:
            nx, ny = fingers[i + 1][1], fingers[i + 1][2]
            center_x, center_y = (cx + nx) // 2, (cy + ny) // 2
            if draw_line:
                pygame.draw.line(screen, (255, 255, 255), (cx, cy), (nx, ny), 2)
            if draw_center:
                Geometry.draw_cross(screen, center_x, center_y)
                Geometry.draw_circle(screen, center_x, center_y, 14)
    return screen


class HandDetector:
    def __init__(self, mode=False, max_hands=2, model_complexity=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.maxHands = max_hands
        self.detectionCon = detection_con
        self.trackCon = track_con
        self.modelComplex = model_complexity

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [8, 12, 16, 20]
        self.results = None

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def fingers_up(self):
        positions = []
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                for ID in self.tipIds:
                    tip_y = handLms.landmark[ID].y
                    pip_y = handLms.landmark[ID - 2].y
                    if tip_y < pip_y:
                        positions.append(ID)
        return len(positions), positions

    def get_finger_position(self, img, finger_index):
        if self.results.multi_hand_landmarks:
            h, w, _ = img.shape
            for handLms in self.results.multi_hand_landmarks:
                lm = handLms.landmark[finger_index]
                return int(lm.x * w), int(lm.y * h)
        return None

    def find_all_positions(self, img, hand_no=0, fingers=None):
        if fingers is None:
            fingers = []
        finger_positions = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            h, w, _ = img.shape
            for ID, lm in enumerate(my_hand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                if any(ID == finger[0] for finger in fingers):
                    finger_positions.append([ID, cx, cy])
        return finger_positions
