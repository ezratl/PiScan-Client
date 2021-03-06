from enum import Enum

import constants

instance = None

def setInstance(app):
    global instance
    instance = app

def getApp():
    return instance

class WindowMode(Enum):
    CONNECT = constants.CONNECT_PAGE_INDEX
    SCANNER = constants.SCANNER_PAGE_INDEX
    DIALOG = constants.DIALOG_PAGE_INDEX

class ScannerMode(Enum):
    SCANNING = 0
    HOLD = 1
    RECEIVE = 1

class DialogMode(Enum):
    MANUAL_ENTRY = 0
    EDIT_ENTRY = 1
    SYSTEM_BROWSER = 2
    SYSTEM_SETTINGS = 3

class AppInterface:
    def completeConnection(self, sock):
        pass

    def scan(self):
        pass

    def hold(self):
        pass

    def manualEntry(self, frequency, modulation):
        pass

    def showManualEntryDialog(self):
        pass

    def showEditEntryDialog(self):
        pass

    def showEntryBrowser(self):
        pass

    def showSettingsDialog(self):
        pass

    def setGain(self, value):
        pass

    def setSquelch(self, value):
        pass

    def dialogClosed(self):
        pass

    def closeEvent(self, event):
        pass

    def tryConnect(self, address, port):
        pass

    def setWindowTitleInfo(self, message):
        pass

    def clearWindowTitleInfo(self):
        pass
