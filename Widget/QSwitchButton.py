from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QObject, pyqtSignal

class QSwitchButton(QPushButton):
    signal_switch = pyqtSignal(dict)

    def __init__(self, onasset, offasset):

        super().__init__()

        self.switchName = ""
        self.onasset = onasset
        self.offasset = offasset

        #self.setStyleSheet('QPushButton{border-image:url('+self.offasset+')}')
        # self.setStyleSheet('QPushButton{background-image:url('+self.offasset+')}')
        self.isoff = True

        self.clicked.connect(self.changeSwitchButtonImage)
        self.clicked.connect(self.clieckedCallFunction)

    def setSwitchName(self, switchName):
        self.switchName = switchName
        self.setText(self.switchName+"\noff")

    def clieckedCallFunction(self):
        print(self.sender().switchName+" is cliecked")

    def changeSwitchButtonImage(self):
        print("Pushbutton Image changed")
        if self.isoff:
            # self.setStyleSheet('QPushButton{background-image:url('+self.onasset+')}')
            #self.setStyleSheet(    'QPushButton{border-image:url('+self.onasset+')}')
            self.setText(self.switchName+"\non")
            #self.switchSignal.emit("on")
            self.signal_switch.emit({'signal_key':self.switchName,'signal_value':True})
            self.isoff = False
        elif self.isoff == False:
            # self.setStyleSheet('QPushButton{background-image:url('+self.offasset+')}')
            #self.setStyleSheet(    'QPushButton{border-image:url('+self.offasset+')}')
            self.setText(self.switchName+"\noff")
            #self.switchSignal.emit("off")
            self.signal_switch.emit({'signal_key':self.switchName,'signal_value':False})
            self.isoff = True
    