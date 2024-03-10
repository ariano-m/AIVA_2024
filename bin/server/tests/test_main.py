from unittest import TestCase
import numpy as np
import cv2 as cv
import sys

sys.path.append('../')
from system.model import System
from system import main


class test_main(TestCase):
    my_system = System()
    image = cv.imread("./images/49.png")

    def test_load_system(self):
        self.assertTrue(isinstance(self.my_system, System()))

    def test_process_petition(self):
        result = main.process_petition(self.image)
        self.assertTrue(isinstance(result, np.ndarray))

    def test_main(self):
        self.assertEquals(main.main(), 0)
