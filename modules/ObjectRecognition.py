import cv2
import numpy as np
import pygame
from modules.IModule import Module
from ultralytics import YOLO
import supervision as sv


class ObjectRecognition(Module):
    def __init__(self):
        super().__init__()
        self.model = YOLO('yolov8n.pt')
        self.box_annotator = sv.BoundingBoxAnnotator(thickness=2)
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
        # Debug: Print the detections and labels
        print("Detections:", self.detections)
        print("Labels:", self.labels)

    def draw(self, img, screen, **kwargs):
        if self.detections is not None:
            # Convert image to NumPy array
            img_array = np.array(img)
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            # Annotate the image using the bounding box annotator
            annotated_image = self.box_annotator.annotate(
                scene=img_array,
                detections=self.detections
            )

            # Annotate the image using the label annotator
            label_annotator = sv.LabelAnnotator()
            annotated_image = label_annotator.annotate(
                scene=annotated_image,
                detections=self.detections,
                labels=self.labels
            )

            # Convert the annotated image back to Pygame Surface
            annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
            annotated_surface = pygame.surfarray.make_surface(annotated_image)

            # Blit the annotated surface onto the screen
            screen.blit(annotated_surface, (0, 0))
        return screen

    def destroy(self, **kwargs):
        pass

    def get_module_name(self):
        return 'Object Recognition'