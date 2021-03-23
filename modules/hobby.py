from .base import Module

class Hobby(Module):
    def exec(self, question):
        return question.lower().replace("я занимаюсь", "").replace("привет", "").replace("моё хобби", "")