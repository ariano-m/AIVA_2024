from sklearn.model_selection import train_test_split
import numpy as np
import cv2 as cv
import itertools
import glob
import cv2


class Dataloader:
    def __init__(self):
        super().__init__()

    def load_image(self, images_l: list, bbox: list, batch_size: int) -> tuple:
        """

        :param images_l: list
        :param bbox:  list
        :param batch_size: list
        :return: tuple
        """

        def read_yaml(file: str):
            try:
                fs: cv2.FileStorage = cv.FileStorage(file, cv.FILE_STORAGE_READ)
                fn: cv2.FileNode = fs.getNode("rectangles")
                r: np.ndarray = fn.mat()
            except:
                r: np.ndarray = np.array([])
                print(f"ERROR in file: {i}")
            return r

        image_cycle: itertools.cycle = itertools.cycle(images_l)
        label_cycle: itertools.cycle = itertools.cycle(bbox)

        while True:
            data: list = []

            for i in range(batch_size):
                image_file: str = next(image_cycle)
                label_file: str = next(label_cycle)
                try:
                    img: np.ndarray = cv.imread(image_file)
                    label: np.ndarray = read_yaml(label_file)
                    data.append([img, label])
                except:
                    print(f"Image {image_file} with label {label_file} couldn't load...")

            images, bbox = zip(*data)
            data.clear()

            yield images, bbox

    def preprocess_image(self, image: np.ndarray, dimensions: tuple = (442, 488)) -> np.ndarray:
        img: np.ndarray = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        img = cv.resize(img, dimensions, interpolation=cv2.INTER_AREA) #442 x 488
        return img


# path = '../../../dataset/MuestrasMaderas/'
def split_train_val_test(path: str):
    """
        function for creating training datat
    :param path:
    :param classes:
    :return:
    """
    images_ls: list = sorted(glob.glob(path + '*.png'))
    regs_ls: list = sorted(glob.glob(path + '*.reg'))
    mix: list = list(zip(images_ls, regs_ls))
    train_data, rest_data = train_test_split(mix, train_size=0.8, shuffle=True, random_state=42) # type: (list, list)
    validation_data, test_data = train_test_split(rest_data, test_size=0.5, shuffle=False, random_state=42)
    return test_data, validation_data, test_data
