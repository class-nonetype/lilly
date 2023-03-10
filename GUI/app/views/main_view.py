# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets


class SideGrip(QtWidgets.QWidget):

    def __init__(self, parent, edge):
        QtWidgets.QWidget.__init__(self, parent)

        # self.setStyleSheet("border : 1px solid #000000;")

        self.WidgetSideGrip = QtWidgets.QWidget(self)
        self.WidgetSideGrip.setObjectName('WidgetSideGrip')
        self.WidgetSideGrip.setStyleSheet('''
            QWidget#WidgetSideGrip {
                background: #D37242;
                border-radius: 20px;
                border: 12px solid #D37242;                   
            }
        ''')

        self.BoxLayoutSideGrip = QtWidgets.QVBoxLayout(self)
        self.BoxLayoutSideGrip.setContentsMargins(0, 0, 0, 0)
        self.BoxLayoutSideGrip.addWidget(self.WidgetSideGrip)

        if edge == QtCore.Qt.LeftEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunction = self.resizeLeft

        elif edge == QtCore.Qt.TopEdge:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunction = self.resizeTop

        elif edge == QtCore.Qt.RightEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunction = self.resizeRight

        else:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunction = self.resizeBottom

        self.mousePos = None

    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunction(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None


class MainView(QtWidgets.QMainWindow):
    _gripSize = 1

    def __init__(self, Controller):
        super().__init__()

        self.Controller = Controller

        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint |
                            QtCore.Qt.FramelessWindowHint)
        self.sideGrips = [
            SideGrip(self, QtCore.Qt.LeftEdge),
            SideGrip(self, QtCore.Qt.TopEdge),
            SideGrip(self, QtCore.Qt.RightEdge),
            SideGrip(self, QtCore.Qt.BottomEdge),
        ]
        self.cornerGrips = [QtWidgets.QSizeGrip(self) for i in range(4)]

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
                                  -self.gripSize, -self.gripSize)

        # top left
        self.cornerGrips[0].setGeometry(
            QtCore.QRect(outRect.topLeft(), inRect.topLeft()))

        # top right
        self.cornerGrips[1].setGeometry(
            QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized())

        # bottom right
        self.cornerGrips[2].setGeometry(
            QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))

        # bottom left
        self.cornerGrips[3].setGeometry(
            QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        # left edge
        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())

        # top edge
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)

        # right edge
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(),
            inRect.top(), self.gripSize, inRect.height())

        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(),
            inRect.width(), self.gripSize)

    def closeEvent(self, event):
        self.destroy()

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        self.updateGrips()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos()-self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() and QtCore.Qt.LeftButton:
                self.move(event.globalPos()-self.m_DragPosition)
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        self.m_drag = False

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            QtWidgets.qApp.quit()

        elif event.key() == QtCore.Qt.Key_F1:
            self.stackedWidget.setCurrentWidget(self.homeWidget)

        elif event.key() == QtCore.Qt.Key_F2:
            self.stackedWidget.setCurrentWidget(self.APIWidget)

        elif event.key() == QtCore.Qt.Key_F3:
            self.stackedWidget.setCurrentWidget(self.workspaceWidget)

        elif event.key() == QtCore.Qt.Key_F4:
            self.Controller.get_log()

        elif event.key() == QtCore.Qt.Key_F7:
            self.radioButtonLightMode.setChecked(True)

        elif event.key() == QtCore.Qt.Key_F8:
            self.radioButtonDarkMode.setChecked(True)

        else:
            super().keyPressEvent(event)

    def setupUi(self):
        if self.objectName():
            self.setObjectName(u"MainWindow")

        self.setEnabled(True)
        self.resize(800, 600)

        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frameTitleBar = QtWidgets.QFrame(parent=self.centralwidget)
        self.frameTitleBar.setMinimumSize(QtCore.QSize(0, 44))
        self.frameTitleBar.setMaximumSize(QtCore.QSize(16777215, 44))
        self.frameTitleBar.setSizeIncrement(QtCore.QSize(0, 0))
        self.frameTitleBar.setStyleSheet("QFrame {\n"
                                         "    background-color : #121212;\n"
                                         "\n"
                                         "}")
        self.frameTitleBar.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frameTitleBar.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frameTitleBar.setObjectName("frameTitleBar")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frameTitleBar)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.labelTitleBar = QtWidgets.QLabel(parent=self.frameTitleBar)
        self.labelTitleBar.setStyleSheet("QLabel {\n"
                                         "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                         "    color : #FFFFFF;\n"
                                         "    border-radius : 0px;\n"
                                         "    text-align : left;\n"
                                         "    padding-left: 5px;\n"
                                         "}\n"
                                         "\n"
                                         "QLabel::hover {\n"
                                         "    color : #4F6FA0;\n"
                                         "}\n"
                                         "")
        self.labelTitleBar.setText("")
        self.labelTitleBar.setObjectName("labelTitleBar")
        self.gridLayout_3.addWidget(self.labelTitleBar, 0, 0, 1, 1)
        self.frameTitleBarActions = QtWidgets.QFrame(parent=self.frameTitleBar)
        self.frameTitleBarActions.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel)
        self.frameTitleBarActions.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised)
        self.frameTitleBarActions.setObjectName("frameTitleBarActions")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frameTitleBarActions)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pushButtonCloseWindow = QtWidgets.QPushButton(
            parent=self.frameTitleBarActions)
        self.pushButtonCloseWindow.setMinimumSize(QtCore.QSize(42, 42))
        self.pushButtonCloseWindow.setMaximumSize(QtCore.QSize(42, 42))
        self.pushButtonCloseWindow.setStyleSheet("QPushButton {\n"
                                                 "    background-color : #121212;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:hover {\n"
                                                 "    background-color : #A93226;\n"
                                                 "}")
        self.pushButtonCloseWindow.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-x.png"),
                       QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonCloseWindow.setIcon(icon)
        self.pushButtonCloseWindow.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonCloseWindow.setObjectName("pushButtonCloseWindow")
        self.gridLayout_4.addWidget(self.pushButtonCloseWindow, 0, 2, 1, 1)
        self.pushButtonMinimizeWindow = QtWidgets.QPushButton(
            parent=self.frameTitleBarActions)
        self.pushButtonMinimizeWindow.setMinimumSize(QtCore.QSize(42, 42))
        self.pushButtonMinimizeWindow.setMaximumSize(QtCore.QSize(42, 42))
        self.pushButtonMinimizeWindow.setStyleSheet("QPushButton {\n"
                                                    "    background-color : #121212;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QPushButton:hover {\n"
                                                    "    background-color : #555555;\n"
                                                    "}")
        self.pushButtonMinimizeWindow.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-window-minimize.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonMinimizeWindow.setIcon(icon1)
        self.pushButtonMinimizeWindow.setIconSize(QtCore.QSize(42, 42))
        self.pushButtonMinimizeWindow.setObjectName("pushButtonMinimizeWindow")
        self.gridLayout_4.addWidget(self.pushButtonMinimizeWindow, 0, 0, 1, 1)
        self.pushButtonRestoreWindow = QtWidgets.QPushButton(
            parent=self.frameTitleBarActions)
        self.pushButtonRestoreWindow.setMinimumSize(QtCore.QSize(42, 42))
        self.pushButtonRestoreWindow.setMaximumSize(QtCore.QSize(42, 42))
        self.pushButtonRestoreWindow.setStyleSheet("QPushButton {\n"
                                                   "    background-color : #121212;\n"
                                                   "}\n"
                                                   "\n"
                                                   "QPushButton:hover {\n"
                                                   "    background-color : #555555;\n"
                                                   "}")
        self.pushButtonRestoreWindow.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-window-maximize.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonRestoreWindow.setIcon(icon2)
        self.pushButtonRestoreWindow.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonRestoreWindow.setObjectName("pushButtonRestoreWindow")
        self.gridLayout_4.addWidget(self.pushButtonRestoreWindow, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.frameTitleBarActions, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frameTitleBar, 0, 0, 1, 1)
        self.frameContainer = QtWidgets.QFrame(parent=self.centralwidget)
        self.frameContainer.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameContainer.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameContainer.setLineWidth(0)
        self.frameContainer.setObjectName("frameContainer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frameContainer)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(
            parent=self.frameContainer)
        self.stackedWidget.setLineWidth(0)
        self.stackedWidget.setObjectName("stackedWidget")
        self.homeWidget = QtWidgets.QWidget()
        self.homeWidget.setObjectName("homeWidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.homeWidget)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.frameHomeContainer = QtWidgets.QFrame(parent=self.homeWidget)
        self.frameHomeContainer.setStyleSheet("QFrame {\n"
                                              "    background-color : #121212;\n"
                                              "}")
        self.frameHomeContainer.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameHomeContainer.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameHomeContainer.setLineWidth(0)
        self.frameHomeContainer.setObjectName("frameHomeContainer")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.frameHomeContainer)
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_17.setSpacing(0)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.labelHomeImage = QtWidgets.QLabel(parent=self.frameHomeContainer)
        self.labelHomeImage.setText("")
        self.labelHomeImage.setPixmap(QtGui.QPixmap(
            "app/resources/img/modules/api.png"))
        self.labelHomeImage.setScaledContents(False)
        self.labelHomeImage.setObjectName("labelHomeImage")
        self.gridLayout_17.addWidget(self.labelHomeImage, 2, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_17.addItem(spacerItem1, 2, 0, 1, 1)
        self.labelHomeTitle = QtWidgets.QLabel(parent=self.frameHomeContainer)
        self.labelHomeTitle.setMinimumSize(QtCore.QSize(0, 44))
        self.labelHomeTitle.setMaximumSize(QtCore.QSize(16777215, 44))
        self.labelHomeTitle.setStyleSheet("QLabel{\n"
                                          "    background-color: #222222;\n"
                                          "    font : 22 17pt \"Microsoft JhengHei UI\" ;\n"
                                          "    color : #FFFFFF;\n"
                                          "    border-radius : 0px;\n"
                                          "    text-align : left;\n"
                                          "    padding: 10px;\n"
                                          "}\n"
                                          "")
        self.labelHomeTitle.setObjectName("labelHomeTitle")
        self.gridLayout_17.addWidget(self.labelHomeTitle, 0, 0, 1, 3)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_17.addItem(spacerItem2, 2, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_17.addItem(spacerItem3, 3, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_17.addItem(spacerItem4, 1, 0, 1, 3)
        self.gridLayout_6.addWidget(self.frameHomeContainer, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.homeWidget)
        self.APIWidget = QtWidgets.QWidget()
        self.APIWidget.setObjectName("APIWidget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.APIWidget)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.frameAPIContainer = QtWidgets.QFrame(parent=self.APIWidget)
        self.frameAPIContainer.setStyleSheet("QFrame {\n"
                                             "    background-color : #121212;\n"
                                             "}")
        self.frameAPIContainer.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameAPIContainer.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameAPIContainer.setLineWidth(0)
        self.frameAPIContainer.setObjectName("frameAPIContainer")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.frameAPIContainer)
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.frameAPIContent = QtWidgets.QFrame(parent=self.frameAPIContainer)
        self.frameAPIContent.setStyleSheet("")
        self.frameAPIContent.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameAPIContent.setLineWidth(0)
        self.frameAPIContent.setObjectName("frameAPIContent")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.frameAPIContent)
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.labelApiTitle = QtWidgets.QLabel(parent=self.frameAPIContent)
        self.labelApiTitle.setMinimumSize(QtCore.QSize(0, 44))
        self.labelApiTitle.setMaximumSize(QtCore.QSize(16777215, 44))
        self.labelApiTitle.setSizeIncrement(QtCore.QSize(0, 0))
        self.labelApiTitle.setBaseSize(QtCore.QSize(0, 50))
        self.labelApiTitle.setStyleSheet("QLabel{\n"
                                         "    background-color: #222222;\n"
                                         "    font : 22 17pt \"Microsoft JhengHei UI\" ;\n"
                                         "    color : #FFFFFF;\n"
                                         "    border-radius : 0px;\n"
                                         "    text-align : left;\n"
                                         "    padding: 10px;\n"
                                         "}\n"
                                         "")
        self.labelApiTitle.setLineWidth(0)
        self.labelApiTitle.setObjectName("labelApiTitle")
        self.gridLayout_10.addWidget(self.labelApiTitle, 0, 0, 1, 2)
        self.frameAPIView = QtWidgets.QFrame(parent=self.frameAPIContent)
        self.frameAPIView.setStyleSheet("QFrame{\n"
                                        "    background-color: #121212;\n"
                                        "    border-radius : 0px;\n"
                                        "}\n"
                                        "")
        self.frameAPIView.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameAPIView.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameAPIView.setLineWidth(0)
        self.frameAPIView.setObjectName("frameAPIView")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.frameAPIView)
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_12.setHorizontalSpacing(0)
        self.gridLayout_12.setVerticalSpacing(9)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.frameAPIRequest = QtWidgets.QFrame(parent=self.frameAPIView)
        self.frameAPIRequest.setStyleSheet("")
        self.frameAPIRequest.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameAPIRequest.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameAPIRequest.setLineWidth(0)
        self.frameAPIRequest.setObjectName("frameAPIRequest")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.frameAPIRequest)
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_13.setSpacing(0)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.frameAPIRequestContent = QtWidgets.QFrame(
            parent=self.frameAPIRequest)
        self.frameAPIRequestContent.setStyleSheet("QFrame{\n"
                                                  "    background-color: #121212;\n"
                                                  "    border-radius : 0px;\n"
                                                  "}\n"
                                                  "")
        self.frameAPIRequestContent.setFrameShape(
            QtWidgets.QFrame.Shape.NoFrame)
        self.frameAPIRequestContent.setFrameShadow(
            QtWidgets.QFrame.Shadow.Plain)
        self.frameAPIRequestContent.setLineWidth(0)
        self.frameAPIRequestContent.setObjectName("frameAPIRequestContent")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.frameAPIRequestContent)
        self.gridLayout_16.setContentsMargins(-1, -1, 9, 9)
        self.gridLayout_16.setSpacing(9)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.pushButtonOpenEditor = QtWidgets.QPushButton(
            parent=self.frameAPIRequestContent)
        self.pushButtonOpenEditor.setMinimumSize(QtCore.QSize(300, 40))
        self.pushButtonOpenEditor.setMaximumSize(QtCore.QSize(500, 16777215))
        self.pushButtonOpenEditor.setStyleSheet("QPushButton{\n"
                                                "    background-color : #5F3E77;\n"
                                                "    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
                                                "    color : #FFFFFF;\n"
                                                "\n"
                                                "    border : 2px;\n"
                                                "    border-radius : 20px;\n"
                                                "\n"
                                                "    text-align : left;\n"
                                                "    padding: 10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "\n"
                                                "    background-color: #61364F;\n"
                                                "    color : #FFFFFF;\n"
                                                "}\n"
                                                "")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-pencil.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonOpenEditor.setIcon(icon3)
        self.pushButtonOpenEditor.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonOpenEditor.setObjectName("pushButtonOpenEditor")
        self.gridLayout_16.addWidget(self.pushButtonOpenEditor, 4, 0, 1, 1)
        self.pushButtonSaveRequestedData = QtWidgets.QPushButton(
            parent=self.frameAPIRequestContent)
        self.pushButtonSaveRequestedData.setMinimumSize(QtCore.QSize(300, 40))
        self.pushButtonSaveRequestedData.setMaximumSize(
            QtCore.QSize(500, 16777215))
        self.pushButtonSaveRequestedData.setStyleSheet("QPushButton{\n"
                                                       "    background-color: #3949AB;\n"
                                                       "\n"
                                                       "    border-radius : 20px;\n"
                                                       "\n"
                                                       "    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
                                                       "    color : #FFFFFF;\n"
                                                       "\n"
                                                       "    border : 2px;\n"
                                                       "\n"
                                                       "    text-align : left;\n"
                                                       "    padding: 10px;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QPushButton:hover{\n"
                                                       "    background-color: #303F9F;\n"
                                                       "    color: #FFFFFF;\n"
                                                       "\n"
                                                       "}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-save.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonSaveRequestedData.setIcon(icon4)
        self.pushButtonSaveRequestedData.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonSaveRequestedData.setObjectName(
            "pushButtonSaveRequestedData")
        self.gridLayout_16.addWidget(
            self.pushButtonSaveRequestedData, 5, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_16.addItem(spacerItem5, 2, 0, 1, 3)
        self.treeViewRequestData = QtWidgets.QTreeView(
            parent=self.frameAPIRequestContent)
        self.treeViewRequestData.setStyleSheet("QTreeView {\n"
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
        self.treeViewRequestData.setObjectName("treeViewRequestData")
        self.gridLayout_16.addWidget(self.treeViewRequestData, 11, 0, 1, 3)
        self.pushButtonRequestData = QtWidgets.QPushButton(
            parent=self.frameAPIRequestContent)
        self.pushButtonRequestData.setMinimumSize(QtCore.QSize(300, 40))
        self.pushButtonRequestData.setMaximumSize(QtCore.QSize(500, 16777215))
        self.pushButtonRequestData.setStyleSheet("QPushButton{\n"
                                                 "    background-color : #5F3E77;\n"
                                                 "    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
                                                 "    color : #FFFFFF;\n"
                                                 "\n"
                                                 "    border : 2px;\n"
                                                 "    border-radius : 20px;\n"
                                                 "\n"
                                                 "    text-align : left;\n"
                                                 "    padding: 10px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QPushButton:hover{\n"
                                                 "\n"
                                                 "    background-color: #61364F;\n"
                                                 "    color : #FFFFFF;\n"
                                                 "}\n"
                                                 "")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-view-column.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonRequestData.setIcon(icon5)
        self.pushButtonRequestData.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonRequestData.setObjectName("pushButtonRequestData")
        self.gridLayout_16.addWidget(self.pushButtonRequestData, 3, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_16.addItem(spacerItem6, 6, 0, 1, 3)
        self.gridLayout_13.addWidget(self.frameAPIRequestContent, 4, 0, 1, 2)
        self.gridLayout_12.addWidget(self.frameAPIRequest, 0, 0, 1, 1)
        self.gridLayout_10.addWidget(self.frameAPIView, 2, 0, 1, 2)
        self.frameDataSearcher = QtWidgets.QFrame(parent=self.frameAPIContent)
        self.frameDataSearcher.setMinimumSize(QtCore.QSize(50, 80))
        self.frameDataSearcher.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frameDataSearcher.setStyleSheet("QFrame {\n"
                                             "    background-color : #121212;\n"
                                             "}")
        self.frameDataSearcher.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameDataSearcher.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameDataSearcher.setLineWidth(0)
        self.frameDataSearcher.setObjectName("frameDataSearcher")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.frameDataSearcher)
        self.gridLayout_11.setContentsMargins(0, 0, 9, 9)
        self.gridLayout_11.setSpacing(9)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.pushButtonSearch = QtWidgets.QPushButton(
            parent=self.frameDataSearcher)
        self.pushButtonSearch.setMinimumSize(QtCore.QSize(170, 30))
        self.pushButtonSearch.setMaximumSize(QtCore.QSize(70, 30))
        self.pushButtonSearch.setStyleSheet("QPushButton{\n"
                                            "    background-color: #D37242;\n"
                                            "\n"
                                            "    border-top-left-radius: 14px;\n"
                                            "    border-bottom-left-radius: 14px;\n"
                                            "    border-top-right-radius: 14px;\n"
                                            "    border-bottom-right-radius: 14px;\n"
                                            "\n"
                                            "    font : 75 10pt \"Microsoft JhengHei UI\" bold;\n"
                                            "    color: #FFFFFF;\n"
                                            "    padding : 10px;\n"
                                            "\n"
                                            "    text-align : left;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "    background-color: #BB673D;\n"
                                            "    border-top-left-radius: 14px;    \n"
                                            "    border-bottom-left-radius: 14px;\n"
                                            "    border-top-right-radius: 14px;\n"
                                            "    border-bottom-right-radius: 14px;\n"
                                            "\n"
                                            "    font : 75 10pt \"Microsoft JhengHei UI\" bold;\n"
                                            "    color: #FFFFFF;\n"
                                            "    text-align : left;\n"
                                            "\n"
                                            "}")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-arrow-circle-right.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonSearch.setIcon(icon6)
        self.pushButtonSearch.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonSearch.setObjectName("pushButtonSearch")
        self.gridLayout_11.addWidget(self.pushButtonSearch, 1, 2, 1, 1)
        self.lineEditSearcher = QtWidgets.QLineEdit(
            parent=self.frameDataSearcher)
        self.lineEditSearcher.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEditSearcher.setMaximumSize(QtCore.QSize(16777215, 16777214))
        self.lineEditSearcher.setStyleSheet("QLineEdit {\n"
                                            "    font: 25 12pt \"Microsoft YaHei UI\";\n"
                                            "    background-color : #222222;\n"
                                            "    color : #FFFFFF;\n"
                                            "    border : 2px;\n"
                                            "    border-radius : 15px;\n"
                                            "}\n"
                                            "\n"
                                            "QLineEdit::hover{\n"
                                            "    background-color: #121212;\n"
                                            "    border : 1px solid #5F3E77;\n"
                                            "}")
        self.lineEditSearcher.setObjectName("lineEditSearcher")
        self.gridLayout_11.addWidget(self.lineEditSearcher, 1, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_11.addItem(spacerItem7, 1, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_11.addItem(spacerItem8, 2, 1, 1, 2)
        spacerItem9 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_11.addItem(spacerItem9, 0, 1, 1, 2)
        self.gridLayout_10.addWidget(self.frameDataSearcher, 1, 0, 1, 2)
        self.gridLayout_15.addWidget(self.frameAPIContent, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.frameAPIContainer, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.APIWidget)
        self.settingsWidget = QtWidgets.QWidget()
        self.settingsWidget.setObjectName("settingsWidget")
        self.gridLayout_19 = QtWidgets.QGridLayout(self.settingsWidget)
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_19.setSpacing(0)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.frameSettingsContainer = QtWidgets.QFrame(
            parent=self.settingsWidget)
        self.frameSettingsContainer.setStyleSheet("QFrame {\n"
                                                  "    background-color : #121212;\n"
                                                  "}")
        self.frameSettingsContainer.setFrameShape(
            QtWidgets.QFrame.Shape.NoFrame)
        self.frameSettingsContainer.setFrameShadow(
            QtWidgets.QFrame.Shadow.Plain)
        self.frameSettingsContainer.setLineWidth(0)
        self.frameSettingsContainer.setObjectName("frameSettingsContainer")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.frameSettingsContainer)
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_20.setSpacing(0)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.frameSettingsContent = QtWidgets.QFrame(
            parent=self.frameSettingsContainer)
        self.frameSettingsContent.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameSettingsContent.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameSettingsContent.setLineWidth(0)
        self.frameSettingsContent.setObjectName("frameSettingsContent")
        self.gridLayout_23 = QtWidgets.QGridLayout(self.frameSettingsContent)
        self.gridLayout_23.setObjectName("gridLayout_23")
        spacerItem10 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_23.addItem(spacerItem10, 4, 0, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_23.addItem(spacerItem11, 1, 0, 1, 1)
        self.groupBoxMode = QtWidgets.QGroupBox(
            parent=self.frameSettingsContent)
        self.groupBoxMode.setStyleSheet("QGroupBox {\n"
                                        "\n"
                                        "    font: 76 13pt \"Microsoft JhengHei UI\";\n"
                                        "    font-weight: bold;\n"
                                        "    color: #D37242;\n"
                                        "    \n"
                                        "    border : 1px solid #5F3E77;\n"
                                        "}\n"
                                        "\n"
                                        "")
        self.groupBoxMode.setTitle("")
        self.groupBoxMode.setFlat(True)
        self.groupBoxMode.setObjectName("groupBoxMode")
        self.gridLayout_22 = QtWidgets.QGridLayout(self.groupBoxMode)
        self.gridLayout_22.setObjectName("gridLayout_22")
        spacerItem12 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_22.addItem(spacerItem12, 1, 0, 1, 1)
        self.radioButtonLightMode = QtWidgets.QRadioButton(
            parent=self.groupBoxMode)
        self.radioButtonLightMode.setStyleSheet("QRadioButton {\n"
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
        self.radioButtonLightMode.setObjectName("radioButtonLightMode")
        self.gridLayout_22.addWidget(self.radioButtonLightMode, 4, 0, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_22.addItem(spacerItem13, 5, 0, 1, 1)
        self.labeTitleMode = QtWidgets.QLabel(parent=self.groupBoxMode)
        self.labeTitleMode.setStyleSheet("QLabel {\n"
                                         "    font: 25 14pt \"Microsoft YaHei UI Light\";\n"
                                         "    color : #4F6FA0;\n"
                                         "}")
        self.labeTitleMode.setObjectName("labeTitleMode")
        self.gridLayout_22.addWidget(self.labeTitleMode, 0, 0, 1, 1)
        self.radioButtonDarkMode = QtWidgets.QRadioButton(
            parent=self.groupBoxMode)
        self.radioButtonDarkMode.setStyleSheet("QRadioButton {\n"
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
        self.radioButtonDarkMode.setChecked(True)
        self.radioButtonDarkMode.setObjectName("radioButtonDarkMode")
        self.gridLayout_22.addWidget(self.radioButtonDarkMode, 2, 0, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_22.addItem(spacerItem14, 3, 0, 1, 1)
        self.gridLayout_23.addWidget(self.groupBoxMode, 2, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(parent=self.frameSettingsContent)
        self.groupBox.setStyleSheet("QGroupBox {\n"
                                    "\n"
                                    "    font: 76 13pt \"Microsoft JhengHei UI\";\n"
                                    "    font-weight: bold;\n"
                                    "    color: #D37242;\n"
                                    "    \n"
                                    "    border : 1px solid #5F3E77;\n"
                                    "}\n"
                                    "\n"
                                    "")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_24 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.listViewLog = QtWidgets.QListView(parent=self.groupBox)
        self.listViewLog.setStyleSheet("QListView {\n"
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
        self.listViewLog.setObjectName("listViewLog")
        self.gridLayout_24.addWidget(self.listViewLog, 2, 0, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_24.addItem(spacerItem15, 1, 0, 1, 1)
        self.labelTitleLog = QtWidgets.QLabel(parent=self.groupBox)
        self.labelTitleLog.setStyleSheet("QLabel {\n"
                                         "    font: 25 14pt \"Microsoft YaHei UI Light\";\n"
                                         "    color : #4F6FA0;\n"
                                         "}")
        self.labelTitleLog.setObjectName("labelTitleLog")
        self.gridLayout_24.addWidget(self.labelTitleLog, 0, 0, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_24.addItem(spacerItem16, 3, 0, 1, 1)
        self.gridLayout_23.addWidget(self.groupBox, 3, 0, 1, 1)
        self.gridLayout_20.addWidget(self.frameSettingsContent, 1, 0, 1, 1)
        self.labelSettingsTitle = QtWidgets.QLabel(
            parent=self.frameSettingsContainer)
        self.labelSettingsTitle.setMinimumSize(QtCore.QSize(0, 44))
        self.labelSettingsTitle.setMaximumSize(QtCore.QSize(16777215, 44))
        self.labelSettingsTitle.setStyleSheet("QLabel{\n"
                                              "    background-color: #222222;\n"
                                              "    font : 22 17pt \"Microsoft JhengHei UI\" ;\n"
                                              "    color : #FFFFFF;\n"
                                              "    border-radius : 0px;\n"
                                              "    text-align : left;\n"
                                              "    padding: 10px;\n"
                                              "}\n"
                                              "")
        self.labelSettingsTitle.setObjectName("labelSettingsTitle")
        self.gridLayout_20.addWidget(self.labelSettingsTitle, 0, 0, 1, 1)
        self.gridLayout_19.addWidget(self.frameSettingsContainer, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.settingsWidget)
        self.workspaceWidget = QtWidgets.QWidget()
        self.workspaceWidget.setObjectName("workspaceWidget")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.workspaceWidget)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.frameWorkspaceContainer = QtWidgets.QFrame(
            parent=self.workspaceWidget)
        self.frameWorkspaceContainer.setStyleSheet("QFrame{\n"
                                                   "    background-color: #121212;\n"
                                                   "    border-radius : 0px;\n"
                                                   "}\n"
                                                   "")
        self.frameWorkspaceContainer.setFrameShape(
            QtWidgets.QFrame.Shape.NoFrame)
        self.frameWorkspaceContainer.setFrameShadow(
            QtWidgets.QFrame.Shadow.Plain)
        self.frameWorkspaceContainer.setLineWidth(0)
        self.frameWorkspaceContainer.setMidLineWidth(0)
        self.frameWorkspaceContainer.setObjectName("frameWorkspaceContainer")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.frameWorkspaceContainer)
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.frameWorkspaceContent = QtWidgets.QFrame(
            parent=self.frameWorkspaceContainer)
        self.frameWorkspaceContent.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel)
        self.frameWorkspaceContent.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised)
        self.frameWorkspaceContent.setObjectName("frameWorkspaceContent")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.frameWorkspaceContent)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.groupBoxWorkspace = QtWidgets.QGroupBox(
            parent=self.frameWorkspaceContent)
        self.groupBoxWorkspace.setStyleSheet("QGroupBox {\n"
                                             "\n"
                                             "    font: 76 13pt \"Microsoft JhengHei UI\";\n"
                                             "    font-weight: bold;\n"
                                             "    color: #D37242;\n"
                                             "    \n"
                                             "    border : 1px solid #5F3E77;\n"
                                             "}\n"
                                             "\n"
                                             "")
        self.groupBoxWorkspace.setTitle("")
        self.groupBoxWorkspace.setObjectName("groupBoxWorkspace")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBoxWorkspace)
        self.gridLayout_14.setObjectName("gridLayout_14")
        spacerItem17 = QtWidgets.QSpacerItem(
            20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_14.addItem(spacerItem17, 10, 1, 1, 1)
        spacerItem18 = QtWidgets.QSpacerItem(
            20, 15, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_14.addItem(spacerItem18, 8, 1, 1, 1)
        self.pushButtonSelectFile = QtWidgets.QPushButton(
            parent=self.groupBoxWorkspace)
        self.pushButtonSelectFile.setMinimumSize(QtCore.QSize(300, 40))
        self.pushButtonSelectFile.setMaximumSize(QtCore.QSize(500, 16777215))
        self.pushButtonSelectFile.setStyleSheet("QPushButton{\n"
                                                "    background-color : #5F3E77;\n"
                                                "    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
                                                "    color : #FFFFFF;\n"
                                                "\n"
                                                "    border : 2px;\n"
                                                "    border-radius : 20px;\n"
                                                "\n"
                                                "    text-align : left;\n"
                                                "    padding: 10px;\n"
                                                "}\n"
                                                "\n"
                                                "QPushButton:hover{\n"
                                                "\n"
                                                "    background-color: #61364F;\n"
                                                "    color : #FFFFFF;\n"
                                                "}\n"
                                                "")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-file.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonSelectFile.setIcon(icon7)
        self.pushButtonSelectFile.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonSelectFile.setFlat(True)
        self.pushButtonSelectFile.setObjectName("pushButtonSelectFile")
        self.gridLayout_14.addWidget(
            self.pushButtonSelectFile, 5, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.pushButtonSelectDirectory = QtWidgets.QPushButton(
            parent=self.groupBoxWorkspace)
        self.pushButtonSelectDirectory.setMinimumSize(QtCore.QSize(300, 40))
        self.pushButtonSelectDirectory.setMaximumSize(
            QtCore.QSize(500, 16777215))
        self.pushButtonSelectDirectory.setStyleSheet("QPushButton{\n"
                                                     "    background-color : #5F3E77;\n"
                                                     "    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
                                                     "    color : #FFFFFF;\n"
                                                     "\n"
                                                     "    border : 2px;\n"
                                                     "    border-radius : 20px;\n"
                                                     "\n"
                                                     "    text-align : left;\n"
                                                     "    padding: 10px;\n"
                                                     "}\n"
                                                     "\n"
                                                     "QPushButton:hover{\n"
                                                     "\n"
                                                     "    background-color: #61364F;\n"
                                                     "    color : #FFFFFF;\n"
                                                     "}\n"
                                                     "")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-folder-open.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonSelectDirectory.setIcon(icon8)
        self.pushButtonSelectDirectory.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonSelectDirectory.setFlat(True)
        self.pushButtonSelectDirectory.setObjectName(
            "pushButtonSelectDirectory")
        self.gridLayout_14.addWidget(
            self.pushButtonSelectDirectory, 7, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.pushButtonConvertJSONToXLSX = QtWidgets.QPushButton(
            parent=self.groupBoxWorkspace)
        self.pushButtonConvertJSONToXLSX.setMinimumSize(QtCore.QSize(300, 40))
        self.pushButtonConvertJSONToXLSX.setMaximumSize(
            QtCore.QSize(500, 16777215))
        self.pushButtonConvertJSONToXLSX.setStyleSheet("QPushButton{\n"
                                                       "    background-color: #3949AB;\n"
                                                       "\n"
                                                       "    border-radius : 20px;\n"
                                                       "\n"
                                                       "    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
                                                       "    color : #FFFFFF;\n"
                                                       "\n"
                                                       "    border : 2px;\n"
                                                       "\n"
                                                       "    text-align : left;\n"
                                                       "    padding: 10px;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QPushButton:hover{\n"
                                                       "    background-color: #303F9F;\n"
                                                       "    color: #FFFFFF;\n"
                                                       "\n"
                                                       "}")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-loop-circular.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonConvertJSONToXLSX.setIcon(icon9)
        self.pushButtonConvertJSONToXLSX.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonConvertJSONToXLSX.setFlat(True)
        self.pushButtonConvertJSONToXLSX.setObjectName(
            "pushButtonConvertJSONToXLSX")
        self.gridLayout_14.addWidget(
            self.pushButtonConvertJSONToXLSX, 11, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.labelSelectedFile = QtWidgets.QLabel(
            parent=self.groupBoxWorkspace)
        self.labelSelectedFile.setStyleSheet("QLabel {\n"
                                             "    font: 25 14pt \"Microsoft YaHei UI Light\";\n"
                                             "    color : #D37242;\n"
                                             "}")
        self.labelSelectedFile.setObjectName("labelSelectedFile")
        self.gridLayout_14.addWidget(self.labelSelectedFile, 1, 1, 1, 1)
        spacerItem19 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_14.addItem(spacerItem19, 4, 1, 1, 1)
        spacerItem20 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_14.addItem(spacerItem20, 0, 1, 1, 1)
        self.lineEditSelectedFile = QtWidgets.QLineEdit(
            parent=self.groupBoxWorkspace)
        self.lineEditSelectedFile.setMinimumSize(QtCore.QSize(500, 30))
        self.lineEditSelectedFile.setMaximumSize(QtCore.QSize(500, 30))
        self.lineEditSelectedFile.setStyleSheet("QLineEdit {\n"
                                                "    font: 25 13pt \"Microsoft YaHei UI\";\n"
                                                "    background-color : #222222;\n"
                                                "    color : #FFFFFF;\n"
                                                "    border : 2px;\n"
                                                "    border-radius : 15px;\n"
                                                "}")
        self.lineEditSelectedFile.setObjectName("lineEditSelectedFile")
        self.gridLayout_14.addWidget(
            self.lineEditSelectedFile, 3, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.pushButtonExecuteSelectedFile = QtWidgets.QPushButton(
            parent=self.groupBoxWorkspace)
        self.pushButtonExecuteSelectedFile.setMinimumSize(
            QtCore.QSize(300, 40))
        self.pushButtonExecuteSelectedFile.setMaximumSize(
            QtCore.QSize(500, 16777215))
        self.pushButtonExecuteSelectedFile.setStyleSheet("QPushButton{\n"
                                                         "    background-color: #3949AB;\n"
                                                         "\n"
                                                         "    border-radius : 20px;\n"
                                                         "\n"
                                                         "    font : 75 13pt \"Microsoft JhengHei UI\" bold;\n"
                                                         "    color : #FFFFFF;\n"
                                                         "\n"
                                                         "    border : 2px;\n"
                                                         "\n"
                                                         "    text-align : left;\n"
                                                         "    padding: 10px;\n"
                                                         "}\n"
                                                         "\n"
                                                         "QPushButton:hover{\n"
                                                         "    background-color: #303F9F;\n"
                                                         "    color: #FFFFFF;\n"
                                                         "\n"
                                                         "}")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-check.png"),
                         QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonExecuteSelectedFile.setIcon(icon10)
        self.pushButtonExecuteSelectedFile.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonExecuteSelectedFile.setFlat(True)
        self.pushButtonExecuteSelectedFile.setObjectName(
            "pushButtonExecuteSelectedFile")
        self.gridLayout_14.addWidget(
            self.pushButtonExecuteSelectedFile, 9, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        spacerItem21 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_14.addItem(spacerItem21, 2, 1, 1, 1)
        spacerItem22 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_14.addItem(spacerItem22, 16, 1, 1, 1)
        spacerItem23 = QtWidgets.QSpacerItem(
            20, 15, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_14.addItem(spacerItem23, 12, 1, 1, 1)
        spacerItem24 = QtWidgets.QSpacerItem(
            20, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout_14.addItem(spacerItem24, 6, 1, 1, 1)
        self.gridLayout_18.addWidget(self.groupBoxWorkspace, 0, 1, 1, 1)
        self.treeViewSystem = QtWidgets.QTreeView(
            parent=self.frameWorkspaceContent)
        self.treeViewSystem.setMinimumSize(QtCore.QSize(300, 0))
        self.treeViewSystem.setStyleSheet("QTreeView {\n"
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
        self.treeViewSystem.setObjectName("treeViewSystem")
        self.gridLayout_18.addWidget(self.treeViewSystem, 0, 0, 1, 1)
        self.listViewFile = QtWidgets.QListView(
            parent=self.frameWorkspaceContent)
        self.listViewFile.setMinimumSize(QtCore.QSize(0, 80))
        self.listViewFile.setMaximumSize(QtCore.QSize(16777215, 200))
        self.listViewFile.setStyleSheet("QListView {\n"
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
        self.listViewFile.setObjectName("listViewFile")
        self.gridLayout_18.addWidget(self.listViewFile, 1, 0, 1, 1)
        self.listViewFileHistory = QtWidgets.QListView(
            parent=self.frameWorkspaceContent)
        self.listViewFileHistory.setMinimumSize(QtCore.QSize(0, 80))
        self.listViewFileHistory.setMaximumSize(QtCore.QSize(16777215, 200))
        self.listViewFileHistory.setStyleSheet("QListView {\n"
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
        self.listViewFileHistory.setObjectName("listViewFileHistory")
        self.gridLayout_18.addWidget(self.listViewFileHistory, 1, 1, 1, 1)
        self.gridLayout_9.addWidget(self.frameWorkspaceContent, 1, 0, 1, 1)
        self.labelWorkspaceTitle = QtWidgets.QLabel(
            parent=self.frameWorkspaceContainer)
        self.labelWorkspaceTitle.setMinimumSize(QtCore.QSize(0, 44))
        self.labelWorkspaceTitle.setMaximumSize(QtCore.QSize(16777215, 44))
        self.labelWorkspaceTitle.setStyleSheet("QLabel{\n"
                                               "    background-color: #222222;\n"
                                               "    font : 22 17pt \"Microsoft JhengHei UI\" ;\n"
                                               "    color : #FFFFFF;\n"
                                               "    border-radius : 0px;\n"
                                               "    text-align : left;\n"
                                               "    padding: 10px;\n"
                                               "}\n"
                                               "")
        self.labelWorkspaceTitle.setObjectName("labelWorkspaceTitle")
        self.gridLayout_9.addWidget(self.labelWorkspaceTitle, 0, 0, 1, 2)
        self.gridLayout_8.addWidget(self.frameWorkspaceContainer, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.workspaceWidget)
        self.gridLayout_2.addWidget(self.stackedWidget, 1, 1, 1, 1)
        self.frameSidebar = QtWidgets.QFrame(parent=self.frameContainer)
        self.frameSidebar.setMinimumSize(QtCore.QSize(44, 0))
        self.frameSidebar.setMaximumSize(QtCore.QSize(0, 16777215))
        self.frameSidebar.setStyleSheet("QFrame {\n"
                                        "    background-color : #46355e;\n"
                                        "    border-radius : 0px;\n"
                                        "    border : 0px;\n"
                                        "}")
        self.frameSidebar.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameSidebar.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameSidebar.setLineWidth(0)
        self.frameSidebar.setObjectName("frameSidebar")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frameSidebar)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        spacerItem25 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_5.addItem(spacerItem25, 6, 0, 1, 1)
        self.pushButtonSwipeSidebar = QtWidgets.QPushButton(
            parent=self.frameSidebar)
        self.pushButtonSwipeSidebar.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButtonSwipeSidebar.setMaximumSize(
            QtCore.QSize(16777215, 16777215))
        self.pushButtonSwipeSidebar.setStyleSheet("\n"
                                                  "QPushButton{\n"
                                                  "    background-color : #D37242;\n"
                                                  "    font : 75 15pt \"Microsoft JhengHei UI\" bold;\n"
                                                  "    color : #FFFFFF;\n"
                                                  "\n"
                                                  "    border : 2px;\n"
                                                  "\n"
                                                  "    text-align : left;\n"
                                                  "    padding: 10px;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton::hover {\n"
                                                  "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                                  "    color : #121212;\n"
                                                  "    background-color : #BB673D;\n"
                                                  "}")
        self.pushButtonSwipeSidebar.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-list.png"),
                         QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonSwipeSidebar.setIcon(icon11)
        self.pushButtonSwipeSidebar.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonSwipeSidebar.setFlat(True)
        self.pushButtonSwipeSidebar.setObjectName("pushButtonSwipeSidebar")
        self.gridLayout_5.addWidget(self.pushButtonSwipeSidebar, 0, 0, 1, 1)
        spacerItem26 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_5.addItem(spacerItem26, 1, 0, 1, 1)
        self.frameSidebarActions = QtWidgets.QFrame(parent=self.frameSidebar)
        self.frameSidebarActions.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameSidebarActions.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameSidebarActions.setLineWidth(0)
        self.frameSidebarActions.setObjectName("frameSidebarActions")
        self.gridLayout_21 = QtWidgets.QGridLayout(self.frameSidebarActions)
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_21.setSpacing(0)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.pushButtonAPI = QtWidgets.QPushButton(
            parent=self.frameSidebarActions)
        self.pushButtonAPI.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButtonAPI.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButtonAPI.setStyleSheet("QPushButton {\n"
                                         "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                         "    color : #FFFFFF;\n"
                                         "    background-color : transparent;\n"
                                         "\n"
                                         "    border : 2px;\n"
                                         "\n"
                                         "    text-align : left;\n"
                                         "    padding: 10px;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton::hover {\n"
                                         "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                         "    color : #121212;\n"
                                         "    background-color : #6b508f;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton::pressed {\n"
                                         "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                         "    color : #121212;\n"
                                         "    background-color : #8468aa;\n"
                                         "}\n"
                                         "")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-browser.png"),
                         QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonAPI.setIcon(icon12)
        self.pushButtonAPI.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonAPI.setFlat(True)
        self.pushButtonAPI.setObjectName("pushButtonAPI")
        self.gridLayout_21.addWidget(self.pushButtonAPI, 1, 0, 1, 1)
        self.pushButtonHome = QtWidgets.QPushButton(
            parent=self.frameSidebarActions)
        self.pushButtonHome.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButtonHome.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButtonHome.setStyleSheet("QPushButton {\n"
                                          "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                          "    color : #FFFFFF;\n"
                                          "    background-color : transparent;\n"
                                          "\n"
                                          "    border : 2px;\n"
                                          "\n"
                                          "    text-align : left;\n"
                                          "    padding: 10px;\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton::hover {\n"
                                          "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                          "    color : #121212;\n"
                                          "    background-color : #6b508f;\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton::pressed {\n"
                                          "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                          "    color : #121212;\n"
                                          "    background-color : #8468aa;\n"
                                          "}\n"
                                          "")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-home.png"),
                         QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonHome.setIcon(icon13)
        self.pushButtonHome.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonHome.setFlat(True)
        self.pushButtonHome.setObjectName("pushButtonHome")
        self.gridLayout_21.addWidget(self.pushButtonHome, 0, 0, 1, 1)
        self.pushButtonWorkspace = QtWidgets.QPushButton(
            parent=self.frameSidebarActions)
        self.pushButtonWorkspace.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButtonWorkspace.setMaximumSize(
            QtCore.QSize(16777215, 16777215))
        self.pushButtonWorkspace.setStyleSheet("QPushButton {\n"
                                               "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                               "    color : #FFFFFF;\n"
                                               "    background-color : transparent;\n"
                                               "\n"
                                               "    border : 2px;\n"
                                               "\n"
                                               "    text-align : left;\n"
                                               "    padding: 10px;\n"
                                               "}\n"
                                               "\n"
                                               "QPushButton::hover {\n"
                                               "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                               "    color : #121212;\n"
                                               "    background-color : #6b508f;\n"
                                               "}\n"
                                               "\n"
                                               "QPushButton::pressed {\n"
                                               "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                               "    color : #121212;\n"
                                               "    background-color : #8468aa;\n"
                                               "}\n"
                                               "")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-mug-tea.png"),
                         QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonWorkspace.setIcon(icon14)
        self.pushButtonWorkspace.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonWorkspace.setFlat(True)
        self.pushButtonWorkspace.setObjectName("pushButtonWorkspace")
        self.gridLayout_21.addWidget(self.pushButtonWorkspace, 2, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frameSidebarActions, 5, 0, 1, 1)
        self.pushButtonSettings = QtWidgets.QPushButton(
            parent=self.frameSidebar)
        self.pushButtonSettings.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButtonSettings.setMaximumSize(
            QtCore.QSize(16777215, 16777215))
        self.pushButtonSettings.setStyleSheet("QPushButton {\n"
                                              "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                              "    color : #FFFFFF;\n"
                                              "    background-color : transparent;\n"
                                              "\n"
                                              "    border : 2px;\n"
                                              "\n"
                                              "    text-align : left;\n"
                                              "    padding: 10px;\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton::hover {\n"
                                              "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                              "    color : #121212;\n"
                                              "    background-color : #6b508f;\n"
                                              "}\n"
                                              "\n"
                                              "QPushButton::pressed {\n"
                                              "    font : 77 15pt \"Microsoft JhengHei UI\";\n"
                                              "    color : #121212;\n"
                                              "    background-color : #8468aa;\n"
                                              "}\n"
                                              "")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-settings.png"),
                         QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonSettings.setIcon(icon15)
        self.pushButtonSettings.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonSettings.setFlat(True)
        self.pushButtonSettings.setObjectName("pushButtonSettings")
        self.gridLayout_5.addWidget(self.pushButtonSettings, 7, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frameSidebar, 0, 0, 2, 1)
        self.gridLayout.addWidget(self.frameContainer, 1, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.labelHomeTitle.setText(_translate("MainWindow", "Inicio"))
        self.labelApiTitle.setText(_translate("MainWindow", "API"))
        self.labelWorkspaceTitle.setText(
            _translate("MainWindow", "Espacio de trabajo"))
        self.labelSettingsTitle.setText(_translate("MainWindow", "Ajustes"))

        self.pushButtonHome.setText(_translate("MainWindow", "\t\t\tInicio"))
        self.pushButtonAPI.setText(_translate("MainWindow", "\t\t\tAPI"))
        self.pushButtonWorkspace.setText(_translate(
            "MainWindow", "\t\t\tEspacio de Trabajo"))
        self.pushButtonSettings.setText(
            _translate("MainWindow", "\t\t\tAjustes"))

        self.pushButtonSearch.setText(_translate("MainWindow", "\t\t\tBuscar"))

        self.pushButtonRequestData.setText(
            _translate("MainWindow", "\t\t\tSolicitar API"))
        self.pushButtonOpenEditor.setText(
            _translate("MainWindow", "\t\t\tAbrir editor"))
        self.pushButtonSaveRequestedData.setText(_translate(
            "MainWindow", "\t\t\tGuardar archivo extraido"))

        self.pushButtonExecuteSelectedFile.setText(
            _translate("MainWindow", "\t\t\tEjecutar archivo"))
        self.pushButtonSelectFile.setText(_translate(
            "MainWindow", "\t\t\tSeleccionar archivo"))
        self.pushButtonSelectDirectory.setText(_translate(
            "MainWindow", "\t\t\tSeleccionar directorio"))

        self.pushButtonConvertJSONToXLSX.setText(
            _translate("MainWindow", "\t\t\tConvertir JSON a XLSX"))

        self.labelSelectedFile.setText(
            _translate("MainWindow", "Seleccionado"))

        self.labeTitleMode.setText(_translate("MainWindow", "Modo"))
        self.radioButtonLightMode.setText(
            _translate("MainWindow", "Modo Claro"))
        self.radioButtonDarkMode.setText(
            _translate("MainWindow", "Modo Oscuro"))


        self.labelTitleLog.setText(
            _translate("MainWindow", "Log"))