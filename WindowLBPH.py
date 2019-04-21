from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *

from Widget.QAbout import QAbout
from Widget.QSimpleConsole import QSimpleConsole
from Widget.QSwitchButton import QSwitchButton
from Widget.QObjectList import QObjectList
from Service.ServFaceRecogLBPH import ServFaceRecogLBPH



class WindowLBPH(QMainWindow):
    def __init__(self):
        super().__init__()
        self.camera = None
        
        self.servFaceRecogLBPH = ServFaceRecogLBPH()
        self.initGUI()
        
    
    def generateFaceData(self):
        self.facename="test"
        self.faceid="0"
        print("[generate data]")
        self.servFaceRecogLBPH.generateFaceData(self.facename,self.faceid)
    
    def trainFaceModel(self):
        self.servFaceRecogLBPH.trainFaceModel()

    def initGUI(self):
        self.switchFlag = {}

        #设置窗口标题
        self.setWindowTitle('Face Recog LBPH')

        self.layout = QHBoxLayout()
        self._pixmap = QPixmap()
        self._imgtext = ""

        # Add QLabel
        self.ilabel = QLabel()
        self.ilabel.setPixmap(self._pixmap)
        self.layout.addWidget(self.ilabel)

        # Add SwitchButton
        self.switchGenerate = QSwitchButton("", "")
        self.switchGenerate.setSwitchName("Generate")

        self.switchTrain = QSwitchButton("", "")
        self.switchTrain.setSwitchName("Train")

        self.switchSets = [self.switchGenerate, self.switchTrain]

        for switch in self.switchSets:
            switch.setFixedSize(80, 80)
            self.layout.addWidget(switch)
        #set central widget
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setAutoFillBackground(True)
        '''
        palette = QPalette()  
        palette.setColor(Background, QColor(192,253,123,100))  

        self.centralWidget.setPalette(palette);  
        '''

    def getSignal(self, signal_dict):
        print(signal_dict)
        key = signal_dict['signal_key']
        value = signal_dict['signal_value']
        self.switchFlag[key] = value

    def updateFrame(self, imgdata):
        self._imgdata = imgdata
        self._pixmap = self.imgdata2QImage(self._imgdata)
        self.ilabel.setPixmap(self._pixmap)

    def imgdata2QImage(self, imgdata):
        image = imgdata
        image.convertToFormat(QImage.Format_ARGB32)
        image = QPixmap.fromImage(image)
        return image
