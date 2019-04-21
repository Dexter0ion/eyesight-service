'''
    Author:ShaoBochao
    Time:2019/4/20
'''
import cv2
import os
import numpy as np
from PIL import Image

class ServFaceRecogLBPH():
    def __init__(self):
        #面部&眼部级联分类器
        self.face_cascade = cv2.CascadeClassifier(
            'cascades/haarcascade_frontalface_default.xml')

        print("[load cascade]")
        #面部数据集
        self.path = 'facedatasLBPH'
        #训练模型数据集
        self.modelpath = 'modelLBPH'

    def __str__(self):
        return "This is a face recognition service using LBPH method"

    #获取图像和标记数据

    def getImageAndLabels(self,path):

        #合并目录 一个list
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []

        for iPath in imagePaths:
            PIL_img = Image.open(iPath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')

            #获取标签及面部特征
            id = int(os.path.split(iPath)[-1].split(".")[1])
            faces = self.face_cascade.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)

        return faceSamples, ids

    def trainFaceModel(self):
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = self.face_cascade

        print(
            "\n [INFO] 面部数据训练中...|Training faces. It will take a few seconds. Wait ..."
        )
        faces, ids = self.getImageAndLabels(self.path)
        recognizer.train(faces, np.array(ids))
        print("\n [Success] 训练完成|Training Complete")
        print("\n [Writing] 写出外部数据中...")
        recognizer.save(self.modelpath+'/trainer.yml')
        recognizer.save(self.modelpath+'/trainer.xml')
        print("\n [Success] 写出完成|Writing Complete")

    def generateFaceData(self, facename, faceid):
        camera = cv2.VideoCapture(0)
        count = 0

        while (count < 50):
            ret, frame = camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)  #min max

            print("detect cascades")
            #裁剪灰度帧区域并将转换为200x200

            for (x, y, w, h) in faces:
                img = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0),
                                    2)

                f = cv2.resize(gray[y:y + h, x:x + w], (200, 200))

                cv2.imwrite(
                    self.path +
                    '/%s.%s.%s.jpg' % (facename, faceid, str(count)), f)
                count += 1

            cv2.imshow("face generate", frame)

            if cv2.waitKey(0) & 0xff == ord("q"):
                break
            #if cv2.waitKey(1000/12)&0xff == ord("q"):
            #    break

        camera.release()
        cv2.destroyAllWindows()

    def getin(self):
        pass

    def process(self):
        pass

    def out(self):
        pass
