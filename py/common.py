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
    MANUAL_ENTRY = 1
    EDIT_ENTRY = 2
    SYSTEM_BROWSER = 3

class AppInterface:
    def completeConnection(self, sock):
        pass
