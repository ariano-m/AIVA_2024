import numpy as np
import cv2 as cv
import itertools
import glob


class Dataloader:
    def __init__(self):
        super().__init__()

    def load_image(self, images_l, labels, batch_size):
        """
            function for creating a dataloader
            :param dataset:
            :param labels:
            :param batch_size:
            :return:
        """

        def read_yaml(file):
            try:
                fs = cv.FileStorage(file, cv.FILE_STORAGE_READ)
                fn = fs.getNode("rectangles")
                r = fn.mat()
            except:
                r = np.array([])
                print(f"ERROR in file: {i}")
            return r

        image_cycle = itertools.cycle(images_l)
        label_cycle = itertools.cycle(labels)

        while True:
            data = []

            for i in range(batch_size):
                image_file = next(image_cycle)
                label_file = next(label_cycle)
                try:
                    img = cv.imread(image_file)
                    label = read_yaml(label_file)
                    data.append([img, label])
                except:
                    print(f"Image {image_file} with label {label_file} couldn't load...")

            images, labels = zip(*data)
            data.clear()

            yield images, labels

    def preprocess_image(self, image):
        pass


path = '../../../dataset/MuestrasMaderas/'
images_ls = sorted(glob.glob(path + '*.png'))
regs_ls = sorted(glob.glob(path + '*.reg'))

# images = [cv.imread(i) for i in images_ls]
# regs = []
# for i in regs_ls:
#     try:
#         fs = cv.FileStorage(i, cv.FILE_STORAGE_READ)
#         fn = fs.getNode("rectangles")
#         regs.append(fn.mat())
#     except:
#         regs.append(np.array([]))
#         print(f"ERROR in file: {i}")
