from .interpretator import Interpretator
from .doris import Doris, train
from neural_networks.recognitionFace import FaceRecognition
from neural_networks.recognitionObject import ObjectRecognition
import json
import os

config = {}
if os.path.isfile("config.json"):
    config = json.load(open("config.json"))
interpretator = Interpretator()
doris = Doris()

running_program = None

def run_interpretator(cmd):
    global running_program
    if cmd == "exit":
        running_program = None
    answer = interpretator.run("QUESTION", cmd)
    return answer

def bot(cmd):
    global running_program
    if cmd == "exit":
        running_program = None
    answer = interpretator.run(cmd, doris.predict(cmd))
    return answer

def answering(cmd):
    global running_program
    if cmd == "exit":
        running_program = None
    answer = doris.predict(cmd)
    return answer


def exec(cmd):
    global config
    global running_program
    try:
        if cmd == "exit":
            exit()
        elif running_program == "interpretator":
            return run_interpretator(cmd)
        elif running_program == "bot":
            return bot(cmd)
        elif running_program == "answering":
            return answering(cmd)
        
        elif "run" in cmd:
            running_program = cmd.replace("run ", "")
        elif "set" in cmd:
            cmd = cmd.split("=")
            config[cmd[0].split(" ")[1].replace('"', '')] = cmd[1].replace('"', '')
            json.dump(config, open("config.json", "w"))
        elif cmd == "train answering":
            train(doris)
        elif cmd == "load":
            doris.load()
        elif cmd == "train recognition_face":
            rf = FaceRecognition("PEOPLES")
            rf.train()
            rf.save(f"models/{str(rf)}")
        elif cmd == "train recognition_object":
            ro = ObjectRecognition()
            ro.train()
            ro.save(f"models/{str(ro)}")
    except Exception as e:
        running_program = None
        return f"Error: {e}"