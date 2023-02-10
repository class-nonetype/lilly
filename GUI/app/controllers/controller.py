





from app.views.view import View
from app.models.model import Model, os


from PyQt5 import QtCore, QtGui, QtWidgets



import requests
import pandas as pd
import json


class Controller(object):
    
    
    
    def __init__(self):
        
        super(Controller, self).__init__()
        
        
        self.View = View(self)
        self.Model = Model(self)
    
    
    def get_main_view(self):
        
        return self.View.get_main()

    def get_receiver_view(self, title : str, function):
        self.View.get_receiver(title)
        self.View.ReceiverView.pushButtonConfirm.clicked.connect(function)
    
    def get_editor_view(self, content, function):
        self.View.get_editor(content)
        self.View.EditorView.pushButtonSaveJson.clicked.connect(function)






    def window_title_bar_restore(self, component):
        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(8, lambda: self.window_status_restore(component))
                
        component.frameTitleBar.mouseDoubleClickEvent = dobleClickMaximizeRestore


    def window_status_restore(self, component):
        
        
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





    def system_file_browser(self):



        header = self.View.MainView.treeViewSystem.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        
        self.View.MainView.treeViewSystem.doubleClicked.connect(self.execute_file_system_file_browser)



    def execute_file_system_file_browser(self, index):

        self.View.MainView.lineEditSelectedFile.setText(self.Model.FileSystemModel.filePath(index))
        
        self.execute_selected_file()



    def execute_selected_file(self):
        
        file_extension = str(self.View.MainView.lineEditSelectedFile.text()).split('.')[-1]
        
        if file_extension == 'json':
            self.View.MainView.labelSelectedFile.setText('Archivo seleccionado')
            
            with open(self.View.MainView.lineEditSelectedFile.text(), 'r') as json_file:
                content = json_file.read()
                
            data = json.loads(fr'{content}')
            
            self.View.MainView.treeViewRequestData.setModel(self.Model.JsonModel)
            self.Model.JsonModel.load(data)
            self.Model.JsonModel.clear()
            self.Model.JsonModel.load(data)
            
            assert (
                json.dumps(self.Model.JsonModel.json(), sort_keys=True) ==
                json.dumps(data, sort_keys=True)
            )

            self.View.ReceiverView.destroy()
            
            
            global data_
            data_ = json.dumps(data, indent=4, sort_keys=True)
            
            self.View.MainView.pushButtonOpenEditor.clicked.connect(lambda : self.get_editor_view(data_, self.save_requested_data))

       
    

    def select_file(self):
        self.View.MainView.labelSelectedFile.setText('Archivo seleccionado')
        
        selected_file = QtWidgets.QFileDialog.getOpenFileName(
            self.View.MainView,
            'Selecciona el archivo',
            '/',
            'Todos los archivos (*);;Archivo JSON (*.json)')
        
        self.View.MainView.lineEditSelectedFile.setText(selected_file[0])


    def select_directory(self):
        self.View.MainView.labelSelectedFile.setText('Directorio seleccionado')
        
        selected_directory = QtWidgets.QFileDialog.getExistingDirectory(
            self.View.MainView,
            'Selecciona el directorio',
            '/'
        )
        self.View.MainView.lineEditSelectedFile.setText(selected_directory)
        
        
        path = []
        
        
        for root, dirs, files in os.walk(selected_directory):
            
            for file in files:
                if str(file).split('.')[1] == 'json':
                    
                    if os.name == 'nt':
                        
                        path_found_file = root + '\\' + file
                        path_found_file = self.Model.DataModel.convert_path_to_windows(path_found_file)
                    
                    else:
                        path_found_file = root + '/' + file
                    path.append(path_found_file)
                    
                    
                    
                    
        model = QtGui.QStandardItemModel()
        self.View.MainView.listViewFile.setModel(model)

        for file in path:
            item = QtGui.QStandardItem(file)
            model.appendRow(item)


    def swipe_sidebar(self):
        if True:
            width = self.View.MainView.frameSidebar.width()
            normal = 44

            if width == 44:
                extend = 250
            else:
                extend = normal

            self.animation = QtCore.QPropertyAnimation(self.View.MainView.frameSidebar, b'minimumWidth')
            self.animation.setDuration(350)
            self.animation.setStartValue(width)
            self.animation.setEndValue(extend)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    

    def export_data(self):

        try:
            file_name = QtWidgets.QFileDialog.getSaveFileName(self.View.MainView, 'Guardar el archivo', './', 'Libro de Excel (*.xlsx)')[0]
            print('Exportado')

        except Exception as exc:
            print(exc)
            pass


    def get_api_data_receiver(self):
        
        return self.get_receiver_view(
            'Ingresa la URL de la API que deseas consultar', self.request_data
        )
        
        
    def request_data(self):
        
        self.Model.DataModel.set_url(self.View.ReceiverView.lineEditData.text())
            
        data = self.Model.DataModel.get_data()
        
        
        if data is not None:
            
            self.View.MainView.treeViewRequestData.setModel(self.Model.JsonModel)
            self.Model.JsonModel.load(data)
            self.Model.JsonModel.clear()
            self.Model.JsonModel.load(data)
            
            assert (
                json.dumps(self.Model.JsonModel.json(), sort_keys=True) ==
                json.dumps(data, sort_keys=True)
            )

            self.View.ReceiverView.destroy()
            
            
            global data_
            data_ = json.dumps(data, indent=4, sort_keys=True)
            
            self.View.MainView.pushButtonOpenEditor.clicked.connect(lambda : self.get_editor_view(data_, self.save_requested_data))
        



    
    def save_requested_data(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self.View.MainView, 'Guardar el archivo', './', 'Archivo JSON (*.json)')[0]
        
        try:
            return self.Model.DataModel.save_data(file, self.View.EditorView.textEditJson.toPlainText())

        except Exception as exc:
            print(exc)
            
            return self.Model.DataModel.save_data(file, data_)
            

