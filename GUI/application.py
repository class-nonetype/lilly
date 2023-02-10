


from app.controllers.controller import Controller, logging



class Lilly:
    
    
    def __init__(self, logger : logging.Logger, struct):
        
        self.__logger = logger
        
        self.__Controller = Controller(self.__logger)
        self.__Model = self.__Controller.Model
        self.__Model.set_struct(struct)
        self.__View = self.__Controller.View
    
    
    def execute(self):
        return self.__Controller.get_main_view()

    
    def __str__(self) -> str:
        return '{0}\n{1}\n{2}'.format(self.__Model, self.__View, self.__Controller)