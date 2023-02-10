

import sys
import os
import shutil

from PyQt5 import QtWidgets
from app.controllers.controller import Controller


'''

API DE PRUEBA

https://jsonplaceholder.typicode.com/users


http://127.0.0.1:8000/api

'''


execution_path =\
    os.path.dirname(os.path.abspath(__file__))


app_path =\
    os.path.join(execution_path, 'app')
    

controllers_path =\
    os.path.join(app_path, 'controllers')
    

models_path =\
    os.path.join(app_path, 'models')


views_path =\
    os.path.join(app_path, 'views')


resources_path =\
    os.path.join(app_path, 'resources')



struct = {
    'app' : {
        'controller' : controllers_path,
        'models' : models_path,
        'views' : views_path,
        'resources' : resources_path
    }
}




for directory in struct['app'].values():
    pycache_path =\
        os.path.join(directory, '__pycache__')

    if os.path.exists(pycache_path):
        shutil.rmtree(pycache_path)



qApp = QtWidgets.QApplication(sys.argv)


controller = Controller()

controller.get_menu_view()


sys.exit(qApp.exec_())
