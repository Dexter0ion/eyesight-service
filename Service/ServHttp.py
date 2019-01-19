import requests
import json


class ServHttp():
    method = None
    in_data = None
    out_data = None
    url = None
    headers = None

    def __init__(self, method, url, in_data):
        self.method = method
        self.in_data = in_data
        self.url = url
        self.headers = {"Content-Type": "application/json"}

    def __str__(self):
        return "ServPostApi:Post Data to Flask Server"

    def getin(self, data):
        self.indata = data

    def process(self):
        cutdata = {"data":self.in_data}
        response = requests.post(
            self.url, data=json.dumps(cutdata), headers=self.headers)
        self.out_data = response.text

    def out(self):
        if self.out_data != None:
            return self.out_data
