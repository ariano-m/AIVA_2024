
class Trainer:
    def __init__(self):
        super().__init__()
        self.model = self._init()

    def _init(self):
        pass

    def compute_metrics(self, labels, predictions):
        pass

    def train(self):
        pass

    def evaluate(self):
        pass

    def save_model(self, path):
        pass

    def plot_loss(self, loss_history):
        pass