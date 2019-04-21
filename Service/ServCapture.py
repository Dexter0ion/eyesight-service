import cv2
import numpy

class ServCapture():
    camera_cv = None
    frame = None

    def __init__(self):
        pass

    def __str__(self):
        return 'ServCapture:Class to capture video frame'

    def process(self):
        #print(self.camera_cv)
        ret, self.frame = self.camera_cv.read()

    def out(self):
        return self.frame

    def setCamera(self,camera_index):
        '''
        if len(camera_index) != 0:
            self.camera_cv = cv2.VideoCapture(camera_index[0])
        else:
        '''
        self.camera_cv = cv2.VideoCapture(camera_index)
    
    def returnCamera(self):
        return self.camera_cv

    def releaseCamera(self):
        self.camera_cv.release()
        
    def isOpened(self):
        return self.camera_cv.isOpened()
    
