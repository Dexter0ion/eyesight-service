from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

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
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initGUI()
    
    def initGUI(self):
         # 读取QImage格 <MW= QImage()

        
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self._pixmap = QPixmap()
        self._imgtext = ""

        # 监视屏大小
        self.circleScale = 400
        self.masktype = 1
        # 界面布局
        
        self.ilabel = QLabel()
        self.ilabel.setPixmap(self._pixmap)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.ilabel)
        

        # Add SwitchButton
        self.switchCapture = QSwitchButton("","")
        self.switchCapture.setSwitchName("Capture")

        self.switchFace= QSwitchButton("","")
        self.switchFace.setSwitchName("Face")

        self.switchNet = QSwitchButton("","")
        self.switchNet.setSwitchName("Net")

        self.switchYolo = QSwitchButton("","")
        self.switchYolo.setSwitchName("YOLO")
        self.switchSets = [self.switchCapture,self.switchFace,self.switchNet,self.switchYolo]

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
    def updateFrame(self, imgdata):
        self._imgdata = imgdata
        self._pixmap = mask_image(self.masktype, self._imgdata, self.circleScale)
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

    if(masktype == 0):
        painter.drawEllipse(0, 0, imgsize, imgsize)  # 画圆
    elif(masktype == 1):
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
