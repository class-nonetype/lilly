# -*- coding: utf-8 -*-


from app.models.data import DataModel
from app.models.json_tree import JsonModel

from PyQt5 import (
    QtWidgets)

import os
import logging





class Model(object):
    
    def __init__(self, Controller, logger : logging.Logger) -> None:
        self.Controller = Controller

        self.logger = logger

        self.DataModel = DataModel(self.logger)

        
        
        self.FileSystemModel = QtWidgets.QFileSystemModel()
        self.FileSystemModel.setRootPath('')
        
        self.JsonModel = JsonModel()
        
        

    def set_struct(self, struct):
        self.struct = struct
        
        return self.struct

