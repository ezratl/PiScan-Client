import sys

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QStackedWidget
from PySide2.QtCore import QFile, QObject, Signal

from socket import *
from threading import Thread

import common
import constants
import connect
import scanner

import messages_pb2
import context_pb2
import request_pb2

import google.protobuf.message as proto

class PiScanClient(QObject, common.AppInterface):
    dataReceived = Signal(bytes)

    def __init__(self, ui_file, parent=None):
        super(PiScanClient, self).__init__(parent)
        common.setInstance(self)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()

        self.dataReceived.connect(self.handleReceived)

        self.connectDialog = connect.ConnectDialog(self.window)
        self.scanner = scanner.Scanner(self.window)
        self.contextStack = self.window.findChild(QStackedWidget, 'contextStack')
        self.setWindowMode(common.WindowMode.CONNECT)
        #self.setWindowMode(common.WindowMode.SCANNER)

        self.window.destroyed.connect(self.onExit)

        self.window.show()

        self.inmsg = messages_pb2.ServerToClient()

    def setWindowMode(self, mode):
        self.mode = mode

        self.contextStack.setCurrentIndex(mode.value)

    def completeConnection(self, sock):
        self.sock = sock
        self.rcv_thread = Thread(target=self.receive)
        self.rcv_thread.start()
        self.setWindowMode(common.WindowMode.SCANNER)

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

    def onExit(self):
        print('Exiting...')
        if sock:
            self.sock.close()
            self.rcv_thread.join()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = PiScanClient('scan_client.ui')
    sys.exit(app.exec_())


