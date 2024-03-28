from utils.plots import plot_results
from ultralytics import YOLO
import sys

sys.path.append('../server/system')
import model

class Trainer:
    def __init__(self):
        super().__init__()
        self.model = self._init()

    def _init(self):
        return model.define_model()

    def compute_metrics(self, labels, predictions):
        pass

    def train(self, model: YOLO, data: yaml, epochs: int, width: int, height: int):
        model.train(data=data, epochs=epochs, imgsz=(width,height))
        model.val()
        model.export(format='onnx')  # export the model to ONNX format

    def evaluate(self):
        model.val()
        pass

    def save_model(self, model: YOLO):
        model.export(format='onnx')

    def plot_loss(self, path: str):
        # https://docs.ultralytics.com/es/yolov5/tutorials/train_custom_data/#local-logging
        plot_results(path)  # plot 'results.csv' as 'results.png' -> 'path/to/results.csv')
        # if logger == 'TensorBoard':
        #     %load_ext
        #     tensorboard
        #     %tensorboard - -logdir
        #     runs / train
