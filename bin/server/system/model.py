import matplotlib.pyplot as plt
from ultralytics import YOLO
import numpy as np
import torch
import cv2

device = 'cuda' if torch.cuda.is_available() else 'cpu'

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
        self.model = self.model.to(device)

    def predict(self, image: np.ndarray):
        """
        Predict the bounding box of the given image

        :param image: np.ndarray, Image to be predicted
        :return: None
        """
        results = self.model.predict(image)
        for i in results:
            print("i.boxes", i.boxes)
            box = i.boxes.xyxy
            print(box)
            if box.size != 0:
                defects = box.tolist()
                for x1,y1,x2,y2 in defects:
                  image = cv2.rectangle(image, (int(x1), int(y1)),
                                        (int(x2), int(y2)),
                                        (255, 0, 0), 2)
                  plt.imshow(image)
                  plt.axis('off')
                  plt.savefig('./prediction.png')

    def define_model(self) -> YOLO:
        """
        Define and initialize the neural network model.

        :return: YOLO, Initialized YOLO model.
        """
        yolo = YOLO('yolov8n.yaml')  # sin pesos 'yolov8n.yaml' con pesos 'yolov8n.pt'
        return yolo.to(device)