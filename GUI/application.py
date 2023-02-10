# -*- coding: utf-8 -*-



from app.controllers.controller import Controller, logging



class Lilly(object):
    
    
    def __init__(self, logger : logging.Logger, struct):
        
        super(Lilly, self).__init__()
        
        self.__logger = logger
        
        self.__Controller = Controller(self.__logger)
        self.__Controller.set_struct(struct)




    def execute(self):
        try:
            
            return self.__Controller.main()
        
        except Exception as exception:
            return self.logger.critical(exception)