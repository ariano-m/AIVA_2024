
class MySystem:
    def __init__(self, model):
        super().__init__()
        self.model = model

    def preprocess_image(self, image):
        pass

    def detect_damage(self, image):
        pass

    def place_figures(self, image, coord_damage):
        pass

    def color_figures(self, image, coord):
        pass

    def save_image(self, image, path):
        pass