import argparse
import json
import os.path
import sys

import cv2 as cv
import numpy as np

class ServYOLO():
    # Initialize the parameters
    confThreshold = 0.5  # Confidence threshold
    nmsThreshold = 0.4  # Non-maximum suppression threshold
    inpWidth = 416  # Width of network's input image
    inpHeight = 416  # Height of network's input image

    isWriteEnable = False
    '''
    parser = argparse.ArgumentParser(description='Object Detection using YOLO in OPENCV')
    parser.add_argument('--image', help='Path to image file.')
    parser.add_argument('--video', help='Path to video file.')
    args = parser.parse_args()
    '''
    # Load names of classes
    classesFile = "yolodatas/coco.names"
    classes = None
    with open(classesFile, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')

    # 初始化检测结果统计表
    cntClassIds = []
    for i in range(0, len(classes)):
        cntClassIds.append(0)
    # Give the configuration and weight files for the model and load the network using them.
    modelConfiguration = "yolodatas/yolov3.cfg"
    modelWeights = "yolodatas/yolov3.weights"

    net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

    def __init__(self):
        self.inframe = None
        self.outframe = None

    def __str__(self):
        return "ServYOLO:Service-YOLO-ObjectDetect"

    def getin(self,frame):
        self.inframe = frame

    def process(self):
        self.outframe = self.procxFrame(self.inframe)
        

    def out(self):
        return self.outframe
    
    # Write to det.txt file
    def write2txt(imgname, classname, left, top, right, bottom):
        det = open('det.txt', 'a')
        det.write(imgname+"\n"+classname+"\n"+str(left)+" " +
                  str(top)+" "+str(right)+" "+str(bottom)+"\n")
        det.close()

    # Write to det.json file
    def write2json(imgname, classname, left, top, right, bottom):
        data = dict(catagory=classname, timestamp=1000, socre=0,
                    name=imgname, bbox=[left, top, right, bottom])
        datajson = json.dumps(data)

        f = open('det.json', 'a')
        f.write(datajson)
        f.write(",")
        f.close()

    # Get the names of the output layers
    def getOutputsNames(self, net):
        # Get the names of all the layers in the network
        layersNames = net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Draw the predicted bounding box
    def drawPred(self, frame, classId, conf, left, top, right, bottom):

        # Print class name
        #print(self.classes[classId])
        # Print bounding box location
        #print(left, top, right, bottom)

        #write2json(args.image[8:],classes[classId],left, top, right, bottom)
        # Draw a bounding box.
        cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

        label = '%.2f' % conf

        # Get the label for the class name and its confidence
        if self.classes:
            assert(classId < len(self.classes))
            label = '%s:%s' % (self.classes[classId], label)

        #Display the label at the top of the bounding box
        labelSize, baseLine = cv.getTextSize(
            label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        
        if self.isWriteEnable == True:
            baseline = 0
            refTop = top+baseline
            refBot = bottom-baseline
            refLeft = left+baseline
            refRight = right-baseline


            try:
                ref  = cv.resize(frame[refTop:bottom,refLeft:refRight],(refRight-refLeft,bottom-refTop))
            except:
                print("resize error")
            else:
                print("object resized")
                cv.imwrite('./objectdatas/%s.jpg' %(label), ref)

        #Draw Prediction
        cv.rectangle(frame, (left, top - round(1.5*labelSize[1])), (left + round(
            1.5*labelSize[0]), top + baseLine), (255, 255, 255), cv.FILLED)
        
        cv.putText(frame, label, (left, top),
                   cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)
        
        '''
        if self.isWriteEnable == True:
            refTop = top-round(1.5*labelSize[1])
            refLeft = left
            refRight = right+round(1.5*labelSize[0])

            try:
                ref  = cv.resize(frame[refTop:bottom,refLeft:refRight],(refRight-refLeft,bottom-refTop))
            except:
                print("resize error")
            else:
                print("object resized")
                cv.imwrite('./objectdatas/%s.jpg' %(label), ref)
        '''
    def switchEnable(self,ename,estatus):
        print(ename)
        if ename == 'writePred':
            self.isWriteEnable = estatus
        


    def postprocess(self, frame, outs):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]

        classIds = []
        confidences = []
        boxes = []
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        classIds = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > self.confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)

                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        indices = cv.dnn.NMSBoxes(
            boxes, confidences, self.confThreshold, self.nmsThreshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            self.cntClassIds[classIds[i]] += 1
            self.drawPred(
                frame, classIds[i], confidences[i], left, top, left + width, top + height)

        #print("classes len:"+str(len(self.classes)))
        for id, cnt in enumerate(self.cntClassIds):
            if cnt != 0:
                print("Id:%s,Name:%s,Cnt:%s" % (id, self.classes[id], cnt))
                #self.msgSender.sendMessage("Id:%s,Name:%s,Cnt:%s" % (id, self.classes[id], cnt))
            self.cntClassIds[id] = 0

    def procxFrame(self, frame):
        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(
            frame, 1/255, (self.inpWidth, self.inpHeight), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        self.net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = self.net.forward(self.getOutputsNames(self.net))

        # Remove the bounding boxes with low confidence
        self.postprocess(frame, outs)

        # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the timings for each of the layers(in layersTimes)
        t, _ = self.net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (
            t * 1000.0 / cv.getTickFrequency())
        cv.putText(frame, label, (0, 15),
                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        return frame
