import unittest
import sys
import os

sys.path.append('../')
from training.trainer import Trainer


class TestTrainer(unittest.TestCase):
    my_trainer = Trainer()
    model_path = "../models/Yolo_Training2/weights/best.pt"
    loss_history = []

    def setUp(self):
        TestTrainer.model_path = self.model_path

    def test_init(self):
        pass

    def test_train(self):
        pass

    def test_evaluate(self):  # Solo devuelve por pantalla
        pass

    def test_save_model(self):
        self.assertTrue(os.path.exists(self.model_path))

    def test_plot_loss(self):
        pass


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestTrainer.MODEL_PATH = sys.argv.pop()
    else:
        TestTrainer.MODEL_PATH = "../models/Yolo_Training2/weights/best.pt"

    unittest.main(argv=['first-arg-is-ignored'], exit=False)
