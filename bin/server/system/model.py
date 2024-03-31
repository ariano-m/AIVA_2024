import matplotlib.pyplot as plt
from ultralytics import YOLO
import numpy as np
import cv2


class Model:
    def __init__(self):
        super().__init__()
        self.model = self.define_model()

    def _load_model(self, path: str):
        """
        Load a YOLO model from the specified path.

        :param path: str, Path to the YOLO model.
        :return: None
        """
        self.model = YOLO(path)

    def predict(self, image: np.ndarray):
        """
        Predict the bounding box of the given image

        :param image: np.ndarray, Image to be predicted
        :return: None
        """
        results = self.model.predict(image)
        for i in results:
            box = i.boxes.xyxy
            print(box)
            if box.size != 0:
                img = cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)
                plt.imshow(img)
                plt.axis('off')
                plt.show()

    def define_model(self) -> YOLO:
        """
        Define and initialize the neural network model.

        :return: YOLO, Initialized YOLO model.
        """
        return YOLO('yolov8n.pt')  # sin pesos 'yolov8n.yaml' con pesos 'yolov8n.pt'
