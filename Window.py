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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGUI()

    #显示关于界面
    def displayAbout(self):
        self.aboutDialog = QAbout(self)
        self.aboutDialog.show()

        print("About")

    def initGUI(self):
        self.switchFlag = {}

        #设置窗口标题
        self.setWindowTitle('Eyesight-Service')

        #设置菜单栏
        self.menubar = self.menuBar()
        helpMenu = self.menubar.addMenu('Help')

        #关于
        aboutAction = QAction('About', self)
        aboutAction.triggered.connect(self.displayAbout)
        helpMenu.addAction(aboutAction)

        #self.setAttribute(Qt.WA_TranslucentBackground)
        self._pixmap = QPixmap()
        self._imgtext = ""

        # 监视屏大小
        self.circleScale = 400
        self.switchFlag['Mask'] = False
        #self.masktype = 1

        # 界面布局
        self.layout = QHBoxLayout()
        # Add QLabel
        self.ilabel = QLabel()
        self.ilabel.setPixmap(self._pixmap)
        self.layout.addWidget(self.ilabel)

        # Add QSimple Console
        self.console = QSimpleConsole()
        self.layout.addWidget(self.console)

        # Add ObjectList
        self.objectList = QObjectList()
        self.layout.addWidget(self.objectList)

        # Add SwitchButton
        self.switchCapture = QSwitchButton("", "")
        self.switchCapture.setSwitchName("Capture")

        self.switchFace = QSwitchButton("", "")
        self.switchFace.setSwitchName("Face")

        self.switchNet = QSwitchButton("", "")
        self.switchNet.setSwitchName("Net")

        self.switchYolo = QSwitchButton("", "")
        self.switchYolo.setSwitchName("YOLO")

        self.switchMask = QSwitchButton("", "")
        self.switchMask.setSwitchName("Mask")

        self.switchCutObj = QSwitchButton("","")
        self.switchCutObj.setSwitchName("CutObj")

        self.switchPostObj = QSwitchButton("","")
        self.switchPostObj.setSwitchName("PostObj")
        
        self.switchUDPLive = QSwitchButton("","")
        self.switchUDPLive.setSwitchName("UDPLive")

        self.switchSets = [
            self.switchCapture, self.switchFace, self.switchNet,
            self.switchYolo, self.switchMask, self.switchCutObj,self.switchPostObj,self.switchUDPLive
        ]

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
        self._pixmap = mask_image(self.switchFlag['Mask'], self._imgdata,
                                  self.circleScale)
        self.ilabel.setPixmap(self._pixmap)


def mask_image(masktype, imgdata, size, imgtype='jpg'):
    # Load image and convert to 32-bit ARGB (adds an alpha channel):
    #image = QImage.fromData(imgdata, imgtype)
    image = imgdata
    image.convertToFormat(QImage.Format_ARGB32)

    # 将图像切割为正方形
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
    )

    image = image.copy(rect)

    # 以相同维度和alpha channel创建输出图像
    # 透明化

    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    # 创建texture brush 画圆 onto out_img
    brush = QBrush(image)  # 创建texture brush
    painter = QPainter(out_img)
    # 设置painter
    painter.setBrush(brush)
    painter.setPen(Qt.NoPen)  # 无边框
    painter.setRenderHint(QPainter.Antialiasing, True)  # 抗锯齿

    if (masktype == True):
        painter.drawEllipse(0, 0, imgsize, imgsize)  # 画圆
    elif (masktype == False):
        painter.drawRect(0, 0, imgsize, imgsize)
    painter.end()  # segfault if you forget this

    # 将image转换为pixmap病重定义大小
    # 设置分辨率适应高清屏
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    return pm
