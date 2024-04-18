import numpy as np


class MyImage:
    def __init__(self, image):
        super().__init__()
        self._original_image = image
        self._bbox_imperfections = []
        self._bbox_margins = []
        self._user = ""
        self._datetime = 0.0

    @property
    def original_image(self):
        return self._original_image

    @original_image.setter
    def original_image(self, img: np.ndarray):
        self._original_image = img

    @property
    def bbox_imperfections(self):
        return self._bbox_imperfections

    @bbox_imperfections.setter
    def bbox_imperfections(self, bbox_l: list):
        self._bbox_imperfections = bbox_l

    @property
    def bbox_margins(self):
        return self._bbox_margins

    @bbox_margins.setter
    def bbox_margins(self, bbox_l: list):
        self._bbox_margins = bbox_l

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, username: str):
        self._user = username

    @property
    def datetime(self):
        return self._datetime

    @datetime.setter
    def datetime(self, time_: str):
        self._datetime = time_




