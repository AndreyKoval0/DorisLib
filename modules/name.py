from .base import Module

class Name(Module):
    def exec(self, question):
        return question.lower().replace("меня зовут", "").replace("привет", "").replace("моё имя", "")