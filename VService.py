'''
    author:dexter0ion

    update:2018/12/8
    features:
        1.add flask server

    update:2018/11/27
    features:
        1.create ServFaceRecog:Class to process face recognition
    
    update:2018/11/23
    features:
        1.create abstrct class VService
        2.create ServEmail:Class to send email'
'''
import smtplib
from abc import ABCMeta, abstractmethod
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr

import cv2
import face_recognition

from flask import Flask, render_template, Response, request,g
import numpy
import requests
class VService():
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return "This is a abstract server class."

    def getin(self):
        pass

    def process(self):
        pass

    def out(self):
        pass


class ServCapture(VService):
    camera_cv = None
    frame = None

    def __init__(self, *camera_index):
        if len(camera_index) != 0:
            self.camera_cv = cv2.VideoCapture(camera_index[0])
        else:
            self.camera_cv = cv2.VideoCapture(0)
    

    def __str__(self):
        return 'ServCapture:Class to capture video frame'

    def process(self):
        #print(self.camera_cv)
        ret, self.frame = self.camera_cv.read()

    def out(self):
        return self.frame

    def isOpened(self):
        return self.camera_cv.isOpened()


class ServEmail(VService):
    sender = None
    password = None
    recevier = None
    smtp_server = None

    def __init__(self, sender, password, recevier, smtp_server):
        self.sender = sender
        self.password = password
        self.recevier = recevier
        self.smtp_server = smtp_server

    def __str__(self):
        return 'ServEmail:Class to send email'

    def trysendone(self):
        #from_addr = input('From: ')
        #password = input('Password: ')
        #to_addr = input('To: ')
        #smtp_server = input('SMTP server: ')

        msg = MIMEText('爱你爱你爱你爱你爱你', 'plain', 'utf-8')
        msg['From'] = Header("超超的Sever-ServEC", 'utf-8')
        msg['To'] = Header("JUJU", 'utf-8')
        msg['Subject'] = Header(u'晚安宝宝', 'utf-8').encode()

        try:
            server = smtplib.SMTP(self.smtp_server)
            server.set_debuglevel(1)
            server.login(self.sender, self.password)
            server.sendmail(self.sender, [self.recevier], msg.as_string())
            server.quit()
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")


class ServFaceRecog():
    inframe = None
    outframe = None

    master_image = face_recognition.load_image_file("facedatas/master.jpg")
    master_face_encoding = face_recognition.face_encodings(master_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [master_face_encoding]
    known_face_names = ["master"]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    def __init__(self):
        # load master picture

        pass

    def __str__(self):
        return 'ServFaceRecog:Class to process face recognition'

    def getin(self, frame):
        self.inframe = frame

    def process(self):
        self.outframe = self.inframe
            # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(self.outframe, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                face_names.append(name)

        #process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(self.outframe, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(self.outframe, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(self.outframe, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    def out(self):
        return self.outframe


class ServFlask(VService):
    app = Flask(__name__)
    
    cmd = "NOCMD"
    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
    
    @app.route('/open_camera')
    def open_camera():
        print("post:open_camera")
        return("open_camera")
        
    def __init__(self):
        pass

    def __str__(self):
        return "This is a abstract server class."

    def getin(self,cmd):
        self.cmd = cmd

    def run(self):
        self.app.run(host='0.0.0.0',port=5001,threaded=True)
    
    def stop(self):
        #self.shutdown()
        requests.post('http://localhost:5001/shutdown')

    def out(self):
        return g.cmd
