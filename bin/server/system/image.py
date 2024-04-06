

class MyImage:
    def __init__(self, image):
        super().__init__()
        self.original_image = image
        self.bbox_imperfections = []
        self.bbox_margins = []
        self.user = ""
        self.datetime_ = ""

    @property
    def original_image(self):
        return self.original_image

    @original_image.setter
    def original_image(self, value):
        self._original_image = value

    @property
    def bbox_imperfections(self):
        return self.bbox_imperfections

    @bbox_imperfections.setter
    def bbox_imperfections(self, bbox_l: list):
        self.bbox_imperfections = bbox_l

    @property
    def bbox_margins(self):
        return self.bbox_margins

    @bbox_imperfections.setter
    def bbox_margins(self, bbox_l: list):
        self.bbox_margins = bbox_l

    @property
    def user(self):
        return self.bbox_margins

    @user.setter
    def user(self, username: str):
        self.user = username

    @property
    def bbox_margins(self):
        self._bbox_margins

    @bbox_margins.setter
    def bbox_margins(self, value: list):
        self._bbox_margins = value

    @property
    def datetime_(self):
        return self.datetime_

    @datetime_.setter
    def datetime(self, time_: float):
        self.datetime_ = time_




