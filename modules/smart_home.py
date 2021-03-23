import requests
import json
import os
from .base import Module


if os.path.isfile("config.json"):
    config = json.load(open("config.json"))

url = config["url"]
login = config["login"]
password = config["password"]

class SmartHome(Module):
    def exec(self, mode, name, value=None):
        if mode == "set":
            requests.post(f"{url}/smart_home/set_value/", data={"login": login, "password": password, name: value})
            return "Хорошо"
