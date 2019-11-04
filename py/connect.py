import sys

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit
from PySide2.QtCore import QObject
from PySide2.QtGui import QMovie, QPixmap

from socket import *

import common

class ConnectDialog:
    def __init__(self, parentWindow):
        self.widget = parentWindow.findChild(QWidget, 'connectPage')
        self.errorLabel = parentWindow.findChild(QLabel, 'connect_errorLabel')
        self.confirmButton = parentWindow.findChild(QPushButton, 'connect_confirmButton')
        self.connectIndicator = parentWindow.findChild(QLabel, 'connect_indicator')
        self.hostLineEdit = parentWindow.findChild(QLineEdit, 'connect_hostnameLineEdit')
        self.portLineEdit = parentWindow.findChild(QLineEdit, 'connect_portLineEdit')
        self.logo = parentWindow.findChild(QLabel, 'connect_logoImage')

        self.logo.setPixmap(QPixmap("resources/icon-256.png"))
        self.logo.setVisible(False)

        movie = QMovie("resources/loader-small.gif")
        movie.start()
        self.connectIndicator.setMovie(movie)
        self.connectIndicator.setVisible(False)

        self.errorLabel.setVisible(False)

        self.confirmButton.clicked.connect(self.onConfirm)
        self.hostLineEdit.returnPressed.connect(self.onConfirm)
        self.portLineEdit.returnPressed.connect(self.onConfirm)

    def onConfirm(self):
        print('connect confirm')
        try:
            self.connectIndicator.setVisible(True)
            self.errorLabel.setVisible(False)
            self.widget.repaint()
            host = self.hostLineEdit.text()
            port = int(self.portLineEdit.text())
            print('Connecting to ', host, ':', port)
            dest = (host, port)

            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect(dest)
            print('Connection success')

            self.connectIndicator.setVisible(False)

            common.getApp().completeConnection(sock)

        except:
            e = sys.exc_info()[0]
            print(e)
            self.connectIndicator.setVisible(False)
            self.errorLabel.setText(str(e))
            self.errorLabel.setVisible(True)





