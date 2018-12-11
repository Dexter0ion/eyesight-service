
class ServEC(QThread):
    signal_QImage = pyqtSignal(QImage)

    switchFlag = {}

    def __init__(self):
        super().__init__()
        self.initServ()

    def initServ(self):
        self.servCapture = ServCapture(1)
        self.servFaceRecog = ServFaceRecog()
        

        self.switchFlag['Capture'] = False
        self.switchFlag['Face'] = False
        self.switchFlag['Net'] = False

        print(self.servCapture)
        print(self.servFaceRecog)
    
    def servOut(self,serv):
        serv.getin(self._frame)
        serv.process()
        self._frame = serv.out()

    def processFrame(self):
        if self.switchFlag['Face'] == True:
            self.servOut(self.servFaceRecog)

        '''
        if self.isYoloOpen == True:
            self._frame = self.procObjectDetect(self._frame)
        '''
    def getSignal(self,signal_dict):
        print(signal_dict)
        key = signal_dict['signal_key']
        value = signal_dict['signal_value']
        self.switchFlag[key] = value
        #print("key:"+key+" value:"+value)
        
    def run(self):
        while self.servCapture.isOpened():
            self.servCapture.process()
            self._frame = self.servCapture.out()
            self.processFrame()

            #if self.switchFlag['Capture'] == True:
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
