from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import common
import messages_pb2
import context_pb2
import request_pb2

import google.protobuf.message as proto

class Scanner:
    def __init__(self, parentWindow):
        self.widget = parentWindow.findChild(QWidget, 'scannerPage')
        self.contextStack = parentWindow.findChild(QStackedWidget, 'scanContextStack')
        self.entryTagLabel = parentWindow.findChild(QLabel, 'scanner_entryTagLabel')
        self.frequencyLabel = parentWindow.findChild(QLabel, 'scanner_frequencyLabel')
        self.modulationLabel = parentWindow.findChild(QLabel, 'scanner_modulationLabel')
        self.systemTagLabel = parentWindow.findChild(QLabel, 'scanner_systemTagLabel')
        self.entryNumLabel = parentWindow.findChild(QLabel, 'scanner_entryNumLabel')
        self.lockoutCheckbox = parentWindow.findChild(QCheckBox, 'scanner_lockoutCheckbox')
        self.scanIndicator = parentWindow.findChild(QLabel, 'scanner_scanIndicator')
        self.gainDial = parentWindow.findChild(QDial, 'scanner_gainDial')
        ##self.gainLabel = parentWindow.findChild(QLabel, 'scanner_gainLabel')
        self.sigStrengthBar = parentWindow.findChild(QProgressBar, 'scanner_sigStrengthBar')
        self.squelchDial = parentWindow.findChild(QDial, 'scanner_squelchDial')
        ##self.squelchLabel = parentWindow.findChild(QLabel, 'scanner_squelchLabel')
        self.fnButtonsWidget = parentWindow.findChild(QWidget, 'scanner_fnButtonsWidget')
        self.fnButton1 = parentWindow.findChild(QPushButton, 'scanner_fnButton1')
        self.fnButton2 = parentWindow.findChild(QPushButton, 'scanner_fnButton2')
        self.fnButton3 = parentWindow.findChild(QPushButton, 'scanner_fnButton3')
        self.fnButton4 = parentWindow.findChild(QPushButton, 'scanner_fnButton4')

        movie = QMovie("resources/bar-scan.gif")
        movie.start()
        self.scanIndicator.setMovie(movie)

        labelPalette = QPalette()
        labelPalette.setColor(QPalette.WindowText, Qt.black)
        labelFont = QFont()
        labelFont.setPointSize(12)
        squelchLayout = QHBoxLayout(self.squelchDial)
        squelchLayout.setContentsMargins(0, 0, 0, 0)
        self.squelchLabel = QLabel()
        self.squelchLabel.setAlignment(Qt.AlignCenter)
        self.squelchLabel.setPalette(labelPalette)
        self.squelchLabel.setFont(labelFont)
        self.squelchLabel.setText(str(0))
        squelchLayout.addWidget(self.squelchLabel)

        gainLayout = QHBoxLayout(self.gainDial)
        gainLayout.setContentsMargins(0, 0, 0, 0)
        self.gainLabel = QLabel()
        self.gainLabel.setAlignment(Qt.AlignCenter)
        self.gainLabel.setPalette(labelPalette)
        self.gainLabel.setFont(labelFont)
        self.gainLabel.setText(str(0))
        gainLayout.addWidget(self.gainLabel)

        self.setMode(common.ScannerMode.SCANNING)

    def setMode(self, mode):
        self.contextStack.setCurrentIndex(mode.value)

    def updateScanContext(self, context):
        if context.state == context_pb2.ScannerContext.State.SCAN:
            self.setMode(common.ScannerMode.SCANNING)
        else:
            if context.state == context_pb2.ScannerContext.State.HOLD:
                self.sigStrengthBar.setValue(0)
            elif context.state == context_pb2.ScannerContext.State.RECEIVE:
                self.sigStrengthBar.setValue(100)

            try:
                #entrynum.configure(text=context.entryIndex)
                self.entryNumLabel.setText(context.entryIndex)
                #systag.configure(text=context.systemTag)
                self.systemTagLabel.setText(context.systemTag)
                #entrytag.configure(text=context.entryTag)
                self.entryTagLabel.setText(context.entryTag)
                freq_formatted = str(float(context.freq) / 1000000)
                #freq.configure(text=(freq_formatted + "MHz"))
                self.frequencyLabel.setText((freq_formatted + " MHz"))
                #modulation.configure(text=context.modulation)
                self.modulationLabel.setText(context.modulation)
            except:
                print('problem setting values')

            
            if context.state == context_pb2.ScannerContext.State.HOLD:
                self.setMode(common.ScannerMode.HOLD)
            elif context.state == context_pb2.ScannerContext.State.RECEIVE:
                self.setMode(common.ScannerMode.RECEIVE)

    def updateDemodContext(self, context):
        #SquelchScale.configure(value=context.squelch)
        self.squelchDial.setValue(context.squelch)
        self.squelchLabel.setText(str(context.squelch))
        #GainScale.configure(value=context.gain)
        self.gainDial.setValue(context.gain)
        #self.gainLabel.setText(context.gain)

        if context.gain < 0:
            #GainLabel.configure(text='Auto')
            self.gainLabel.setText('Auto')
        else:
            #GainLabel.configure(text=context.gain)
            self.gainLabel.setText(str(context.gain))
