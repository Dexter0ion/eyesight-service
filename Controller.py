'''
    author:dexter0ion

    update:2018/11/27
    features:
        1.import MainWindow GUI
        2.create Signal Adapter
        
'''

import sys
import cv2
import numpy

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import qtmodern.styles
import qtmodern.windows

from Window import MainWindow
#from VService import *
from Service.ServCapture import ServCapture
from Service.ServFlask import ServFlask 
from Service.ServFaceRecog import ServFaceRecog
from Service.ServYOLO import ServYOLO

class ServNet(QThread):
    servFlask = ServFlask()
    signal_netcmd = pyqtSignal(str)
    netcmd = "NOCMD"
    def run(self):
        print("[开启]Flask服务器线程")
        self.servFlask.run()
        self.cmd = self.servFlask.out()
        if self.netcmd != "NOCMD":
            self.signal_netcmd.emit(self.netcmd)
            self.servFlask.getin("NOCMD")
        

    def stop(self):
        print('[关闭]Flask服务器')
        self.servFlask.stop()
    
    '''
    def updateFrame(self, imgdata):
            #print("更新服务器画面帧")
            #print(imgdata)
            self.netcompo.setFrame(imgdata)
            #self.netcompo.testPosttoServer()

    def getSwitchSignal(self, swsignal):
            s = swsignal
            print(s)
    '''
class ServEC(QThread):
    signal_QImage = pyqtSignal(QImage)

    switchFlag = {}

    def __init__(self):
        super().__init__()
        self.initServ()

    def initServ(self):
        self.servCapture = ServCapture(0)
        #self.cap= cv2.VideoCapture(0)
        self.servFaceRecog = ServFaceRecog()
        self.servYOLO = ServYOLO()

        self.switchFlag['Capture'] = True
        self.switchFlag['Face'] = False
        self.switchFlag['Net'] = False
        self.switchFlag['YOLO'] = False
        #print(self.servCapture)
        print(self.servFaceRecog)
    
    def servOut(self,serv):
        serv.getin(self._frame)
        serv.process()
        self._frame = serv.out()

    def processFrame(self):
        if self.switchFlag['Face'] == True:
            self.servOut(self.servFaceRecog)
        if self.switchFlag['YOLO'] == True:
            self.servOut(self.servYOLO)
        


    def getSignal(self,signal_dict):
        print(signal_dict)
        key = signal_dict['signal_key']
        value = signal_dict['signal_value']
        self.switchFlag[key] = value
        #print("key:"+key+" value:"+value)
        
    def run(self):
        while self.servCapture.isOpened():
            if self.switchFlag['Capture'] == True:
                self.servCapture.process()
                self._frame = self.servCapture.out()
                self.processFrame()

                self._frame_QImage = self.cvtNdarry2QImage(self._frame)
                self.signal_QImage.emit(self._frame_QImage)
        
    def cvtNdarry2QImage(self, ndarray):
        # in this class ndarry meands frame capture image
        vframe = ndarray
        # 采集摄像头线程
        height, width, bytesPerComponent = vframe.shape
        bytesPerLine = bytesPerComponent * width
        # 变换彩色空间顺序
        cv2.cvtColor(vframe, cv2.COLOR_BGR2RGB, vframe)
        qimg = QImage(vframe.data, width, height, bytesPerLine,
                      QImage.Format_RGB888)
        return qimg

class ServMana():
    servNet = ServNet()
    switchFlag = {}

    def getSignal(self,signal_dict):
        print(signal_dict)
        key = signal_dict['signal_key']
        value = signal_dict['signal_value']
        self.switchFlag[key] = value
        
        if self.switchFlag['Net'] == True:
            self.servNet.start()
        elif self.switchFlag['Net'] == False:
            self.servNet.stop()

class SignalAdapter():
    def __init__(self):
        pass

    def adapt(self, signal, function):
        signal.connect(function)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)
    #qtmodern.styles._apply_base_theme(app)

    ECGUI = MainWindow()
    #ECGUI = qtmodern.windows.ModernWindow(MainWindow())
    servEC = ServEC()
    servEC.start()
    
    servMana = ServMana()
      
    sigAda = SignalAdapter()
    sigAda.adapt(servEC.signal_QImage, ECGUI.updateFrame)
    sigAda.adapt(ECGUI.switchCapture.signal_switch,servEC.getSignal)
    sigAda.adapt(ECGUI.switchFace.signal_switch,servEC.getSignal)
    sigAda.adapt(ECGUI.switchYolo.signal_switch,servEC.getSignal)
    sigAda.adapt(ECGUI.switchMask.signal_switch,ECGUI.getSignal)
    sigAda.adapt(ECGUI.switchNet.signal_switch,servMana.getSignal)
    
    '''
    for switch in ECGUI.switchSets:
        sigAda.adapt(switch.switchSignal,servEC.getSignal)
        sigAda.adapt(switch.switchSignal,servMana.getSignal)
    '''
    #show MainWindow
    ECGUI.resize(500, 400)
    ECGUI.show()
    app.exit(app.exec_())