from keras import Model as KerasModel
from unittest import TestCase
import cv2 as cv
import sys
import os

sys.path.append('../')
from system.model import Model


class test_model(TestCase):
    model = Model("./model/")
    image = cv.imread("./images/49.png")

    def test_load_model(self):
        self.assertTrue(isinstance(self.model._load_model(), KerasModel))

    def test_predict(self):
        coords = self.model.predict(self.image)
        self.assertTrue(isinstance(coords, list))
        self.assertEquals(len(coords) % 2, 0)
