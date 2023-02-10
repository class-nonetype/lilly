





from app.views.main_view import MainView
from app.views.receiver_view import ReceiverView


from PyQt5 import (
    QtCore,
    QtWidgets
)

import time



_translate = QtCore.QCoreApplication.translate


class View(object):
    def __init__(self, Controller):
        super(View, self).__init__()
        
        
        self.Controller = Controller
        
        self.MainView = MainView(self.Controller)
        self.ReceiverView = ReceiverView()
        
        
        
    
    def get_menu(self):
        
        self.MainView.setupUi()
        
        def window_title():
            self.MainView.labelTitleBar.setText(
                f'''{time.asctime()} - Menu'''
            )
        
        self.timer = QtCore.QTimer(self.MainView)

        self.timer.timeout.connect(window_title)
        self.timer.start(1000)
        
        self.Controller.window_title_bar_restore()
        
        
        
        self.MainView.stackedWidget.setCurrentWidget(self.MainView.homeWidget)

        self.MainView.pushButtonCloseWindow.clicked.connect(QtWidgets.qApp.quit)
        self.MainView.pushButtonMinimizeWindow.clicked.connect(self.MainView.showMinimized)
        self.MainView.pushButtonRestoreWindow.clicked.connect(lambda : self.Controller.window_status_restore())


        self.MainView.pushButtonSwipeSidebar.clicked.connect(self.Controller.swipe_sidebar)
        
        self.MainView.pushButtonHome.clicked.connect(
            lambda : self.MainView.stackedWidget.setCurrentWidget(self.MainView.homeWidget))
        
        self.MainView.pushButtonAPI.clicked.connect(
            lambda : self.MainView.stackedWidget.setCurrentWidget(self.MainView.APIWidget))
        
        self.MainView.pushButtonWorkspace.clicked.connect(
            lambda : self.MainView.stackedWidget.setCurrentWidget(self.MainView.workspaceWidget))

        self.MainView.lineEditSelectedFile.setEnabled(False)
        
        self.MainView.pushButtonRequestData.clicked.connect(self.Controller.get_api_data_receiver)
        self.MainView.pushButtonExportRequestedData.clicked.connect(self.Controller.export_data)
        
        
        self.MainView.pushButtonSaveRequestedData.clicked.connect(self.Controller.save_requested_data)

        
        
        self.Controller.system_file_browser()
        
        
        
        return self.MainView.show()


    def get_receiver(self, title : str):
        
        self.ReceiverView.setupUi()
        
        
        self.ReceiverView.lineEditData.setAlignment(QtCore.Qt.AlignCenter)
        self.ReceiverView.labelTitle.setText(
            _translate('MainWindow', title)
        )
        

        return self.ReceiverView.show()