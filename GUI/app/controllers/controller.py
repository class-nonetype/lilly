





from app.views.view import View
from app.models.model import Model


from PyQt5 import QtCore, QtGui, QtWidgets



import requests
import pandas as pd



class Controller(object):
    
    
    
    def __init__(self):
        
        super(Controller, self).__init__()
        
        
        self.View = View(self)
        self.Model = Model(self)
    
    
    def get_menu_view(self):
        
        return self.View.get_menu()

    def get_receiver_view(self, title : str, function):
        self.View.get_receiver(title)
        self.View.ReceiverView.pushButtonConfirm.clicked.connect(function)
        





    def window_title_bar_restore(self):
        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(8, lambda: self.window_status_restore())
                
        self.View.MainView.frameTitleBar.mouseDoubleClickEvent = dobleClickMaximizeRestore


    def window_status_restore(self):
        
        
        def window_maximize():
            return self.View.MainView.showMaximized()

        def window_minimize():
            return self.View.MainView.showNormal()
        
        if self.View.MainView.windowState() == QtCore.Qt.WindowState.WindowNoState:
            
            window_maximize()
            
            self.View.MainView.pushButtonRestoreWindow.setToolTip('Restore')
            
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap('app/resources/img/icons/24x24/cil-window-restore.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.MainView.pushButtonRestoreWindow.setIcon(icon)
            self.View.MainView.pushButtonRestoreWindow.setIconSize(QtCore.QSize(20, 20))
        
        else:
            
            window_minimize()
            
            self.View.MainView.pushButtonRestoreWindow.setToolTip('Maximize')
            
            icon = QtGui.QIcon()
            icon.addPixmap(
                QtGui.QPixmap(u'app/resources/img/icons/24x24/cil-window-maximize.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            self.View.MainView.pushButtonRestoreWindow.setIcon(icon)
            self.View.MainView.pushButtonRestoreWindow.setIconSize(QtCore.QSize(20, 20))





    def system_file_browser(self):

        FileSystemModel = QtWidgets.QFileSystemModel()
        FileSystemModel.setRootPath('')
        
        self.View.MainView.treeViewSystem.setModel(FileSystemModel)
        self.View.MainView.treeViewSystem.setAnimated(False)
        self.View.MainView.treeViewSystem.setIndentation(20)
        self.View.MainView.treeViewSystem.setSortingEnabled(True)
        
        self.View.MainView.treeViewSystem.horizontalScrollBar().setStyleSheet(
            '''
                QScrollArea {
                    border: none;
                }

                QScrollBar {
                    background: transparent;
                }

                QScrollBar:horizontal {
                    height: 13px;
                }

                QScrollBar:vertical {
                    width: 13px;
                }

                QScrollBar::handle {
                    background: #61364F;
                }

                QScrollBar::handle:horizontal {
                    height: 25px;
                    min-width: 10px;
                }

                QScrollBar::handle:vertical {
                    width: 25px;
                    min-height: 10px;
                }

                QScrollBar::add-line {
                    border: none;
                    background: none;
                }

                QScrollBar::sub-line {
                    border: none;
                    background: none;
                }
            '''
        )


        self.View.MainView.treeViewSystem.verticalScrollBar().setStyleSheet(
            '''
                QScrollArea {
                    border: none;
                }

                QScrollBar {
                    background: transparent;
                }

                QScrollBar:horizontal {
                    height: 13px;
                }

                QScrollBar:vertical {
                    width: 13px;
                }

                QScrollBar::handle {
                    background: #61364F;
                }

                QScrollBar::handle:horizontal {
                    height: 25px;
                    min-width: 10px;
                }

                QScrollBar::handle:vertical {
                    width: 25px;
                    min-height: 10px;
                }

                QScrollBar::add-line {
                    border: none;
                    background: none;
                }

                QScrollBar::sub-line {
                    border: none;
                    background: none;
                }
            '''
        )


        header = self.View.MainView.treeViewSystem.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)


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

    
    
    def __request_data(self):
        try:
            true, false, null = True, False, None

            request = requests.get(self.View.ReceiverView.lineEditData.text())
            request = eval(request.text)

            ModelItemListViewFileHistory = QtGui.QStandardItemModel()

            self.View.MainView.listViewRequest.setModel(ModelItemListViewFileHistory)
            self.View.MainView.listViewRequest.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

            for data in list(request.values()):
                item = QtGui.QStandardItem(data)

                ModelItemListViewFileHistory.appendRow(item)

            def select(index):
                true, false, null = True, False, None

                global item
                item = index.data()

                request = requests.get(item)
                request = eval(request.text)

                row_count = len(request)
                
                try:
                    for value in data:
                        value = dict(value)
                        column_count = len(value.keys())
                    
                except Exception as e:
                    column_count = len(request.keys())
                
                headers = list(request.keys())
                
                
                    
                self.View.MainView.tableWidgetRequestData.setColumnCount(column_count)
                self.View.MainView.tableWidgetRequestData.setRowCount(row_count)
                self.View.MainView.tableWidgetRequestData.setHorizontalHeaderLabels(headers)

                header = self.View.MainView.tableWidgetRequestData.horizontalHeader()

                    
                try:

                    for row in range(row_count):
                        for column in range(column_count):
                            item = (list(request[row].values())[column])
                            header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
                            set_item(row, column, item)

                except Exception as exc:
                    print(exc)

                
            def set_item(row, column, item):
                self.View.MainView.tableWidgetRequestData.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))


            self.View.MainView.listViewRequest.doubleClicked.connect(select)
            

        
        except Exception as exc:
            print(exc)
        
        
        finally:
            
            self.View.ReceiverView.destroy()


    def _request_data(self):
        try:
            true, false, null = True, False, None
            
            #self.View.ReceiverView.lineEditData.setText('https://jsonplaceholder.typicode.com/users')

            request = requests.get(
                self.View.ReceiverView.lineEditData.text()
            )
            request = eval(request.text)
            
            print(request)
            print('\n\n\n\n\n')

            ModelItemListViewFileHistory = QtGui.QStandardItemModel()

            self.View.MainView.listViewRequest.setModel(ModelItemListViewFileHistory)
            self.View.MainView.listViewRequest.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

            for data in request:
                print(data)
                
                item = QtGui.QStandardItem(data)

                ModelItemListViewFileHistory.appendRow(item)

            def select(index):
                true, false, null = True, False, None

                global selected_item
                selected_item = index.data()

                try:
                    url = self.View.ReceiverView.lineEditData.text() + '/' + str(selected_item)
                    
                    request = requests.get(url)
                    request = eval(request.text)

                    row_count = len(request)

                    for data in request:
                        data = dict(data)
                        
                        print(data)
                        column_count = len(data.keys())
                        
                    data_table(
                        row_count,
                        column_count,
                        request
                    )

                except Exception as exc:
                    print(exc)

            def data_table(row_count : int, column_count : int, data):

                row_count = (row_count)
                column_count = (column_count)
                self.View.MainView.tableWidgetRequestData.setColumnCount(column_count)
                self.View.MainView.tableWidgetRequestData.setRowCount(row_count)
                self.View.MainView.tableWidgetRequestData.setHorizontalHeaderLabels((data[0].keys()))

                __header = self.View.MainView.tableWidgetRequestData.horizontalHeader()

                global _header
                _header = list(data[0].keys())

                try:

                    for row in range(row_count):
                        #item = (str(list_value[i]))
                        for column in range(column_count):
                            item = (list(data[row].values())[column])
                            __header.setSectionResizeMode(column, QtWidgets.QHeaderView.ResizeToContents)
                            set_item(row, column, item)

                except Exception as exc:
                    print(exc)
                
            def set_item(row, column, item):
                self.View.MainView.tableWidgetRequestData.setItem(row, column, QtWidgets.QTableWidgetItem(str(item)))

            self.View.MainView.listViewRequest.doubleClicked.connect(select)

        
        except Exception as exc:
            print(exc)
            pass


    def export_data(self):

        try:
            file_name = QtWidgets.QFileDialog.getSaveFileName(self.View.MainView, 'Guardar el archivo', './', 'Libro de Excel (*.xlsx)')[0]

            exported_data = []
            processed_data = []
            counted_data = 0


            for number_rows in range(self.View.MainView.tableWidgetRequestData.model().rowCount()):
                
                cells = [

                    self.View.MainView.tableWidgetRequestData.model().data(
                        self.View.MainView.tableWidgetRequestData.model().index(number_rows, number_column), QtCore.Qt.DisplayRole)
                    for number_column in range(self.View.MainView.tableWidgetRequestData.model().columnCount())
                ]
                
                exported_data.append(cells)

            for data in exported_data:

                data = tuple(data)
                counted_data+=1
                processed_data.append(data)

                df = pd.DataFrame(processed_data)
                df.columns = _header


            excel_writer = pd.ExcelWriter(
                f'{file_name}',
                engine = 'xlsxwriter',
                engine_kwargs = {'options': {'strings_to_urls': False}}
            )
            df.to_excel(excel_writer)

            excel_writer_book = excel_writer.book
            excel_writer_sheets = excel_writer.sheets
            excel_writer_sheets = excel_writer_sheets['Sheet1']



            id_format = excel_writer_book.add_format(
                {
                    'bg_color': '#6178B2',
                    'font_color' : '#FFFFFF',
                    'font_size' : '12',
                    'font' : 'Microsoft JhengHei UI',
                    'bold':  True,
                    'align': 'left',
                    'border': 1,
                    'align': 'left',
                    'valign': 'vleft',
                    'text_wrap': True
                }
            )

            header_format = excel_writer_book.add_format(
                {
                    'bg_color': '#D37242',
                    'font_color' : '#FFFFFF',
                    'font_size' : '12',
                    'font' : 'Microsoft JhengHei UI',
                    'bold':  True,
                    'align': 'left',
                    'border': 1,
                    'align': 'left',
                    'valign': 'vleft',
                    'text_wrap': True
                }
            )

            format = excel_writer_book.add_format(
                {
                    'bg_color': '#FFFFFF',
                    'font_color' : '#6178B2',
                    'font_size' : '10',
                    'font' : 'Microsoft JhengHei UI',
                    'align': 'left',
                    'border': 1,
                    'align': 'left',
                    'valign': 'vleft',
                    'text_wrap': True
                }
            )

            excel_writer_sheets.set_column("B:B", 16, cell_format = format)
            excel_writer_sheets.set_column("C:D", 30, cell_format = format)
            excel_writer_sheets.set_column("E:F", 28, cell_format = format)
            excel_writer_sheets.set_column("G:I", 35, cell_format = format)
            excel_writer_sheets.set_column("J:K", 24, cell_format = format)
            excel_writer_sheets.set_column("L:L", 45, cell_format = format)

            for column_number, value in enumerate(df.columns.values):
                excel_writer_sheets.write(0, column_number + 1, value, header_format)

            excel_writer_sheets.conditional_format(
                f'A1:A{df.shape[0]+1}', {
                    'type': 'no_blanks','format': id_format
                }
            )
            excel_writer.save()
            
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
            self.View.MainView.labelStatusRequestedData.setText('Datos recibidos')
            self.View.ReceiverView.destroy()
        



    
    def save_requested_data(self):
        file = QtWidgets.QFileDialog.getSaveFileName(self.View.MainView, 'Guardar el archivo', './', 'Archivo JSON (*.json)')[0]
        
        return self.Model.DataModel.save_data(file)



