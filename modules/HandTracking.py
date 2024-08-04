import cv2
import mediapipe as mp
import pygame

from geometry.Geometry import Geometry


class handDetector:
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelComplex = modelComplexity

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [8, 12, 16, 20]
        self.results = None

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results and self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def fingersUp(self):
        positions = []
        if self.results and self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    if id in self.tipIds:
                        tipY = lm.y
                        pipId = id - 2
                        pipY = handLms.landmark[pipId].y
                        if tipY < pipY:
                            positions.append(id)
        return len(positions), positions

    def getFingerPosition(self, img, fingerIndex):
        if self.results and self.results.multi_hand_landmarks:
            h, w, c = img.shape  # Get the dimensions of the input image
            for handLms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    if id == fingerIndex:
                        x, y = int(lm.x * w), int(lm.y * h)  # Convert to pixel coordinates
                        return x, y
        return None

    def find_all_positions(self, img, hand_no=0, fingers=None):
        if fingers is None:
            fingers = []
        lm_list = []
        finger_positions = []
        if self.results and self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for ID, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([ID, cx, cy])
                for finger in fingers:
                    if ID == finger[0]:
                        finger_positions.append(lm_list[ID])
        return finger_positions

    def draw_fingers(self, screen, fingers, draw_line=False, draw_center=False):
        for i in range(len(fingers)):
            cx, cy = fingers[i][1], fingers[i][2]
            Geometry.draw_cross(screen, cx, cy)
            if i < len(fingers) - 1:  # Check if there is a next finger
                next_finger = fingers[i + 1]
                nx, ny = next_finger[1], next_finger[2]
                center_x, center_y = (cx + nx) // 2, (cy + ny) // 2
                if draw_line:
                    pygame.draw.line(screen, (255, 255, 255), (cx, cy), (nx, ny), 2)
                if draw_center:
                    Geometry.draw_cross(screen, center_x, center_y)
                    Geometry.draw_circle(screen, center_x, center_y, 14)
        return screen
