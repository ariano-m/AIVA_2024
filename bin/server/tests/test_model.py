from ultralytics import YOLO
import cv2 as cv
import unittest
import sys

sys.path.append('../')
from system.model import Model


class TestModel(unittest.TestCase):
    model, image = Model(), None
    MODEL_PATH, IMG_PATH = "", ""
    path = './output.png'

    def setUp(self):
        TestModel.MODEL_PATH = self.MODEL_PATH
        TestModel.IMG_PATH = self.IMG_PATH
        TestModel.image = cv.imread(self.IMG_PATH)

    def test_load_model(self):
        self.model.load_model(TestModel.MODEL_PATH)
        self.assertTrue(isinstance(self.model.model, YOLO))  # Ya no devuelve un modelo

    def test_predict(self):
        coords = self.model.inference(self.image)
        self.assertTrue(isinstance(coords, list))

        for x, y, x2, y2 in coords:
            self.assertTrue(0 <= x < self.image.shape[1])
            self.assertTrue(0 <= y < self.image.shape[0])
            self.assertTrue(0 <= x2 < self.image.shape[1])
            self.assertTrue(0 <= y2 < self.image.shape[0])


if __name__ == '__main__':
    if len(sys.argv) > 2:
        TestModel.MODEL_PATH = sys.argv[1]
        TestModel.IMG_PATH = sys.argv[2]
    else:
        TestModel.MODEL_PATH = "../models/Yolo_Training2/weights/best.pt"
        TestModel.IMG_PATH = '../../../dataset/MuestrasMaderas/10.png'

    unittest.main(argv=['first-arg-is-ignored'], exit=False)
