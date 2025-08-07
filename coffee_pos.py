import mysql.connector
import os
from dotenv import load_dotenv

class CoffeePos:
    def __init__(self, host, user, password):
        self._host = host
        self._user = user
        self._password = password
        self._database = None
        self._conn = None
        self._cursor = None
        
    def connect(self):
        if self._conn is None or not self._conn.is_connected():
            try:
                self._conn = mysql.connector.connect(
                    host=self._host,
                    user=self._user,
                    password=self._password,
                    database=self._database
                )
                
                self._cursor = self._conn.cursor()

            except Exception as e:
                print(e)
                raise
    
    def close(self):
        if self._cursor != None:
            self._cursor.close()
            self._cursor = None
        if self._conn != None:
            self._conn.close()
            self._conn = None
        
    def execute(self, cmds: list | str, execute_seperate = False):
        self.connect()
            
        if isinstance(cmds, str):
            cmds = [cmds]
            
        for cmd in cmds:
          self._cursor.execute(cmd)
          if (execute_seperate): self._conn.commit()
        
        self._conn.commit()
        self.close()

    def createDB(self):
        with open('./sql/db.sql', 'r') as f:
            dbCmd = f.read()

        self.execute(dbCmd)

        self._database = 'coffee_pos'
    
    def createSchemas(self):
        with open('./sql/schema.sql', 'r') as f:
            schemaCmds = f.read()

        cmds = schemaCmds.split(';')

        clean_cmds = [cmd.strip() for cmd in cmds]
        
        self.execute(clean_cmds)
    
    def dbIsPopulated(self):
        self.connect()
        self._cursor.execute("SELECT COUNT(*) FROM staff")
        count = self._cursor.fetchone()[0]
        self.close()
        return count != 0
    
    def populateDB(self):
        
        with open('./sql/data.sql', 'r') as f:
            data = f.read()
            
        cmds = [cmd.strip() for cmd in data.split(';')]
        
        if (not self.dbIsPopulated()):
            self.execute(cmds, execute_seperate=True)
            
        
    def start(self):
        self.createDB()
        self.createSchemas()
        self.populateDB()