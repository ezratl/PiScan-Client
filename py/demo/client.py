#test.py
#try:
#   import tkinter as tk  # for python 3
#except:
#    import Tkinter as tk  # for python 2
import pygubu

import tkinter as tk
from ttk import *

from socket import *
from threading import Thread

import messages_pb2
import context_pb2
import request_pb2

import google.protobuf.message as proto


class Application: 
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()
        self.master = master

        #2: Load an ui file
        builder.add_from_file('clientwindow.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('MainWindow', master)
        self.addrdialog = builder.get_object('AddressDialog', master)
        self.mandialog = builder.get_object('ManualDialog', master)
        self.ScanTab = builder.get_object('ScanTab', master)
        self.HoldTab = builder.get_object('HoldTab', master)
        self.DisplayNotebook = builder.get_object('DisplayNotebook', master)

        builder.connect_callbacks(self)
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.onClose)

        self.addrdialog.show()

        self.sock = socket(AF_INET, SOCK_STREAM)

        self.rcv_thread = Thread(target=self.receive)
        self.inmsg = messages_pb2.ServerToClient()

        self.lastGainVal = 0
        self.lastSquelchSlide = 0
        self._job = None

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
                self.inmsg.ParseFromString(data)
                self.decodeMessage(message=self.inmsg)
            except OSError:
                break
            except proto.DecodeError as e:
                print("Parse error")
                print(e)

    def decodeMessage(self, message):
        print(message)
        if message.type == messages_pb2.ServerToClient.Type.SCANNER_CONTEXT:
            self.handleScannerContext(context = message.scannerContext)
        elif message.type == messages_pb2.ServerToClient.Type.DEMOD_CONTEXT:
            self.handleDemodContext(context=message.demodContext)

    def handleScannerContext(self, context):
        if context.state == context_pb2.ScannerContext.State.SCAN:
            self.doStateScan(context=context)
        elif context.state == context_pb2.ScannerContext.State.HOLD:
            self.doStateHold(context=context)
        elif context.state == context_pb2.ScannerContext.State.RECEIVE:
            self.doStateHold(context=context)

    def handleDemodContext(self, context):
        SquelchScale = self.builder.get_object('SquelchScale', self.master)
        GainScale = self.builder.get_object('GainScale', self.master)
        SquelchLabel = self.builder.get_object('SquelchLabel', self.master)
        GainLabel = self.builder.get_object('GainLabel', self.master)

        SquelchScale.configure(value=context.squelch)
        GainScale.configure(value=context.gain)

        SquelchLabel.configure(text=context.squelch)
        if context.gain < 0:
            GainLabel.configure(text='Auto')
        else:
            GainLabel.configure(text=context.gain)

    '''------------------------------------------'''

    def doStateScan(self, context):
        self.DisplayNotebook.tab(0, state='normal')
        self.DisplayNotebook.tab(1, state='disabled')
        self.DisplayNotebook.select(0)

    def doStateHold(self, context):
        entrynum = self.builder.get_object('EntryNumLabel', self.master)
        systag = self.builder.get_object('SysTagLabel', self.master)
        entrytag = self.builder.get_object('EntryTagLabel', self.master)
        freq = self.builder.get_object('FreqLabel', self.master)
        modulation = self.builder.get_object('ModulationLabel', self.master)
        strength = self.builder.get_object('SignalBar', self.master)

        if context.state == context_pb2.ScannerContext.State.HOLD:
            strength.configure(value=0)
        elif context.state == context_pb2.ScannerContext.State.RECEIVE:
            strength.configure(value=100)

        entrynum.configure(text=context.entryIndex)
        systag.configure(text=context.systemTag)
        entrytag.configure(text=context.entryTag)
        freq_formatted = str(float(context.freq) / 1000000)
        freq.configure(text=(freq_formatted + "MHz"))
        modulation.configure(text=context.modulation)
        
        self.DisplayNotebook.tab(0, state='disabled')
        self.DisplayNotebook.tab(1, state='normal')
        self.DisplayNotebook.select(1)

    '''------------------------------------------'''

    def onClose(self):
        self.sock.close()
        self.master.destroy()

    def handleButton1(self):
        message = messages_pb2.ClientToServer()
        message.type = messages_pb2.ClientToServer.Type.SCANNER_STATE_REQUEST
        message.scanStateRequest.state = request_pb2.ScannerStateRequest.NewState.SCAN
        self.sock.send(message.SerializeToString())

    def handleButton2(self):
        message = messages_pb2.ClientToServer()
        message.type = messages_pb2.ClientToServer.Type.SCANNER_STATE_REQUEST
        message.scanStateRequest.state = request_pb2.ScannerStateRequest.NewState.HOLD
        print(message)
        self.sock.send(message.SerializeToString())

    def handleButton3(self):
        self.mandialog.show()

    def handleButton4(self):
        print("button4")

    def handleGainSlider(self, value):
        self.lastGainVal = value
        if self._job:
            self.master.after_cancel(self._job)
        self._job = self.master.after(100, self.setGain)

    def setGain(self):
        self._job = None
        val = float(self.lastGainVal)
        #if abs(val - self.lastGainSlide) < 0.25:
        message = messages_pb2.ClientToServer()
        message.type = messages_pb2.ClientToServer.Type.DEMOD_REQUEST
        message.demodRequest.type = request_pb2.DemodRequest.DemodFunc.SET_GAIN
        message.demodRequest.level = val
        self.sock.send(message.SerializeToString())
        #self.lastGainSlide = val

    def handleSquelchSlider(self, value):
        val = float(value)
        if abs(val - self.lastSquelchSlide) < 0.5:
            message = messages_pb2.ClientToServer()
            message.type = messages_pb2.ClientToServer.Type.DEMOD_REQUEST
            message.demodRequest.type = request_pb2.DemodRequest.DemodFunc.SET_SQUELCH
            message.demodRequest.level = val
            self.sock.send(message.SerializeToString())
        self.lastSquelchSlide = val

    def handleConnect(self):
        print("connect")
        host = self.builder.get_object('AddrEntry', self.master).get()
        port = int(self.builder.get_object('PortEntry', self.master).get())
        print(host, ':', port)
        addr = (host, port)
        try:
            self.sock.connect(addr)
            print("Connection success")
            self.addrdialog.close()
            self.rcv_thread.start()
        except:
            print("Connection failed")

    def handleTune(self):
        freq = self.builder.get_object('FreqEntry', self.master).get()
        freq = int(float(freq) * 1000000)

        message = messages_pb2.ClientToServer()
        message.type = messages_pb2.ClientToServer.Type.SCANNER_STATE_REQUEST
        message.scanStateRequest.state = request_pb2.ScannerStateRequest.NewState.MANUAL
        message.scanStateRequest.manFreq = freq
        self.sock.send(message.SerializeToString())
        
        self.mandialog.close()


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = Application(root)
    root.mainloop()
