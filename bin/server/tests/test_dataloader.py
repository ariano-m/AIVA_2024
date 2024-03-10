from unittest import TestCase
import numpy as np
import cv2 as cv
import sys

sys.path.append('../')
from system.training.dataloader import Dataloader


class test_dataloader(TestCase):
    my_dataloader = Dataloader()
    image = cv.imread("./images/49.png")

    def test_load_image(self):
        result = self.my_dataloader.load_image()
        self.assertTrue(isinstance(result, np.ndarray))

    def test_preprocess_image(self):
        result = self.my_dataloader.preprocess_image(self.image)
        self.assertTrue(isinstance(result, np.ndarray))
