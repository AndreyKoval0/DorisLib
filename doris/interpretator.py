from datetime import datetime
from modules import *
import json
import os

config = {"bot_name": "Doris", "bot_hobby": "саморазвитие, познание, совершенствование"}
if os.path.isfile("config.json"):
    config = json.load(open("config.json"))

class Interpretator():
    def __init__(self):
        self.modules = {
            "save": Save,
            "search": Search,
            "calc": Calc,
            "weather": Weather,
            "name": Name,
            "hobby": Hobby,
            "is_yes": IsYes,
            "save_people": SavePeople,
            "recognize_object": RecognizeObject,
            "recognize_face": RecognizeFace,
            "learn": Learn,
            "smart_home": SmartHome
        }
        self.answers = []
        self.questions = []
        self.for_future = []
        self.bot_name = config["bot_name"]
        self.bot_hobby = config["bot_hobby"]
        self.people_name = "неизвестный человек"
        self.people_hobby = "неизвестное хобби"
        for label in list(self.modules):
            self.modules[label] = self.modules[label](self).exec
    
    def set_name(self, name): self.people_name = self.modules["name"](name)
    def set_hobby(self, hobby): self.people_hobby = self.modules["hobby"](hobby)

    def init_var(self, code):
        if 'NEXT_' in code:
            QUESTION = self.questions[len(self.questions)-1] if len(self.questions) >= 1 else ""
            ANSWER = self.answers[len(self.answers)-1] if len(self.answers) >= 1 else ""
            LAST_QUESTION = self.questions[len(self.questions)-2] if len(self.questions) >= 2 else ""
            LAST_ANSWER = self.answers[len(self.answers)-2] if len(self.answers) >= 2 else ""
            NEXT_QUESTION = self.question
            NEXT_ANSWER = self.answer
        else:
            QUESTION = self.question
            ANSWER = self.answer
            LAST_QUESTION = self.questions[len(self.questions)-1] if len(self.questions) >= 1 else ""
            LAST_ANSWER = self.answers[len(self.answers)-1] if len(self.answers) >= 1 else ""
            NEXT_QUESTION = None
            NEXT_ANSWER = None
        NAME = self.people_name
        HOBBY = self.people_hobby
        BOT_NAME = self.bot_name
        BOT_HOBBY = self.bot_hobby
        return QUESTION, ANSWER, LAST_QUESTION, LAST_ANSWER, NEXT_QUESTION, NEXT_ANSWER, NAME, HOBBY, BOT_NAME, BOT_HOBBY
    
    def exec(self, code):
        QUESTION, ANSWER, LAST_QUESTION, LAST_ANSWER, NEXT_QUESTION, NEXT_ANSWER, NAME, HOBBY, BOT_NAME, BOT_HOBBY = self.init_var(code)
        modules = self.modules
        return eval(code.strip())

    def run_for_future_code(self):
        answer = []
        for code in self.for_future:
            answer.append(self.exec(code))
        answer = str(" ".join(answer))
        self.for_future = []
        return answer

    def run_code(self, code):
        ans = []
        self.for_future = []
        for i in range(len(code)):
            if 'NEXT_' in code[i]:
                self.for_future.append(code[i])
                ans.append('')
            else:
                ans.append(self.exec(code[i]))
        return ans
    
    def get_stack(self, answer):
        stack = []
        for piece_code in answer.split("{"):
            if "}" in piece_code:
                code = piece_code.split("}")[0]
                answer = answer.replace(code, "")
                stack.append(code)
        return answer, stack

    def run(self, question, answer):
        self.questions.append(question)
        self.answers.append(answer)
        if self.for_future != []:
            answer = self.run_for_future_code()
            return answer
        elif len(self.questions) >= 2:
            self.question = self.questions[-2].lower()
            self.answer, stack = self.get_stack(self.answers[-2])
            responce = self.run_code(stack)
            if self.for_future != []:
                answer = self.run_for_future_code()
                return answer
        self.question = question.lower()
        self.answer, stack = self.get_stack(answer)
        responce = self.run_code(stack)
        answer = self.answer.format(*responce)
        return answer
