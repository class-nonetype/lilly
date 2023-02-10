

from app.models.data import DataModel
from app.models.json_tree import JsonModel

from PyQt5 import (
    QtWidgets)

import os



class Model(object):
    
    def __init__(self, Controller) -> None:
        self.Controller = Controller

        self.DataModel = DataModel(self.Controller)
        
        
        self.FileSystemModel = QtWidgets.QFileSystemModel()
        self.FileSystemModel.setRootPath('')
        
        self.JsonModel = JsonModel()
        

