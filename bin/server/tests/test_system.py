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
    path = './output.png'

    def test_morphology(self):
        self.assertEqual(self.my_system.preprocess_image(self.image).shape, (442, 488, 3))

    def test_get_contours(self):
        coords = self.my_system.get_contours(self.image)
        self.assertTrue(isinstance(coords, cv.typing.Rect))  # Sequence[int]
        x, y, w, h = coords
        self.assertTrue(0 <= x < self.image.shape[0])
        self.assertTrue(0 <= y < self.image.shape[1])
        self.assertTrue(0 <= x + w < self.image.shape[0])
        self.assertTrue(0 <= y + h < self.image.shape[1])

    def test_preprocess_image(self):
        self.assertEqual(self.my_system.preprocess_image(self.image).size(), (488, 442))

    def test_detect_damage(self):
        coords = self.my_system.detect_damage(self.image)
        self.assertTrue(isinstance(coords, list))
        self.assertEquals(len(coords) % 2, 0)

    def test_place_figures(self):
        img_bin = self.my_system.preprocess_image(self.image)
        erode_img = self.my_system.morphology(img_bin)
        result = self.my_system.place_figures(self.image,
                                              self.my_system.detect_damage(self.image),
                                              self.my_system.get_contours(erode_img))

        for x, y, x2, y2 in result:
            self.assertTrue(0 <= x < self.image.shape[0])
            self.assertTrue(0 <= y < self.image.shape[1])
            self.assertTrue(0 <= x2 < self.image.shape[0])
            self.assertTrue(0 <= y2 < self.image.shape[1])

    def test_color_figures(self):
        img_bin = self.my_system.preprocess_image(self.image)
        erode_img = self.my_system.morphology(img_bin)
        coord = self.my_system.place_figures(self.image,
                                               self.my_system.detect_damage(self.image),
                                               self.my_system.get_contours(erode_img))

        result = self.my_system.color_figures(self.image, coord)
        self.assertTrue(isinstance(result, np.ndarray))
        #with self.assertRaises(TypeError):
        #    self.my_system.color_figures(self.image, coord)

    # def test_save_image(self):
    #     self.assertTrue(os.path.exists(self.path))
    #     with self.assertRaises(TypeError):
    #          self.my_system.save_image(self.image, self.path)
