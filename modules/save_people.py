from .base import Module
import sqlite3
import pandas as pd

class SavePeople(Module):
    def exec(self, question):
        name_and_hobby = question.lower().replace("я занимаюсь", "").replace("привет", "").replace("моё хобби", "").replace("меня зовут", "").replace("привет", "").replace("моё имя", "")
        for word in name_and_hobby.split(" "):
            if word != '':
                name = word
                break
        self.interpretator.people_hobby = name_and_hobby.replace(name, "")
        self.interpretator.people_name = name
        path = "faces/"+self.interpretator.people_name
        df = pd.DataFrame({"PathToFace": [path], "Name": [self.interpretator.people_name], "Hobby": [self.interpretator.people_hobby]})
        conn = sqlite3.connect('memory.db')
        df.to_sql("PEOPLES", conn, if_exists='append', index = False)
        return f"Привет, {self.interpretator.people_name}"