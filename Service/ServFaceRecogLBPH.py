'''
    Author:ShaoBochao
    Time:2019/4/20
'''
import cv2

class ServFaceRecogLBPH():
    #面部&眼部级联分类器
    face_cascade = cv2.CascadeClassifier('/cascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('/cascades/haarcascade_eye.xml')

    def __init__(self):
        pass

    def __str__(self):
        return "This is a face recognition service using LBPH method"

    def generateFaceData(self,camera,facename,faceid):
        
        count =0
        while(count<50):
            print("generate face data")
            ret, frame = camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)  #min max

            #裁剪灰度帧区域并将转换为200x200

            for (x, y, w, h) in faces:
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                f = cv2.resize(gray[y:y + h, x:x + w], (200, 200))

                cv2.imwrite('/facedatas/%s.%s.%s.jpg' %(facename,faceid,str(count)), f)
                count+=1
        #camera.release()

    def getin(self):
        pass

    def process(self):
        pass

    def out(self):
        pass
