# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


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


class ReceiverView(QtWidgets.QMainWindow):
    _gripSize = 1

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
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
        if event.buttons() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos()-self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() and Qt.LeftButton:
                self.move(event.globalPos()-self.m_DragPosition)
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        self.m_drag = False

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            qApp.quit()

        elif event.key() == QtCore.Qt.Key_F1:
            pass

        else:
            super().keyPressEvent(event)

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(750, 200)

        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frameContainer = QtWidgets.QFrame(parent=self.centralwidget)
        self.frameContainer.setStyleSheet("QFrame {\n"
                                          "\n"
                                          "    background-color : #5F3E77;\n"
                                          "}")
        self.frameContainer.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frameContainer.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frameContainer.setLineWidth(0)
        self.frameContainer.setObjectName("frameContainer")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frameContainer)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 5)
        self.pushButtonConfirm = QtWidgets.QPushButton(
            parent=self.frameContainer)
        self.pushButtonConfirm.setMinimumSize(QtCore.QSize(170, 36))
        self.pushButtonConfirm.setMaximumSize(QtCore.QSize(170, 36))
        self.pushButtonConfirm.setStyleSheet("QPushButton{\n"
                                             "    background-color: #61364F;\n"
                                             "\n"
                                             "    border-top-left-radius: 14px;\n"
                                             "    border-bottom-left-radius: 14px;\n"
                                             "    border-top-right-radius: 14px;\n"
                                             "    border-bottom-right-radius: 14px;\n"
                                             "    border : 1px solid #D37242;\n"
                                             "\n"
                                             "    font : 75 12pt \"Microsoft JhengHei UI\" bold;\n"
                                             "    color: #FFFFFF;\n"
                                             "    padding : 10px;\n"
                                             "\n"
                                             "    text-align : left;\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:hover{\n"
                                             "    background-color: #121212;\n"
                                             "    border-top-left-radius: 14px;    \n"
                                             "    border-bottom-left-radius: 14px;\n"
                                             "    border-top-right-radius: 14px;\n"
                                             "    border-bottom-right-radius: 14px;\n"
                                             "\n"
                                             "    font : 75 12pt \"Microsoft JhengHei UI\" bold;\n"
                                             "    color: #FFFFFF;\n"
                                             "    text-align : left;\n"
                                             "\n"
                                             "}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("app/resources/img/icons/24x24/cil-arrow-circle-right.png"),
                       QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButtonConfirm.setIcon(icon)
        self.pushButtonConfirm.setIconSize(QtCore.QSize(24, 24))
        self.pushButtonConfirm.setObjectName("pushButtonConfirm")
        self.gridLayout_2.addWidget(
            self.pushButtonConfirm, 2, 3, 1, 1, QtCore.Qt.AlignmentFlag.AlignRight)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.lineEditData = QtWidgets.QLineEdit(parent=self.frameContainer)
        self.lineEditData.setMinimumSize(QtCore.QSize(480, 36))
        self.lineEditData.setMaximumSize(QtCore.QSize(480, 36))
        self.lineEditData.setSizeIncrement(QtCore.QSize(0, 0))
        self.lineEditData.setStyleSheet("QLineEdit {\n"
                                        "    font: 25 18pt \"Microsoft YaHei UI\";\n"
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
        self.lineEditData.setObjectName("lineEditData")
        self.gridLayout_2.addWidget(
            self.lineEditData, 2, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignLeft)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 2, 4, 1, 1)
        self.labelTitle = QtWidgets.QLabel(parent=self.frameContainer)
        self.labelTitle.setStyleSheet("QLabel {\n"
                                      "\n"
                                      "    font : 25 15pt \"Microsoft YaHei UI Light\";\n"
                                      "    color : #FFFFFF;\n"
                                      "    \n"
                                      "    text-align: left;\n"
                                      "\n"
                                      "}")
        self.labelTitle.setText("")
        self.labelTitle.setObjectName("labelTitle")
        self.gridLayout_2.addWidget(self.labelTitle, 0, 1, 2, 4)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.frameContainer, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonConfirm.setText(_translate("MainWindow", "Confirmar"))
