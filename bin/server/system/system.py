import cv2
import numpy as np


class MySystem:
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.triangle_size = (125, 125)
        self.rectangle_size = (150, 70)
        self.circle_size = (90, 90)

    def morphology(self, image: np.ndarray) -> np.ndarray:
        """
            Applies morphology operations to the input image.

        :param image: The input image.
        :return: The processed image.
        """
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image[:, :, 0], kernel, iterations=3)

    def get_contours(self, image: np.ndarray) -> cv2.typing.Rect:
        """
            Extracts contours from the input image and returns the bounding rectangle.

        :param image: The input binary image.
        :return: The bounding rectangle of the largest contour.
        """
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea)[-1]
        return cv2.boundingRect(contours)

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """
            Preprocess the image before feeding it to the model
        :param image: np.ndarray, image
        :return:
        """
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        th, im_bin = cv2.threshold(img, 128, 192, cv2.THRESH_OTSU)
        im_bin = im_bin[:, :, np.newaxis]
        return np.repeat(im_bin, 3, axis=2)

    def detect_damage(self, image: np.ndarray) -> list:
        """
            Detects damage in the input image.

        :param image: The input image.
        :return: A list containing detected damages.
        """
        img_bin = self.preprocess_image(image)
        return self.model.inference(img_bin)

    def place_figures(self, image, bbox_damages, black_bbox) -> list:
        """
            Places figures on the input image while avoiding damaged areas.

        :param image: The input image.
        :param bbox_damages: Bounding boxes of damaged areas.
        :param black_bbox: Bounding box of the black area.
        :return: A list of bounding boxes of placed figures.
        """
        def search(table, shape, flag):
            height, width = table.shape
            for y in range(height):
                for x in range(0, width, 100):
                    y2 = y + shape[1]
                    x2 = x + shape[0]

                    if np.all(table[y:y2, x:x2] == 0):
                        table[y:y2, x:x2] = flag
                        return x, y, x2, y2

        matrix = np.zeros(image.shape[:2])
        x, y, w, h = black_bbox
        matrix[:y, :] = -1
        matrix[y + h:, :] = -1

        for i in bbox_damages:
            x1, y1, x2, y2 = i
            matrix[y1:y2, x1:x2] = -1
            # image = cv2.rectangle(image, (x1, y1), (x2, y2), (100,100,0), thickness=4)

        bbox_l = []
        for idx, size in enumerate([self.triangle_size, self.rectangle_size, self.circle_size]):
            bbox = search(matrix, size, idx + 1)
            bbox_l.append(bbox)

        return bbox_l

    def color_figures(self, image: np.ndarray, coord: list) -> np.ndarray:
        """
            Colors the placed figures on the input image.

        :param image: The input image.
        :param coord: Coordinates of placed figures.
        """

        bbox_triangle = coord[0]
        bbox_rectangle = coord[1]
        bbox_circle = coord[2]

        colors = [(255, 0, 0), (0, 255, 0), (255, 0, 255)]
        image = cv2.rectangle(image, (bbox_rectangle[0], bbox_rectangle[1]), (bbox_rectangle[2], bbox_rectangle[3]),
                              colors[0], thickness=cv2.FILLED)

        x, y = (bbox_circle[0] + bbox_circle[2]) // 2, (bbox_circle[1] + bbox_circle[3]) // 2
        image = cv2.circle(image, (x, y), self.circle_size[0] // 2, colors[2], thickness=cv2.FILLED)

        triangle_cnt = np.array([(bbox_triangle[0], bbox_triangle[3]),
                                 (bbox_triangle[2], bbox_triangle[3]),
                                 (bbox_triangle[2], bbox_triangle[1])])
        image = cv2.drawContours(image, [triangle_cnt], 0, (0, 255, 0), -1)

        return image


    def save_image(self, image: np.ndarray, path: str) -> None:
        """
            Function for saving an image in a given path
        :param image: nd.ndarray, image to be saved
        :param path: str, path to save
        :return: None
        """
        cv2.imwrite(path, image)
