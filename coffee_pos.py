import mysql.connector
import os
from dotenv import load_dotenv
from utilities import clearTerminal
from models.coffee_db import CoffeeDb
from models.staff import Staff

class CoffeePos:
    def __init__(self, db: CoffeeDb):
        self.db = db
        self.staff: Staff | None = None
    
    def takeOrderOrSeeSalesData(self):
        print(
            "Take a coffee order    [1]\n"
            "Review sales data      [2]\n"
        )
        
    def login(self):
        while True:
            try:
                id = int(input("Please enter Staff ID: "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        try:
            self.staff = Staff.fetch(id=id, db=self.db)
        except Exception as e:
            print(e)
            print("Invalid ID. Please ensure the ID is accurate")
            self.login()
        
        clearTerminal()
        
        print(f"Logged in as {self.staff.first_name} {self.staff.last_name}")
        self.takeOrderOrSeeSalesData()
        
        
    def createStaff(self):
        first_name: str =  input("First Name: ")
        last_name: str = input("Last Name: ")
        
        self.staff = Staff.create(first_name=first_name, last_name=last_name, db=self.db)
        
        print(
            f"{self.staff.first_name} {self.staff.last_name} associated with staff id {self.staff.id}\n"
        )
        
        a = input("Create another staff?\n"
              "Yes  [1]\n"
              "No   [2]\n")
        
        while not (a == '1' or a=='2'):
            a = input("Please select 1 or 2: ")
        
        clearTerminal()
        
        if (a == '1'):
            self.createStaff()
        else:
            self.start()
        
        
    def start(self):
        
        print(
            f"\n{'-' * 22}Welcome to CoffeePOS{'-' * 22}\n",
            "Navigate the prompts to take coffee orders and view sales data\n\n"
            "Log in with Staff ID    [1]\n"
            "Create Staff ID         [2]\n"
        )
        
        a = ""
        
        while not (a == '1' or a == '2'):
            a = input("Please select 1 or 2: ")
            
        clearTerminal()
        
        if (a == '1'):
            self.login()
        else:
            self.createStaff()