import mysql.connector
import os
from dotenv import load_dotenv

class CoffeePos:
    def __init__(self, conn: mysql.connector):
        print(conn)
        

def initPos():
    return CoffeePos()