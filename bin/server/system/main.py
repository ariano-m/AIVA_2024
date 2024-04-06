from system import MySystem
from model import Model
from image import MyImage
import numpy as np
import datetime
import cv2

processed_images_l = []


def load_system() -> None:
    pass


def process_petition(image: np.ndarray) -> None:
    pass


def main():
    save_path = '../models/'
    name = 'Yolo_Training2'
    model_ = Model()
    model_.load_model(f'{save_path}/{name}/weights/best.pt')

    my_system = MySystem(model_)
    img = cv2.imread('../../../dataset/MuestrasMaderas/06.png')
    img_bin = my_system.preprocess_image(img)
    erode_img = my_system.morphology(img_bin)
    bbox_board = my_system.get_contours(erode_img)

    bbox_defects = my_system.detect_damage(img)
    bbox_figures = my_system.place_figures(img, bbox_defects, bbox_board)
    image = my_system.color_figures(img, bbox_figures)

    cv2.imshow("Figure", image)
    cv2.waitKey(0)

    my_image = MyImage()
    my_image.user = ""
    my_image.original_image = img
    my_image.bbox_imperfections = bbox_defects
    my_image.bbox_margins = bbox_board
    my_image.user = "@user"
    my_image.datatime_ = datetime.datetime.now()
    processed_images_l.append(my_image)


if __name__ == "__main__":
    main()
