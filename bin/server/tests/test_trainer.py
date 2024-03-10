from keras import Model as KerasModel
from unittest import TestCase
import numpy as np
import sys
import os

sys.path.append('../')
from system.training.trainer import Trainer


class test_trainer(TestCase):
    my_trainer = Trainer()
    labels = [[3, 6, 8, 9], [30, 15, 34, 56]]
    predictions = [[3, 6, 8, 9], [30, 15, 20, 33]]
    path = "./output"
    loss_history = []

    def test_init(self):
        self.assertTrue(isinstance(self.my_trainer._init(), KerasModel))

    def test_compute_metrics(self, labels, predictions):
        result = self.my_trainer.compute_metrics(self.labels, self.predictions)
        self.assertTrue(isinstance(result, dict))

    def test_train(self):
        self.assertTrue(isinstance(self.my_trainer._init(), KerasModel))

    def test_evaluate(self):  # Solo devuelve por pantalla
        pass

    def test_save_model(self):
        self.assertTrue(os.path.exists(self.path))
        with self.assertRaises(TypeError):
            self.my_trainer.save_model(self.path)

    def test_plot_loss(self):
        result = self.my_trainer.plot_loss(self.loss_history)
        self.assertTrue(isinstance(result, np.ndarray))
