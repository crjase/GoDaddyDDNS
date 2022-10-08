import json
import os


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Load:
    def __init__(self):
        self.filename = __location__ + "\\" + "config.json"


    def get_json(self):

        with open(self.filename) as file:
            config = json.load(file)

            return config