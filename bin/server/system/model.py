from ultralytics import YOLO
import numpy as np
import torch
import cv2

if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

print("MODEL RUNNING ON:", device)


class Model:
    def __init__(self):
        super().__init__()
        self.model = self.define_model()

    def load_model(self, path: str) -> None:
        """
        Load a YOLO model from the specified path.

        :param path: str, Path to the YOLO model.
        :return: None
        """
        self.model = YOLO(path)
        self.model = self.model.to(device)

    def inference(self, image: np.ndarray) -> list:
        """
        Predict the bounding box of the given image

        :param image: np.ndarray, Image to be predicted
        :return: None
        """
        results = self.model.predict(image)
        contours = []
        for i in results:
            box = i.boxes.xyxy
            if box.size != 0:
                defects = box
                for x1, y1, x2, y2 in defects:
                    cnt = (int(x1), int(y1 - 10), int(x2), int(y2 - 10))
                    contours.append(cnt)

        if not contours:
            contours = self._processing_image(image)

        return contours
    def _processing_image(self, image: np.ndarray) -> list:
        kernel = np.ones((5, 5), np.uint8)
        im_bin = cv2.erode(image[:, :, 0], kernel, iterations=3)
        contours, hierarchy = cv2.findContours(im_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea)[:-1]
        bboxes = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            bboxes.append((x, y, x + w, y + h))
        return bboxes

    def define_model(self) -> YOLO:
        """
        Define and initialize the neural network model.

        :return: YOLO, Initialized YOLO model.
        """
        yolo = YOLO('yolov8.yaml')  # sin pesos 'yolov8.yaml' con pesos 'yolov8n.pt'
        return yolo.to(device)
