# -*- coding: utf-8 -*-


from app.views.main_view import MainView
from app.views.receiver_view import ReceiverView
from app.views.editor_view import EditorView
from app.views.progress_view import ProgressView


from PyQt5 import (
    QtCore,
    QtWidgets
)

import time


_translate = QtCore.QCoreApplication.translate


scrollbar_stylesheet = '''
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


class View(object):
    def __init__(self, Controller, logger):
        super(View, self).__init__()

        self.Controller = Controller

        self.logger = logger

        self.MainView = MainView(self.Controller)
        self.ReceiverView = ReceiverView()
        self.EditorView = EditorView(self.Controller)
        self.ProgressView = ProgressView()

    def get_main(self):

        try:
            self.MainView.setupUi()

            def window_title():
                return self.MainView.labelTitleBar.setText(
                    f'''{time.asctime()} - Menu'''
                )

            self.timer = QtCore.QTimer(self.MainView)

            self.timer.timeout.connect(window_title)
            self.timer.start(1000)

            self.Controller.window_title_bar_restore(self.MainView)

            self.MainView.stackedWidget.setCurrentWidget(
                self.MainView.homeWidget)

            self.MainView.pushButtonCloseWindow.clicked.connect(
                QtWidgets.qApp.quit)

            self.MainView.pushButtonMinimizeWindow.clicked.connect(
                self.MainView.showMinimized)

            self.MainView.pushButtonRestoreWindow.clicked.connect(
                lambda: self.Controller.window_status_restore(self.MainView))

            self.MainView.pushButtonSwipeSidebar.clicked.connect(
                self.Controller.swipe_sidebar)

            self.MainView.pushButtonHome.clicked.connect(
                lambda: self.MainView.stackedWidget.setCurrentWidget(self.MainView.homeWidget))

            self.MainView.pushButtonAPI.clicked.connect(
                lambda: self.MainView.stackedWidget.setCurrentWidget(self.MainView.APIWidget))

            self.MainView.pushButtonWorkspace.clicked.connect(
                lambda: self.MainView.stackedWidget.setCurrentWidget(self.MainView.workspaceWidget))

            self.MainView.pushButtonSettings.clicked.connect(
                self.Controller.get_log)

            self.MainView.lineEditSelectedFile.setEnabled(False)

            self.MainView.pushButtonRequestData.clicked.connect(
                self.Controller.get_api_data_receiver)

            self.MainView.pushButtonSaveRequestedData.clicked.connect(
                self.Controller.save_requested_data)

            self.MainView.pushButtonExecuteSelectedFile.clicked.connect(
                self.Controller.execute_selected_file)

            self.MainView.pushButtonSelectDirectory.clicked.connect(
                self.Controller.select_directory)
            self.MainView.pushButtonSelectFile.clicked.connect(
                self.Controller.select_file)

            self.MainView.pushButtonConvertJSONToXLSX.clicked.connect(
                self.Controller.convert_json_to_xlsx)

            self.Controller.system_file_browser()

            self.MainView.radioButtonLightMode.toggled.connect(self.mode)
            self.MainView.radioButtonDarkMode.toggled.connect(self.mode)

            self.MainView.radioButtonLightMode.setChecked(True)


            self.MainView.treeViewSystem.setAnimated(True)
            self.MainView.treeViewSystem.setIndentation(20)
            self.MainView.treeViewSystem.setSortingEnabled(True)

            self.MainView.treeViewRequestData.setSortingEnabled(True)
            self.MainView.treeViewRequestData.setAnimated(True)
            self.MainView.treeViewRequestData.setIndentation(20)

            self.MainView.treeViewSystem.horizontalScrollBar().setStyleSheet(scrollbar_stylesheet)
            self.MainView.treeViewSystem.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
            self.MainView.treeViewRequestData.horizontalScrollBar(
            ).setStyleSheet(scrollbar_stylesheet)
            self.MainView.treeViewRequestData.verticalScrollBar(
            ).setStyleSheet(scrollbar_stylesheet)

            self.MainView.listViewFile.horizontalScrollBar().setStyleSheet(scrollbar_stylesheet)
            self.MainView.listViewFile.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
            self.MainView.listViewFile.setEditTriggers(
                QtWidgets.QAbstractItemView.NoEditTriggers)
            self.MainView.listViewFile.doubleClicked.connect(lambda: self.MainView.lineEditSelectedFile.setText(
                self.MainView.listViewFile.currentIndex().data(QtCore.Qt.DisplayRole)))

            self.MainView.listViewFileHistory.horizontalScrollBar(
            ).setStyleSheet(scrollbar_stylesheet)
            self.MainView.listViewFileHistory.verticalScrollBar(
            ).setStyleSheet(scrollbar_stylesheet)
            self.MainView.listViewFileHistory.setEditTriggers(
                QtWidgets.QAbstractItemView.NoEditTriggers)

            self.MainView.listViewLog.horizontalScrollBar().setStyleSheet(scrollbar_stylesheet)
            self.MainView.listViewLog.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)
            self.MainView.listViewLog.setEditTriggers(
                QtWidgets.QAbstractItemView.NoEditTriggers)

            self.MainView.lineEditSelectedFile.setAlignment(
                QtCore.Qt.AlignCenter)
            self.MainView.lineEditSearcher.setAlignment(QtCore.Qt.AlignCenter)
            self.MainView.lineEditSearcher.textChanged.connect(self.search)
            self.MainView.lineEditSearcher.returnPressed.connect(
                lambda: self.search(self.MainView.lineEditSearcher.text()))
            self.MainView.pushButtonSearch.clicked.connect(
                lambda: self.search(self.MainView.lineEditSearcher.text()))

            self.MainView.lineEditSearcher.setPlaceholderText(
                'Ingresa el nombre de la llave')

            return self.MainView.show()

        except Exception as exception:
            return self.logger.critical(exception)

    def get_receiver(self, title: str):

        try:
            self.ReceiverView.setupUi()

            self.ReceiverView.lineEditData.setAlignment(QtCore.Qt.AlignCenter)
            self.ReceiverView.labelTitle.setText(
                _translate('MainWindow', title)
            )

            return self.ReceiverView.show()

        except Exception as exception:
            return self.logger.critical(exception)

    def get_editor(self, content):

        try:

            self.EditorView.setupUi()

            self.Controller.window_title_bar_restore(self.EditorView)

            self.EditorView.pushButtonCloseWindow.clicked.connect(
                self.EditorView.close)

            self.EditorView.pushButtonMinimizeWindow.clicked.connect(
                self.EditorView.showMinimized)

            self.EditorView.pushButtonRestoreWindow.clicked.connect(
                lambda: self.Controller.window_status_restore(self.EditorView))

            self.EditorView.textEditJson.setText(str(content))
            self.EditorView.textEditJson.horizontalScrollBar().setStyleSheet(scrollbar_stylesheet)

            self.EditorView.textEditJson.verticalScrollBar().setStyleSheet(scrollbar_stylesheet)

            return self.EditorView.show()

        except Exception as exception:
            return self.logger.critical(exception)

    def get_progress(self):

        try:

            self.ProgressView.setupUi()

            self.ProgressView.setWindowTitle('Progreso')
            self.ProgressView.setMaximumSize(800, 150)
            self.ProgressView.setMinimumSize(800, 150)

            return self.ProgressView.show()

        except Exception as exception:
            return self.logger.critical(exception)

    def mode(self):
        try:
            if self.MainView.radioButtonLightMode.isChecked():

                self.MainView.frameHomeContainer.setStyleSheet("QFrame {\n"
                                                               "    background-color : #FFFFFF;\n"
                                                               "}")
                self.MainView.frameAPIContainer.setStyleSheet("QFrame {\n"
                                                              "    background-color : #FFFFFF;\n"
                                                              "}")
                self.MainView.frameWorkspaceContainer.setStyleSheet("QFrame {\n"
                                                                    "    background-color : #FFFFFF;\n"
                                                                    "}")
                self.MainView.frameSettingsContainer.setStyleSheet("QFrame {\n"
                                                                   "    background-color : #FFFFFF;\n"
                                                                   "}")

                self.MainView.frameDataSearcher.setStyleSheet("QFrame {\n"
                                                              "    background-color : #FFFFFF;\n"
                                                              "}")
                self.MainView.frameAPIContainer.setStyleSheet("QFrame {\n"
                                                              "    background-color : #FFFFFF;\n"
                                                              "}")
                self.MainView.frameAPIContent.setStyleSheet("QFrame {\n"
                                                            "    background-color : #FFFFFF;\n"
                                                            "}")
                self.MainView.frameAPIRequest.setStyleSheet("QFrame {\n"
                                                            "    background-color : #FFFFFF;\n"
                                                            "}")
                self.MainView.frameAPIRequestContent.setStyleSheet("QFrame {\n"
                                                                   "    background-color : #FFFFFF;\n"
                                                                   "}")

                self.MainView.labelHomeTitle.setStyleSheet("QLabel{\n"
                                                           "    background-color: #3A609B;\n"
                                                           "    font : 77 17pt \"Microsoft JhengHei UI\" ;\n"
                                                           "    color : #FFFFFF;\n"
                                                           "    border-radius : 0px;\n"
                                                           "    text-align : left;\n"
                                                           "    padding: 10px;\n"
                                                           "}\n"
                                                           "")
                self.MainView.labelApiTitle.setStyleSheet("QLabel{\n"
                                                          "    background-color: #3A609B;\n"
                                                          "    font : 77 17pt \"Microsoft JhengHei UI\" ;\n"
                                                          "    color : #FFFFFF;\n"
                                                          "    border-radius : 0px;\n"
                                                          "    text-align : left;\n"
                                                          "    padding: 10px;\n"
                                                          "}\n"
                                                          "")
                self.MainView.labelWorkspaceTitle.setStyleSheet("QLabel{\n"
                                                                "    background-color: #3A609B;\n"
                                                                "    font : 77 17pt \"Microsoft JhengHei UI\" ;\n"
                                                                "    color : #FFFFFF;\n"
                                                                "    border-radius : 0px;\n"
                                                                "    text-align : left;\n"
                                                                "    padding: 10px;\n"
                                                                "}\n"
                                                                "")
                self.MainView.labelSettingsTitle.setStyleSheet("QLabel{\n"
                                                               "    background-color: #3A609B;\n"
                                                               "    font : 77 17pt \"Microsoft JhengHei UI\" ;\n"
                                                               "    color : #FFFFFF;\n"
                                                               "    border-radius : 0px;\n"
                                                               "    text-align : left;\n"
                                                               "    padding: 10px;\n"
                                                               "}\n"
                                                               "")

                self.MainView.lineEditSelectedFile.setStyleSheet("QLineEdit {\n"
                                                                 "    font: 25 13pt \"Microsoft YaHei UI\";\n"
                                                                 "    background-color : #FFFFFF;\n"
                                                                 "    color : #5F3E77;\n"
                                                                 "    border : 1px solid #5F3E77;\n"
                                                                 "    border-radius : 15px;\n"
                                                                 "}")
                self.MainView.lineEditSearcher.setStyleSheet("QLineEdit {\n"
                                                             "    font: 25 12pt \"Microsoft YaHei UI\";\n"
                                                             "    background-color : #FFFFFF;\n"
                                                             "    color : #5F3E77;\n"
                                                             "    border : 1px solid #5F3E77;\n"
                                                             "    border-radius : 15px;\n"
                                                             "}\n"
                                                             "\n"
                                                             "QLineEdit::hover{\n"
                                                             "    background-color: #DDDDDD;\n"
                                                             "    border : 1px solid #5F3E77;\n"
                                                             "}")

                self.MainView.treeViewSystem.setStyleSheet("QTreeView {\n"
                                                           "\n"
                                                           "    background-color : #DDDDDD;\n"
                                                           "\n"
                                                           "    font: 25 12pt \"Microsoft YaHei UI Light\";\n"
                                                           "    color : #121212;\n"
                                                           "\n"
                                                           "    border : 1px solid #5F3E77;\n"
                                                           "\n"
                                                           "}\n"
                                                           "\n"
                                                           "QHeaderView::section {\n"
                                                           "    background-color : #5F3E77;\n"
                                                           "    font: 25 10pt \"Microsoft YaHei UI Light\" bold;\n"
                                                           "    color : #FFFFFF;\n"
                                                           "    border-radius : 0px;\n"
                                                           "    text-align : left;\n"
                                                           "}")

                self.MainView.treeViewRequestData.setStyleSheet("QTreeView {\n"
                                                                "    background-color : #DDDDDD;\n"
                                                                "    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
                                                                "    color : #D37242;\n"
                                                                "    border-radius : 0px;\n"
                                                                "    padding-left : 50px;\n"
                                                                "    text-align : left;\n"
                                                                "}\n"
                                                                "\n"
                                                                "QHeaderView::section {\n"
                                                                "    background-color : #6178B2;\n"
                                                                "    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
                                                                "    color : #FFFFFF;\n"
                                                                "    border-radius : 0px;\n"
                                                                "    text-align : left;\n"
                                                                "}")

                self.MainView.listViewFileHistory.setStyleSheet("QListView {\n"
                                                                "\n"
                                                                "    background-color : #DDDDDD;\n"
                                                                "\n"
                                                                "    font: 25 12pt \"Microsoft YaHei UI Light\";\n"
                                                                "    color : #5F3E77;\n"
                                                                "\n"
                                                                "    border : 1px solid #5F3E77;\n"
                                                                "\n"
                                                                "}\n"
                                                                "\n"
                                                                "QHeaderView::section {\n"
                                                                "    background-color : #5F3E77;\n"
                                                                "    font: 25 10pt \"Microsoft YaHei UI Light\" bold;\n"
                                                                "    color : #FFFFFF;\n"
                                                                "    border-radius : 0px;\n"
                                                                "    text-align : left;\n"
                                                                "}")

                self.MainView.listViewFile.setStyleSheet("QListView {\n"
                                                         "\n"
                                                         "    background-color : #DDDDDD;\n"
                                                         "\n"
                                                         "    font: 25 12pt \"Microsoft YaHei UI Light\";\n"
                                                         "    color : #5F3E77;\n"
                                                         "\n"
                                                         "    border : 1px solid #5F3E77;\n"
                                                         "\n"
                                                         "}\n"
                                                         "\n"
                                                         "QHeaderView::section {\n"
                                                         "    background-color : #5F3E77;\n"
                                                         "    font: 25 10pt \"Microsoft YaHei UI Light\" bold;\n"
                                                         "    color : #FFFFFF;\n"
                                                         "    border-radius : 0px;\n"
                                                         "    text-align : left;\n"
                                                         "}")

                self.MainView.listViewLog.setStyleSheet("QListView {\n"
                                                        "\n"
                                                        "    background-color : #DDDDDD;\n"
                                                        "\n"
                                                        "    font: 25 12pt \"Microsoft YaHei UI Light\";\n"
                                                        "    color : #5F3E77;\n"
                                                        "\n"
                                                        "    border : 1px solid #5F3E77;\n"
                                                        "\n"
                                                        "}\n"
                                                        "\n"
                                                        "QHeaderView::section {\n"
                                                        "    background-color : #5F3E77;\n"
                                                        "    font: 25 10pt \"Microsoft YaHei UI Light\" bold;\n"
                                                        "    color : #FFFFFF;\n"
                                                        "    border-radius : 0px;\n"
                                                        "    text-align : left;\n"
                                                        "}")

                self.MainView.radioButtonDarkMode.setStyleSheet("QRadioButton {\n"
                                                                "    font : 75 11pt \"Microsoft JhengHei UI\"  bold;\n"
                                                                "    color : #121212;\n"
                                                                "    border-radius : 0px;\n"
                                                                "}\n"
                                                                "\n"
                                                                "QRadioButton:hover {\n"
                                                                "    color : #3A609B;\n"
                                                                "    border-radius : 0px;\n"
                                                                "}\n"
                                                                "\n"
                                                                "QRadioButton::checked {\n"
                                                                "    color : #3A609B;\n"
                                                                "    border-radius : 0px;\n"
                                                                "}\n"
                                                                "\n"
                                                                "QRadioButton::indicator {\n"
                                                                "    color : #3A609B;\n"
                                                                "}\n"
                                                                "\n"
                                                                "QRadioButton::indicator:checked:pressed {\n"
                                                                "    color : #3A609B;\n"
                                                                "}")

                self.MainView.radioButtonLightMode.setStyleSheet("QRadioButton {\n"
                                                                 "    font : 75 11pt \"Microsoft JhengHei UI\"  bold;\n"
                                                                 "    color : #121212;\n"
                                                                 "    border-radius : 0px;\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "QRadioButton:hover {\n"
                                                                 "    color : #3A609B;\n"
                                                                 "    border-radius : 0px;\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "QRadioButton::checked {\n"
                                                                 "    color : #3A609B;\n"
                                                                 "    border-radius : 0px;\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "QRadioButton::indicator {\n"
                                                                 "    color : #3A609B;\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "QRadioButton::indicator:checked:pressed {\n"
                                                                 "    color : #3A609B;\n"
                                                                 "}")

            elif self.MainView.radioButtonDarkMode.isChecked():
                self.MainView.frameHomeContainer.setStyleSheet("QFrame {\n"
                                                               "    background-color : #121212;\n"
                                                               "}")
                self.MainView.frameAPIContainer.setStyleSheet("QFrame {\n"
                                                              "    background-color : #121212;\n"
                                                              "}")
                self.MainView.frameWorkspaceContainer.setStyleSheet("QFrame {\n"
                                                                    "    background-color : #121212;\n"
                                                                    "}")
                self.MainView.frameSettingsContainer.setStyleSheet("QFrame {\n"
                                                                   "    background-color : #121212;\n"
                                                                   "}")

                self.MainView.frameDataSearcher.setStyleSheet("QFrame {\n"
                                                              "    background-color : #121212;\n"
                                                              "}")
                self.MainView.frameAPIContainer.setStyleSheet("QFrame {\n"
                                                              "    background-color : #121212;\n"
                                                              "}")
                self.MainView.frameAPIContent.setStyleSheet("QFrame {\n"
                                                            "    background-color : #121212;\n"
                                                            "}")
                self.MainView.frameAPIRequest.setStyleSheet("QFrame {\n"
                                                            "    background-color : #121212;\n"
                                                            "}")
                self.MainView.frameAPIRequestContent.setStyleSheet("QFrame {\n"
                                                                   "    background-color : #121212;\n"
                                                                   "}")

                self.MainView.labelHomeTitle.setStyleSheet("QLabel{\n"
                                                           "    background-color: #222222;\n"
                                                           "    font : 77 17pt \"Microsoft JhengHei UI\" ;\n"
                                                           "    color : #FFFFFF;\n"
                                                           "    border-radius : 0px;\n"
                                                           "    text-align : left;\n"
                                                           "    padding: 10px;\n"
                                                           "}\n"
                                                           "")
                self.MainView.labelApiTitle.setStyleSheet("QLabel{\n"
                                                          "    background-color: #222222;\n"
                                                          "    font : 77 17pt \"Microsoft JhengHei UI\" ;\n"
                                                          "    color : #FFFFFF;\n"
                                                          "    border-radius : 0px;\n"
                                                          "    text-align : left;\n"
                                                          "    padding: 10px;\n"
                                                          "}\n"
                                                          "")
                self.MainView.labelWorkspaceTitle.setStyleSheet("QLabel{\n"
                                                                "    background-color: #222222;\n"
                                                                "    font : 77 17pt \"Microsoft JhengHei UI\" ;\n"
                                                                "    color : #FFFFFF;\n"
                                                                "    border-radius : 0px;\n"
                                                                "    text-align : left;\n"
                                                                "    padding: 10px;\n"
                                                                "}\n"
                                                                "")
                self.MainView.labelSettingsTitle.setStyleSheet("QLabel{\n"
                                                               "    background-color: #222222;\n"
                                                               "    font : 77 17pt \"Microsoft JhengHei UI\" ;\n"
                                                               "    color : #FFFFFF;\n"
                                                               "    border-radius : 0px;\n"
                                                               "    text-align : left;\n"
                                                               "    padding: 10px;\n"
                                                               "}\n"
                                                               "")

                self.MainView.lineEditSelectedFile.setStyleSheet("QLineEdit {\n"
                                                                 "    font: 25 13pt \"Microsoft YaHei UI\";\n"
                                                                 "    background-color : #222222;\n"
                                                                 "    color : #5F3E77;\n"
                                                                 "    border : 1px solid #5F3E77;\n"
                                                                 "    border-radius : 15px;\n"
                                                                 "}")
                self.MainView.lineEditSearcher.setStyleSheet("QLineEdit {\n"
                                                             "    font: 25 12pt \"Microsoft YaHei UI\";\n"
                                                             "    background-color : #222222;\n"
                                                             "    color : #5F3E77;\n"
                                                             "    border : 1px solid #5F3E77;\n"
                                                             "    border-radius : 15px;\n"
                                                             "}\n"
                                                             "\n"
                                                             "QLineEdit::hover{\n"
                                                             "    background-color: #121212;\n"
                                                             "    border : 1px solid #5F3E77;\n"
                                                             "}")

                self.MainView.treeViewSystem.setStyleSheet("QTreeView {\n"
                                                           "\n"
                                                           "    background-color : #222222;\n"
                                                           "\n"
                                                           "    font: 25 12pt \"Microsoft YaHei UI Light\";\n"
                                                           "    color : #FFFFFF;\n"
                                                           "\n"
                                                           "    border : 1px solid #5F3E77;\n"
                                                           "\n"
                                                           "}\n"
                                                           "\n"
                                                           "QHeaderView::section {\n"
                                                           "    background-color : #5F3E77;\n"
                                                           "    font: 25 10pt \"Microsoft YaHei UI Light\" bold;\n"
                                                           "    color : #FFFFFF;\n"
                                                           "    border-radius : 0px;\n"
                                                           "    text-align : left;\n"
                                                           "}")

                self.MainView.treeViewRequestData.setStyleSheet("QTreeView {\n"
                                                                "    background-color : #222222;\n"
                                                                "    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
                                                                "    color : #D37242;\n"
                                                                "    border-radius : 0px;\n"
                                                                "    padding-left : 50px;\n"
                                                                "    text-align : left;\n"
                                                                "}\n"
                                                                "\n"
                                                                "QHeaderView::section {\n"
                                                                "    background-color : #6178B2;\n"
                                                                "    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
                                                                "    color : #FFFFFF;\n"
                                                                "    border-radius : 0px;\n"
                                                                "    text-align : left;\n"
                                                                "}")

                self.MainView.listViewFileHistory.setStyleSheet("QListView {\n"
                                                                "\n"
                                                                "    background-color : #222222;\n"
                                                                "\n"
                                                                "    font: 25 12pt \"Microsoft YaHei UI Light\";\n"
                                                                "    color : #FFFFFF;\n"
                                                                "\n"
                                                                "    border : 1px solid #5F3E77;\n"
                                                                "\n"
                                                                "}\n"
                                                                "\n"
                                                                "QHeaderView::section {\n"
                                                                "    background-color : #5F3E77;\n"
                                                                "    font: 25 10pt \"Microsoft YaHei UI Light\" bold;\n"
                                                                "    color : #FFFFFF;\n"
                                                                "    border-radius : 0px;\n"
                                                                "    text-align : left;\n"
                                                                "}")

                self.MainView.listViewFile.setStyleSheet("QListView {\n"
                                                         "\n"
                                                         "    background-color : #222222;\n"
                                                         "\n"
                                                         "    font: 25 12pt \"Microsoft YaHei UI Light\";\n"
                                                         "    color : #FFFFFF;\n"
                                                         "\n"
                                                         "    border : 1px solid #5F3E77;\n"
                                                         "\n"
                                                         "}\n"
                                                         "\n"
                                                         "QHeaderView::section {\n"
                                                         "    background-color : #5F3E77;\n"
                                                         "    font: 25 10pt \"Microsoft YaHei UI Light\" bold;\n"
                                                         "    color : #FFFFFF;\n"
                                                         "    border-radius : 0px;\n"
                                                         "    text-align : left;\n"
                                                         "}")

                self.MainView.listViewLog.setStyleSheet("QListView {\n"
                                                        "\n"
                                                        "    background-color : #222222;\n"
                                                        "\n"
                                                        "    font: 25 12pt \"Microsoft YaHei UI Light\";\n"
                                                        "    color : #FFFFFF;\n"
                                                        "\n"
                                                        "    border : 1px solid #5F3E77;\n"
                                                        "\n"
                                                        "}\n"
                                                        "\n"
                                                        "QHeaderView::section {\n"
                                                        "    background-color : #5F3E77;\n"
                                                        "    font: 25 10pt \"Microsoft YaHei UI Light\" bold;\n"
                                                        "    color : #FFFFFF;\n"
                                                        "    border-radius : 0px;\n"
                                                        "    text-align : left;\n"
                                                        "}")

                self.MainView.radioButtonDarkMode.setStyleSheet("QRadioButton {\n"
                                                                "    font : 75 11pt \"Microsoft JhengHei UI\"  bold;\n"
                                                                "    color : #FFFFFF;\n"
                                                                "    border-radius : 0px;\n"
                                                                "}\n"
                                                                "\n"
                                                                "QRadioButton:hover {\n"
                                                                "    color : #3A609B;\n"
                                                                "    border-radius : 0px;\n"
                                                                "}\n"
                                                                "\n"
                                                                "QRadioButton::checked {\n"
                                                                "    color : #3A609B;\n"
                                                                "    border-radius : 0px;\n"
                                                                "}\n"
                                                                "\n"
                                                                "QRadioButton::indicator {\n"
                                                                "    color : #3A609B;\n"
                                                                "}\n"
                                                                "\n"
                                                                "QRadioButton::indicator:checked:pressed {\n"
                                                                "    color : #3A609B;\n"
                                                                "}")

                self.MainView.radioButtonLightMode.setStyleSheet("QRadioButton {\n"
                                                                 "    font : 75 11pt \"Microsoft JhengHei UI\"  bold;\n"
                                                                 "    color : #FFFFFF;\n"
                                                                 "    border-radius : 0px;\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "QRadioButton:hover {\n"
                                                                 "    color : #3A609B;\n"
                                                                 "    border-radius : 0px;\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "QRadioButton::checked {\n"
                                                                 "    color : #3A609B;\n"
                                                                 "    border-radius : 0px;\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "QRadioButton::indicator {\n"
                                                                 "    color : #3A609B;\n"
                                                                 "}\n"
                                                                 "\n"
                                                                 "QRadioButton::indicator:checked:pressed {\n"
                                                                 "    color : #3A609B;\n"
                                                                 "}")

        except Exception as exception:
            return self.logger.critical(exception)

    def search(self, text):

        try:
            row_count = self.MainView.treeViewRequestData.model().rowCount()
            column_count = self.MainView.treeViewRequestData.model().columnCount()
            model = self.MainView.treeViewRequestData.model()

            for row in range(row_count):
                # Row | Column

                if text in str(model.index(row, 0, QtCore.QModelIndex()).data(QtCore.Qt.DisplayRole)):
                    self.MainView.treeViewRequestData.expand(
                        model.index(row, 0, QtCore.QModelIndex()))

                else:
                    self.MainView.treeViewRequestData.collapse(
                        model.index(row, 0, QtCore.QModelIndex()))

        except Exception as exception:
            return self.logger.critical(exception)
