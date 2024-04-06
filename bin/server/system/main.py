import cv2
import numpy as np
from system import MySystem
from model import Model
def load_system() -> None:
    pass


def process_petition(image: np.ndarray) -> None:
    pass


def main():
    save_path = '../models/'
    name = 'Yolo_Training2'
    model_ = Model()
    model_._load_model(f'{save_path}/{name}/weights/best.pt')

    my_system = MySystem(model_)
    img = cv2.imread('../../../dataset/MuestrasMaderas/06.png')
    img_bin = my_system.preprocess_image(img)
    erode_img = my_system.morphology(img_bin)
    bbox_board = my_system.get_contours(erode_img)

    bbox_defects = my_system.detect_damage(img)
    bbox_figures = my_system.place_figures(img, bbox_defects, bbox_board)
    image = my_system.color_figures(img, bbox_figures)

    cv2.imshow("Figure",image)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()
