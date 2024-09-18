import cv2
import numpy as np
import pygame
from modules.IModule import Module
from ultralytics import YOLO
import supervision as sv


class ObjectRecognition(Module):
    def __init__(self):
        super().__init__()
        self.model = YOLO('yolov8l.pt')
        self.detections = None
        self.labels = None
        self.filtered_detections = None
        self.cap = cv2.VideoCapture(0)

    def run(self, image_data, **kwargs):
        _, img = self.cap.read()

        result = self.model(img, agnostic_nms=True)[0]
        self.detections = sv.Detections.from_yolov8(result)
        self.filtered_detections = [
            detection
            for detection
            in self.detections
            if detection[1] > 0.65
        ]

    def draw(self, screen, **kwargs):
        cap = cv2.VideoCapture(0)
        _, img = cap.read()

        result = self.model(img, agnostic_nms=True)[0]
        self.detections = sv.Detections.from_yolov8(result)
        self.filtered_detections = [
            detection
            for detection
            in self.detections
            if detection[1] > 0.65
        ]

        if self.detections is not None:
            for detection in self.filtered_detections:
                x1, y1, x2, y2 = detection[0]
                confidence = detection[1]
                class_id = detection[2]
                label = f"{self.model.model.names[class_id]} {confidence:.2f}"
                rect = pygame.Rect(int(x1), int(y1), int(x2 - x1), int(y2 - y1))
                pygame.draw.rect(screen, (255, 0, 0), rect, 2)
                font = pygame.font.Font(None, 24)
                text = font.render(label, True, (255, 0, 0))
                screen.blit(text, (int(x1), int(y1) - 20))
        return screen

    def destroy(self, **kwargs):
        pass

    def get_module_name(self):
        return 'Object Recognition'