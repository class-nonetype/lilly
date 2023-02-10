# -*- coding: utf-8 -*-


import sys
import os
import shutil
import logging



from PyQt5 import QtWidgets


from application import Lilly




global struct
global logger

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

log_path =\
    os.path.join(app_path, 'log')



struct = {
    'app' : {
        'executioon' : execution_path,
        'controller' : controllers_path,
        'models' : models_path,
        'views' : views_path,
        'resources' : resources_path,
        'log' : {
            'directory' : log_path
        }
    }
}




for directory in struct['app'].values():
    try:
        pycache_path =\
            os.path.join(directory, '__pycache__')
    
    except TypeError:
        pass

    if os.path.exists(pycache_path):
        shutil.rmtree(pycache_path)
        

if not os.path.exists(struct['app']['log']['directory']):
    os.mkdir(struct['app']['log']['directory'])




logger = logging.getLogger('Logger')

log_file_path = os.path.normpath(os.path.join(struct['app']['log']['directory'], 'LOG.log'))
struct['app']['log'].update({'file' : log_file_path})


logging.basicConfig(
    filename    = struct['app']['log']['file'],
    level       = logging.DEBUG,
    encoding    = 'utf-8',
    format      = '%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt     = '%Y-%m-%d %H:%M:%S',
)

log_formatter = logging.Formatter(
    fmt='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(log_formatter)

logger.addHandler(console_handler)

logger.info('Logger instanciado.')




qApp = QtWidgets.QApplication(sys.argv)

Lilly(logger, struct).execute()

sys.exit(qApp.exec_())
