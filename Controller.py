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
from Service.ServUDP import ServUDP
from Service.ServFaceRecogLBPH import ServFaceRecogLBPH

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
        self.servFaceRecogLBPH = ServFaceRecogLBPH()
        self.servYOLO = ServYOLO()
        self.servUDP = ServUDP('127.0.0.1',1082)
        self.switchFlag['Capture'] = True
        self.switchFlag['Face'] = False
        self.switchFlag['Net'] = False
        self.switchFlag['YOLO'] = False
        self.switchFlag['UDPLive'] = False

        #print(self.servCapture)
        print(self.servFaceRecog)
        print(self.servFaceRecogLBPH)

    def servOut(self, serv):
        serv.getin(self._frame)
        serv.process()
        self._frame = serv.out()

    def processFrame(self):
        if self.switchFlag['Face'] == True:
            self.servOut(self.servFaceRecog)
        if self.switchFlag['YOLO'] == True:
            self.servOut(self.servYOLO)
        if self.switchFlag['UDPLive'] == True:
            self.servUDP.getin(self._frame)
            self.servUDP.process()

    def getSignal(self, signal_dict):
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
    def stop(self):
        self.servCapture.releaseCamera()
    def restart(self):
        self.servCapture.releaseCamera()
        self.servCapture.setCamera(0)
                
            

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


class ThreadManager():
    servNet = ServNet()
    servEC = ServEC()
    switchFlag ={}

    def getSignal(self, signal_dict):
        print("[Thread Signal]")
        print(signal_dict)
        
        key = signal_dict['signal_key']
        value = signal_dict['signal_value']
        self.switchFlag[key] = value

        
        if self.switchFlag['EC'] == True:
            self.servEC.start()
            #self.servEC.restart()
        if self.switchFlag['EC'] == False:
            self.servEC.stop()
        if self.switchFlag['Net'] == True:
            self.servNet.start()
        if self.switchFlag['Net'] == False:
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
    #servEC = ServEC()
    #servEC.start()

    thdm = ThreadManager()

    sigAda = SignalAdapter()
    sigAda.adapt(ECGUI.switchNet.signal_switch, thdm.getSignal)
    sigAda.adapt(ECGUI.switchEC.signal_switch, thdm.getSignal)
    
    sigAda.adapt(thdm.servEC.signal_QImage, ECGUI.windowLBPH.updateFrame)
    sigAda.adapt(thdm.servEC.signal_QImage, ECGUI.updateFrame)
    
    sigAda.adapt(ECGUI.switchCapture.signal_switch, thdm.servEC.getSignal)
    sigAda.adapt(ECGUI.switchFace.signal_switch, thdm.servEC.getSignal)
    sigAda.adapt(ECGUI.switchYolo.signal_switch, thdm.servEC.getSignal)
    sigAda.adapt(ECGUI.switchMask.signal_switch, ECGUI.getSignal)

    sigAda.adapt(ECGUI.switchCutObj.signal_switch, thdm.servEC.servYOLO.getSignal)
    sigAda.adapt(ECGUI.switchPostObj.signal_switch, thdm.servEC.servYOLO.getSignal)
    sigAda.adapt(ECGUI.switchUDPLive.signal_switch, thdm.servEC.getSignal)
    '''
    for switch in ECGUI.switchSets:
        sigAda.adapt(switch.switchSignal,servEC.getSignal)
        sigAda.adapt(switch.switchSignal,servMana.getSignal)
    '''
    #show MainWindow
    ECGUI.resize(500, 400)
    ECGUI.show()
    app.exit(app.exec_())