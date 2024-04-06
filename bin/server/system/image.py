import numpy as np


class MyImage:
    def __init__(self, image):
        super().__init__()
        self.original_image = image
        self.bbox_imperfections = []
        self.bbox_margins = []
        self.user = ""
        self.datetime_ = 0.0

    @property
    def original_image(self):
        return self.original_image

    @original_image.setter
    def original_image(self, img: np.ndarray):
        self._original_image = img

    @property
    def bbox_imperfections(self):
        return self.bbox_imperfections

    @bbox_imperfections.setter
    def bbox_imperfections(self, bbox_l: list):
        self.bbox_imperfections = bbox_l

    @property
    def bbox_margins(self):
        return self.bbox_margins

    @bbox_margins.setter
    def bbox_margins(self, bbox_l: list):
        self.bbox_margins = bbox_l

    @property
    def user(self):
        return self.user

    @user.setter
    def user(self, username: str):
        self.user = username

    @property
    def datetime_(self):
        return self.datetime_

    @datetime_.setter
    def datetime(self, time_: float):
        self.datetime_ = time_




