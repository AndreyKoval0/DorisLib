from .base import Module
import pandas as pd
import sqlite3

class Save(Module):
    def exec(self, data, table):
        df = pd.DataFrame({"Question": [data[0]], "Answer":[data[1]]})
        conn = sqlite3.connect('memory.db')
        df.to_sql(table, conn, if_exists='append', index = False)
        return ''