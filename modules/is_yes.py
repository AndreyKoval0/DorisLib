from .base import Module

class IsYes(Module):
    def exec(self, question):
        return "да" in question.lower().split()