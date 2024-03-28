import numpy as np
from ultralytics import YOLO
class Model:
    def __init__(self, path):
        super().__init__()
        self._load_model(path)
        self.model = self.define_model()

    def _load_model(self, path: str) -> YOLO:
        return YOLO(path)

    def predict(self, image: np.ndarray, model: YOLO):
        results = model.predict(image)
        #boxes = results[0].boxes.xyxy
        pass

    def define_model(self) -> YOLO:
        """
            Define the neural network model
        :return: YOLO
        """
        return YOLO('yolov8n.pt') # sin pesos 'yolov8n.yaml' con pesos 'yolov8n.pt'