import copy
import matplotlib.pyplot as plt
from ultralytics import YOLO
import numpy as np
import cv2
import sys

sys.path.append('../system')
from model import Model


class Trainer:
    def __init__(self):
        """
        Initializes the Trainer class.
        """
        super().__init__()

    def train(self, model: YOLO, data: str, epochs: int, batch: int, size: int, name: str, path: str):
        """
        Train the specified YOLO model.

        :param model: YOLO,  model to train.
        :param data: str, Path to the dataset YAML file.
        :param epochs: int, Number of epochs for training.
        :param batch: int, Batch size for training.
        :param size: int, Image size (e.g., 488x442).
        :param name: str, Name of the results directory.
        :param path: str, Directory for saving models, results & logging.
        :return: None
        """
        results = model.train(
            data=data,
            imgsz=size,
            epochs=epochs,
            batch=batch,
            name=name,
            project=path)

        print("Train metrics: ")
        for key, value in results.results_dict.items():
            if key.startswith('metrics/'):
                key = key[len('metrics/'):]
            print(f"{key}: {value:.6f}")

    def evaluate(self, model: YOLO, name: str, path: str):
        """
        Evaluates the trained YOLO model.

        :param model: YOLO, The trained model to be evaluated.
        :param name: str, Name of the results directory.
        :param path: str, Directory for saving models, results & logging.
        :return: None
        """
        result = model.val(name=name, project=path)
        print("Validation metrics: ")
        for key, value in result.results_dict.items():
            if key.startswith('metrics/'):
                key = key[len('metrics/'):]
            print(f"{key}: {value:.6f}")

    def save_model(self, model: YOLO, format: str, name: str, path: str):
        """
        Saves the trained YOLO model in the specified format.

        :param model: YOLO, The trained model to be saved.
        :param format: str, The format to export the model, such as ONNX format or torchscript.
        :param name: str, Name of the results directory.
        :param path: str, Directory for saving models, results & logging.
        :return: None
        """
        model.export(format=format, name=name, project=path)

    def plot_loss(self, path: str):
        """
        Plot the loss curve.

        :param path: str, Path to the loss curve image (str).
        :return: None
        """
        img = cv2.imread(path)
        plt.axis('off')
        plt.imshow(img)


def main():
    save_path = '../models/'
    save_val = './my_val'
    name = 'Yolo_Training2'

    trainer = Trainer()
    model_ = Model()
    trainer.train(model_.model, '../../../dataset/data.yaml', 300, 64, 512, name, save_path)
    print("Training finished!")

    model_._load_model(f'{save_path}/{name}/weights/best.pt')

    trainer.evaluate(model_.model, name, save_val)
    trainer.save_model(model_.model, 'torchscript', name, save_path)
    trainer.plot_loss(f'{save_path}/{name}/results.png')

    img = cv2.imread('../../../dataset/MuestrasMaderas/06.png')

    rgb = copy.deepcopy(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, im_bin = cv2.threshold(img, 128, 192, cv2.THRESH_OTSU)
    im_bin = im_bin[:, :, np.newaxis]
    im_bin = np.repeat(im_bin, 3, axis=2)

    contours = model_.inference(im_bin)
    for x1, y1, x2, y2 in contours:
        rgb = cv2.rectangle(rgb, (int(x1), int(y1)),
                              (int(x2), int(y2)),
                              (255, 0, 0), 2)
    cv2.imshow("", rgb)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
