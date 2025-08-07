import mysql.connector
import os
from dotenv import load_dotenv
from utilities import clearTerminal
from models.coffee_db import CoffeeDb

class CoffeePos:
    def __init__(self, db: CoffeeDb):
        self._db = db
            
    def takeOrderOrSeeSalesData(self):
        print(
            "Take a coffee order    [1]\n"
            "Review sales data      [2]\n"
        )
        
    def createEmployee(self):
        first_name =  input("First Name: ")
        last_name = input("Last Name: ")
        
        
        
    def start(self):
        
        print(
            f"\n{'-' * 22}Welcome to CoffeePOS{'-' * 22}\n",
            "Navigate the prompts to take coffee orders and view sales data\n\n"
            "Log in with Employee ID    [1]\n"
            "Create Employee ID         [2]\n"
        )
        
        a = ""
        
        while not (a == '1' or a == '2'):
            a = input("Please enter a select 1 or 2: ")
            
        clearTerminal()
        
        if (a == '1'):
            self.takeOrderOrSeeSalesData()
        else:
            self.createEmployee()