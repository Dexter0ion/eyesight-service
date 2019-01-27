import cv2
import numpy
import socket

class ServUDP():
    ip = None
    port = None
    jpeg_quality = 20
    in_frame = None
    out_frame = None

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.jpeg_quality]
        
        # initializing socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # bind socket to the port
        self.server_address = (self.ip, self.port)

    def __str__(self):
        return "ServUDP:Transifer Video Frame to Achieve LiveStream"

    def getin(self, frame):
        self.in_frame = frame

    def process(self):
        # process img data
        result, self.out_frame = cv2.imencode('.jpg', self.in_frame, self.encode_param)
        

        # send frame
        self.sock.sendto(self.out_frame.tobytes(), self.server_address)
  
    def out(self):
        return self.out_frame
