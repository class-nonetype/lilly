# -*- coding: utf-8 -*-


from app.views.view import View
from app.models.model import Model, os, logging


from PyQt5 import QtCore, QtGui, QtWidgets



import pandas as pd
import json
import sys


class Controller(object):
    
    
    
    def __init__(self, logger : logging.Logger):
        super(Controller, self).__init__()
        
        self.Application = QtWidgets.QApplication(sys.argv)
        
        self.logger = logger

        
        self.__View = View(self, self.logger)

        self.__Model = Model(self, self.logger)
        
        
        
        
        




    def main(self):
        self.get_main_view()
        
        
        return self.Application.exec_()
    
    
    
    def set_struct(self, struct):
        self.__Model.set_struct(struct)



    
    def get_main_view(self):
        try:
            self.__View.get_main()

            self.__View.MainView.treeViewSystem.setModel(self.__Model.FileSystemModel)


        except Exception as exception:
            
            return self.logger.critical(exception)
            

    def get_receiver_view(self, title : str, function):
        try:
            self.__View.get_receiver(title)
            self.__View.ReceiverView.pushButtonConfirm.clicked.connect(function)

        except Exception as exception:
            
            return self.logger.critical(exception)



    def get_editor_view(self, content, function):
        try:
            self.__View.get_editor(content)
            self.__View.EditorView.pushButtonSaveJson.clicked.connect(function)

        except Exception as exception:
            
            return self.logger.critical(exception)




    def window_title_bar_restore(self, component):
        try:
            def dobleClickMaximizeRestore(event):
                if event.type() == QtCore.QEvent.MouseButtonDblClick:
                    QtCore.QTimer.singleShot(8, lambda: self.window_status_restore(component))
                    
            component.frameTitleBar.mouseDoubleClickEvent = dobleClickMaximizeRestore

        except Exception as exception:
            
            return self.logger.critical(exception)



    def window_status_restore(self, component):
        try:
        
            def window_maximize():
                return component.showMaximized()

            def window_minimize():
                return component.showNormal()
            
            if component.windowState() == QtCore.Qt.WindowState.WindowNoState:
                
                window_maximize()
                
                component.pushButtonRestoreWindow.setToolTip('Restore')
                
                icon = QtGui.QIcon()
                icon.addPixmap(
                    QtGui.QPixmap('app/resources/img/icons/24x24/cil-window-restore.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                
                component.pushButtonRestoreWindow.setIcon(icon)
                component.pushButtonRestoreWindow.setIconSize(QtCore.QSize(20, 20))
            
            else:
                
                window_minimize()
                
                component.pushButtonRestoreWindow.setToolTip('Maximize')
                
                icon = QtGui.QIcon()
                icon.addPixmap(
                    QtGui.QPixmap(u'app/resources/img/icons/24x24/cil-window-maximize.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                
                component.pushButtonRestoreWindow.setIcon(icon)
                component.pushButtonRestoreWindow.setIconSize(QtCore.QSize(20, 20))


        except Exception as exception:
            
            return self.logger.critical(exception)



    def system_file_browser(self):
        
        try:
            header = self.__View.MainView.treeViewSystem.header()
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            
            self.__View.MainView.treeViewSystem.doubleClicked.connect(self.execute_file_system_file_browser)


        except Exception as exception:
            
            return self.logger.critical(exception)




    def execute_file_system_file_browser(self, index):
        try:
            self.__View.MainView.lineEditSelectedFile.setText(self.__Model.FileSystemModel.filePath(index))
            
            self.execute_selected_file()


        except Exception as exception:
            
            return self.logger.critical(exception)






    def execute_selected_file(self):
        
        try:
            file_extension = str(self.__View.MainView.lineEditSelectedFile.text()).split('.')[-1]
            
            if file_extension == 'json':
                
                with open(self.__View.MainView.lineEditSelectedFile.text(), 'r') as json_file:
                    content = json_file.read()
                    
                data = json.loads(fr'{content}')
                
                self.__View.MainView.treeViewRequestData.setModel(self.__Model.JsonModel)
                self.__Model.JsonModel.load(data)
                self.__Model.JsonModel.clear()
                self.__Model.JsonModel.load(data)
                
                assert (
                    json.dumps(self.__Model.JsonModel.json(), sort_keys=True) ==
                    json.dumps(data, sort_keys=True)
                )

                self.__View.ReceiverView.destroy()
                
                
                global data_
                data_ = json.dumps(data, indent=4, sort_keys=True)
                
                self.__View.MainView.pushButtonOpenEditor.clicked.connect(lambda : self.get_editor_view(data_, self.save_requested_data))



        except Exception as exception:
            
            return self.logger.critical(exception)




    

    def select_file(self):
        try:
            selected_file = QtWidgets.QFileDialog.getOpenFileName(
                self.__View.MainView,
                'Selecciona el archivo',
                '/',
                'Todos los archivos (*);;Archivo JSON (*.json)')
            
            self.__View.MainView.lineEditSelectedFile.setText(selected_file[0])


        except Exception as exception:
            
            return self.logger.critical(exception)







    def select_directory(self):
        try:
            selected_directory = QtWidgets.QFileDialog.getExistingDirectory(
                self.__View.MainView,
                'Selecciona el directorio',
                '/'
            )
            self.__View.MainView.lineEditSelectedFile.setText(selected_directory)
            
            
            path = []
            
            
            for root, dirs, files in os.walk(selected_directory):
                
                for file in files:
                    if str(file).split('.')[1] == 'json':
                        
                        if os.name == 'nt':
                            
                            path_found_file = root + '\\' + file
                            path_found_file = self.__Model.DataModel.convert_path_to_windows(path_found_file)
                        
                        else:
                            path_found_file = root + '/' + file
                        path.append(path_found_file)
                        
                        
                        
                        
            model = QtGui.QStandardItemModel()
            self.__View.MainView.listViewFile.setModel(model)

            for file in path:
                item = QtGui.QStandardItem(file)
                model.appendRow(item)


        except Exception as exception:
            
            return self.logger.critical(exception)




    def get_log(self):
        try:
            model = QtGui.QStandardItemModel()
            self.__View.MainView.listViewLog.setModel(model)
            
            exceptions = []
            
            with open(self.__Model.struct['app']['log']['file'], 'r') as log_file:
                exceptions.append(log_file.read().replace('\n', '" ,"'))
            log_file.close()
            
            
            exceptions = exceptions[0].split(',')
            
            for exception in exceptions:
                item = QtGui.QStandardItem(exception)
                model.appendRow(item)
                


        except Exception as exception:
            
            return self.logger.critical(exception)

        finally:
            return self.__View.MainView.stackedWidget.setCurrentWidget(self.__View.MainView.settingsWidget)

    def swipe_sidebar(self):
        try:
            if True:
                width = self.__View.MainView.frameSidebar.width()
                normal = 44

                if width == 44:
                    extend = 250
                else:
                    extend = normal

                self.animation = QtCore.QPropertyAnimation(self.__View.MainView.frameSidebar, b'minimumWidth')
                self.animation.setDuration(350)
                self.animation.setStartValue(width)
                self.animation.setEndValue(extend)
                self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                self.animation.start()


        except Exception as exception:
            
            return self.logger.critical(exception)




    

    def convert_json_to_xlsx(self):

        try:
            xlsx_file_path = QtWidgets.QFileDialog.getSaveFileName(self.__View.MainView, 'Guardar el archivo', './', 'Libro de Excel (*.xlsx)')[0]
            
            self.__Model.DataModel.convert_json_to_xlsx(
                json_file_path = self.__View.MainView.lineEditSelectedFile.text(),
                xlsx_file_path = xlsx_file_path
            )


        except Exception as exception:
            
            return self.logger.critical(exception)






    def get_api_data_receiver(self):
        
        try:
            return self.get_receiver_view(
                'Ingresa la URL de la API que deseas consultar', self.request_data
            )


        except Exception as exception:
            
            return self.logger.critical(exception)




        
    def request_data(self):
        try:
            self.__Model.DataModel.set_url(self.__View.ReceiverView.lineEditData.text())
                
            data = self.__Model.DataModel.get_data()
            
            
            if data is not None:
                
                self.__View.MainView.treeViewRequestData.setModel(self.__Model.JsonModel)
                self.__Model.JsonModel.load(data)
                self.__Model.JsonModel.clear()
                self.__Model.JsonModel.load(data)
                
                assert (
                    json.dumps(self.__Model.JsonModel.json(), sort_keys=True) ==
                    json.dumps(data, sort_keys=True)
                )

                self.__View.ReceiverView.destroy()
                
                
                global data_
                data_ = json.dumps(data, indent=4, sort_keys=True)
                
                self.__View.MainView.pushButtonOpenEditor.clicked.connect(lambda : self.get_editor_view(data_, self.save_requested_data))
            


        except Exception as exception:
            
            return self.logger.critical(exception)






    
    def save_requested_data(self):
        
        try:
            file = QtWidgets.QFileDialog.getSaveFileName(self.__View.MainView, 'Guardar el archivo', './', 'Archivo JSON (*.json)')[0]

            
            try:
                return self.__Model.DataModel.save_data(file, self.__View.EditorView.textEditJson.toPlainText())
            except Exception as exception:
                self.logger.critical(exception)
                
                try:
                    return self.__Model.DataModel.save_data(file, data_)
                except Exception as exception:
                    self.logger.critical(exception)

        except Exception as exception:
            
            return self.logger.critical(exception)





