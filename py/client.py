import sys, getopt

from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtCore import *

from socket import *
from threading import Thread

import common
import constants
import connect
import dialogs
import scanner

import messages_pb2
import context_pb2
import request_pb2

import google.protobuf.message as proto

class PiScanClient(QWidget, common.AppInterface):
    dataReceived = Signal(bytes)

    def __init__(self, parent=None, address=None, port=None):
        super(PiScanClient, self).__init__(parent)
        common.setInstance(self)
        ui_file = 'scan_client.ui'
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        #layout = QGridLayout(self)
        #layout.setContentsMargins(0, 0, 0, 0)
        #layout.addWidget(self.window)

        self.dataReceived.connect(self.handleReceived)

        self.connectDialog = connect.ConnectDialog(self.window, address, port)
        self.scanner = scanner.Scanner(self.window)
        self.dialogs = dialogs.Dialogs(self.window)

        self.contextStack = self.window.findChild(QStackedWidget, 'contextStack')
        self.setWindowMode(common.WindowMode.CONNECT)
        #self.setWindowMode(common.WindowMode.SCANNER)

        #self.window.show()

        self.inmsg = messages_pb2.ServerToClient()

    def mainWidget(self):
        return self.window

    def setWindowMode(self, mode):
        self.mode = mode

        self.contextStack.setCurrentIndex(mode.value)

    def showDialog(self, dialog):
        self.dialogs.setDialog(dialog)
        self.setWindowMode(common.WindowMode.DIALOG)

    def receive(self):
        message1 = messages_pb2.ClientToServer()
        message1.type = messages_pb2.ClientToServer.Type.GENERAL_REQUEST
        message1.generalRequest.type = request_pb2.GeneralRequest.RequestType.SCANNER_CONTEXT
        self.sock.send(message1.SerializeToString())
        message2 = messages_pb2.ClientToServer()
        message2.type = messages_pb2.ClientToServer.Type.GENERAL_REQUEST
        message2.generalRequest.type = request_pb2.GeneralRequest.RequestType.DEMOD_CONTEXT
        self.sock.send(message2.SerializeToString())
        
        while True:
            try:
                data = self.sock.recv(2048)
                self.dataReceived.emit(data)
            except OSError as os_error:
                print(os_error)
                break
            except proto.DecodeError as e:
                print("Parse error")
                print(e)

        print("Closing connection")

    def handleReceived(self, data):
        self.inmsg.ParseFromString(data)
        self.decodeMessage(message=self.inmsg)

    def decodeMessage(self, message):
        print(message)
        if message.type == messages_pb2.ServerToClient.Type.SCANNER_CONTEXT:
            self.scanner.updateScanContext(message.scannerContext)
        elif message.type == messages_pb2.ServerToClient.Type.DEMOD_CONTEXT:
            self.scanner.updateDemodContext(message.demodContext)

    def closeEvent(self, event):
        print('Exiting...')
        try:
            if self.sock:
                self.sock.close()
                self.rcv_thread.join()
        except:
            pass

    ## AppInterface methods

    def completeConnection(self, sock):
        self.sock = sock
        self.rcv_thread = Thread(target=self.receive)
        self.rcv_thread.start()
        self.setWindowMode(common.WindowMode.SCANNER)

    def scan(self):
        message = messages_pb2.ClientToServer()
        message.type = messages_pb2.ClientToServer.Type.SCANNER_STATE_REQUEST
        message.scanStateRequest.state = request_pb2.ScannerStateRequest.NewState.SCAN
        self.sock.send(message.SerializeToString())

    def hold(self):
        message = messages_pb2.ClientToServer()
        message.type = messages_pb2.ClientToServer.Type.SCANNER_STATE_REQUEST
        message.scanStateRequest.state = request_pb2.ScannerStateRequest.NewState.HOLD
        self.sock.send(message.SerializeToString())

    def manualEntry(self, frequency, modulation):
        message = messages_pb2.ClientToServer()
        message.type = messages_pb2.ClientToServer.Type.SCANNER_STATE_REQUEST
        message.scanStateRequest.state = request_pb2.ScannerStateRequest.NewState.MANUAL
        message.scanStateRequest.manFreq = frequency
        self.sock.send(message.SerializeToString())

    def showManualEntryDialog(self):
        self.lastMode = self.mode
        self.showDialog(common.DialogMode.MANUAL_ENTRY)

    def showEditEntryDialog(self):
        self.lastMode = self.mode
        self.showDialog(common.DialogMode.EDIT_ENTRY)

    def showEntryBrowser(self):
        self.lastMode = self.mode
        self.showDialog(common.DialogMode.SYSTEM_BROWSER)

    def showSettingsDialog(self):
        self.lastMode = self.mode
        self.showDialog(common.DialogMode.SYSTEM_SETTINGS)

    def setGain(self, value):
        message = messages_pb2.ClientToServer()
        message.type = messages_pb2.ClientToServer.Type.DEMOD_REQUEST
        message.demodRequest.type = request_pb2.DemodRequest.DemodFunc.SET_GAIN
        message.demodRequest.level = value
        self.sock.send(message.SerializeToString())

    def setSquelch(self, value):
        message = messages_pb2.ClientToServer()
        message.type = messages_pb2.ClientToServer.Type.DEMOD_REQUEST
        message.demodRequest.type = request_pb2.DemodRequest.DemodFunc.SET_SQUELCH
        message.demodRequest.level = value
        self.sock.send(message.SerializeToString())

    def dialogClosed(self):
        self.setWindowMode(self.lastMode)

    def tryConnect(self, address, port):
        self.connectDialog.tryConnect(address, port)

class HostWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, address=None, port=None):
        super(HostWindow, self).__init__(parent)

        form = PiScanClient(self, address, port)

        mainWidget = form.mainWidget()
        self.setPalette(mainWidget.palette())
        self.setGeometry(mainWidget.geometry())
        self.setWindowTitle(mainWidget.windowTitle())

        self.setCentralWidget(mainWidget)
        #self.actionQuit.triggered.connect(self.closeEvent)

        self.show()

        if address:
            if not port:
                port = constants.DEFAULT_TCP_PORT
            form.tryConnect(address, port)

    def closeEvent(self, event):
        print('exit')
        common.getApp().closeEvent(event)
        event.accept()

if __name__ == '__main__':
    shortOpts = 'la:p:'
    longOpts = ['--local', '--address', '--port']

    options, remainder = getopt.getopt(sys.argv[1:], shortOpts, longOpts)

    address = None
    port = None

    for opt, arg in options:
        if opt in ('-l', '--local'):
            address = 'localhost'
        elif opt in ('-a', '--address'):
            address = arg
        elif opt in ('-p', '--port'):
            port = int(arg)

    app = QApplication(sys.argv)
    window = HostWindow(address=address, port=port)
    sys.exit(app.exec_())


