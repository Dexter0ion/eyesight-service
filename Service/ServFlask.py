from flask import Flask, render_template, Response, request,g
import requests

class ServFlask():
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

