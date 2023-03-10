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


class EditorView(QtWidgets.QMainWindow):
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

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(450, 600)
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frameContainer = QtWidgets.QFrame(parent=self.centralwidget)
        self.frameContainer.setStyleSheet("QFrame {\n"
                                          "\n"
                                          "    background-color : #121212;\n"
                                          "}")
        self.frameContainer.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameContainer.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameContainer.setLineWidth(9)
        self.frameContainer.setObjectName("frameContainer")
        self.gridLayout = QtWidgets.QGridLayout(self.frameContainer)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.gridLayout.setSpacing(9)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.pushButtonSaveJson = QtWidgets.QPushButton(
            parent=self.frameContainer)
        self.pushButtonSaveJson.setMinimumSize(QtCore.QSize(300, 42))
        self.pushButtonSaveJson.setMaximumSize(QtCore.QSize(500, 16777215))
        self.pushButtonSaveJson.setStyleSheet("QPushButton{\n"
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-save.png"),
                       QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonSaveJson.setIcon(icon)
        self.pushButtonSaveJson.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonSaveJson.setObjectName("pushButtonSaveJson")
        self.gridLayout.addWidget(
            self.pushButtonSaveJson, 3, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        self.textEditJson = QtWidgets.QTextEdit(parent=self.frameContainer)
        self.textEditJson.setStyleSheet("QTextEdit {\n"
                                        "    background-color : #121212;\n"
                                        "\n"
                                        "    font: 25 12pt \"Microsoft YaHei UI Light\";\n"
                                        "    color : #FFFFFF;\n"
                                        "    border : 1px solid #5F3E77;\n"
                                        "}\n"
                                        "\n"
                                        "QTextEdit::hover {\n"
                                        "    background-color : #222222;\n"
                                        "\n"
                                        "    font: 25 12pt \"Microsoft YaHei UI Light\";\n"
                                        "    color : #FFFFFF;\n"
                                        "    border : 1px solid #5F3E77;\n"
                                        "}")
        self.textEditJson.setObjectName("textEditJson")
        self.gridLayout.addWidget(self.textEditJson, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frameContainer, 1, 0, 1, 1)
        self.frameTitleBar = QtWidgets.QFrame(parent=self.centralwidget)
        self.frameTitleBar.setMinimumSize(QtCore.QSize(0, 44))
        self.frameTitleBar.setMaximumSize(QtCore.QSize(16777215, 44))
        self.frameTitleBar.setSizeIncrement(QtCore.QSize(0, 0))
        self.frameTitleBar.setStyleSheet("QFrame {\n"
                                         "    background-color : #121212;\n"
                                         "\n"
                                         "}")
        self.frameTitleBar.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameTitleBar.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameTitleBar.setLineWidth(0)
        self.frameTitleBar.setObjectName("frameTitleBar")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frameTitleBar)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 0, 1, 1, 1)
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-x.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonCloseWindow.setIcon(icon1)
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-window-minimize.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonMinimizeWindow.setIcon(icon2)
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
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-window-maximize.png"),
                        QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonRestoreWindow.setIcon(icon3)
        self.pushButtonRestoreWindow.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonRestoreWindow.setObjectName("pushButtonRestoreWindow")
        self.gridLayout_4.addWidget(self.pushButtonRestoreWindow, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.frameTitleBarActions, 0, 2, 1, 1)
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
        self.gridLayout_2.addWidget(self.frameTitleBar, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        self.pushButtonSaveJson.setText(
            _translate("MainWindow", "Guardar archivo"))
