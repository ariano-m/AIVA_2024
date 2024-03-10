from unittest import TestCase
import numpy as np
import cv2 as cv
import sys
import os

sys.path.append('../')
from system.model import System
from system.model import Model


class test_system(TestCase):
    model = Model("./model/")
    my_system = System(model)
    image = cv.imread("./images/49.png")
    figures_coords = {'circle': [-50, 8, 500], 'triangle': [1, 40, 5, 90, 8], 'reactangle': [9, 15, -20, 100]}
    damage_coords = []
    path = './output'

    def test_preprocess_image(self):
        self.assertEqual(self.my_system.preprocess_image(self.image).size(), (488, 442))

    def test_detect_damage(self):
        coords = self.model.predict(self.image)
        self.assertTrue(isinstance(coords, list))
        self.assertEquals(len(coords) % 2, 0)

    def test_place_figures(self):
        # {'circle': [x, y, radio], 'triangle': [x1, y1, x2, y2, x3, y3], 'rectangle': [x, y, h, w]}
        result = self.my_system.place_figures(self.image, self.damage_coords)
        self.assertEquals(len(result['circle']), 2)
        self.assertEquals(len(result['triangle']), 6)
        self.assertEquals(len(result['rectangle']), 4)

    def test_color_figures(self):
        result = self.my_system.color_figures(self.image, self.figures_coords)
        self.assertTrue(isinstance(result, np.ndarray))
        with self.assertRaises(TypeError):
            self.my_system.color_figures(self.image, self.figures_coords)

    def test_save_image(self):
        self.assertTrue(os.path.exists(self.path))
        with self.assertRaises(TypeError):
            self.my_system.save_image(self.image, self.path)
