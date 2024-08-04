import cv2
import numpy as np
import pygame
from modules.IModule import Module
from ultralytics import YOLO
import supervision as sv


class ObjectRecognition(Module):
    def __init__(self):
        super().__init__()
        self.model = YOLO('yolov8m.pt')
        self.box_annotator = sv.BoxAnnotator(thickness=2)
        self.detections = None
        self.labels = None

    def run(self, image_data, **kwargs):
        result = self.model(image_data)[0]
        self.detections = sv.Detections.from_ultralytics(result)
        self.labels = [
            result.names[class_id]
            for class_id
            in self.detections.class_id
        ]

    def draw(self, screen, **kwargs):
        # Convert Pygame Surface to OpenCV Image
        screen_array = pygame.surfarray.array3d(screen)
        screen_array = np.rot90(screen_array)
        screen_array = cv2.cvtColor(screen_array, cv2.COLOR_RGB2BGR)

        # Annotate the image using the box annotator
        annotated_image = self.box_annotator.annotate(
            scene=screen_array, detections=self.detections)

        # Annotate the image using the label annotator
        label_annotator = sv.LabelAnnotator()
        annotated_image = label_annotator.annotate(
            scene=annotated_image, detections=self.detections, labels=self.labels)

        # Convert the annotated image back to Pygame Surface
        annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        annotated_image = np.rot90(annotated_image, 3)
        annotated_surface = pygame.surfarray.make_surface(annotated_image)

        # Blit the annotated surface onto the screen
        screen.blit(annotated_surface, (0, 0))
        return screen

    def destroy(self, **kwargs):
        pass

    def get_module_name(self):
        return 'Object Recognition'