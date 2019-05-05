from PyQt5.QtCore import pyqtSignal,QObject

class MessageSender(QObject):
    
    senderSignal = pyqtSignal(str)

    @property
    def msg(self):
        return self._msg
    @msg.setter
    def msg(self,value):
        self._msg = value

    def sendMessage(self,msg):
        if msg == None:
            self.senderSignal.emit(self.__msg)
        elif msg != None:
            self.senderSignal.emit(msg)

