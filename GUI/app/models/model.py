

from app.models.data import DataModel


class Model(object):
    
    def __init__(self, Controller) -> None:
        self.Controller = Controller

        self.DataModel = DataModel(self.Controller)
