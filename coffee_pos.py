import mysql.connector
import os
from dotenv import load_dotenv
from utilities import clearTerminal
from models.coffee_db import CoffeeDb
from models.staff import Staff
from models.cutomer import Customer
from models.product import Product

class CoffeePos:
    def __init__(self, db: CoffeeDb):
        self.db = db
        self.staff: Staff | None = None
        self.customer: Customer | None = None
        self.products: Product | None = None
        self.productQuantity = []
    
    def createSaleAndSaleProduct(self):
        self.db.connect()
        
        q = f"INSERT INTO sale (staff_id, customer_id) VALUES ({self.staff.id}, {self.customer.id})"
        
        self.db.execute(q, close_conn=False)
        
        id = self.db.cursor.lastrowid
        
        for p, quant in self.productQuantity:
            q = f"INSERT INTO sale_product (sale_id, product_id, quantity) VALUES ({id}, {p.id}, {quant})"
            self.db.execute(q)
        
        self.db.close()
    
    def takeOrderOrSeeSalesData(self):
        print(
            "Take a coffee order    [1]\n"
            "Review sales data      [2]\n"
            "Quit                   [3]\n"
        )
        
        a = ''
        
        while a not in ['1','2','3']:
            a = input("\nPlease select 1-3: ")

        clearTerminal()
        
        if a == '1':
            self.customerEntry()
        elif a == '2':
            self.reviewSalesData()
        else:
            print("Exiting...")
            exit()
     
    def sumOrderPrice(self):
        clearTerminal()
        total = 0
        
        for (product, quantity) in self.productQuantity:
            total += (product.price) * quantity

        print(f"Customer pays ${total}\n")
        
        a = input(
            "New Customer               [1]\n"
            "Review sales data          [2]\n"
        )
        
        while a not in ['1', '2']:
            a = input("Please select 1 or 2: ")
        
        clearTerminal()
            
        if (a == '1'):
            self.customerEntry()
        else:
            self.reviewSalesData()
        
        
        
    def takeOrder(self):
        self.products = Product.fetchProducts(self.db)
        
        for i in range(len(self.products)):
            print(f"{self.products[i].p_name:<30}{self.products[i].price}     [{i}]")
        else:
             print(f"{"Submit":<30}        [{len(self.products)}]")
             
        a = -1
        
        while not (0 <= a <= len(self.products)):
            try:
                a = int(input(f"\nSelect a number, 0-{len(self.products)}: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        if (a == len(self.products)):
            if len(self.productQuantity) == 0:
                clearTerminal()
                print("Invalid input. Must purchase 1 item")
                self.takeOrder()
            else:
                self.createSaleAndSaleProduct()
                self.sumOrderPrice()
        
        q = None
        
        
        while True:
            try:
                q = int(input(f"Select {self.products[a].p_name} quantity: "))
                productInList = False
                for (p, q) in self.productQuantity:
                    
                    if (p == self.products[a]):
                        productInList = True
                        break
                if (productInList):
                    print("Invalid input. Product already chosen")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        
        self.productQuantity.append((self.products[a], q))
        
        clearTerminal()
        
        self.takeOrder() 
        
        
    def customerLogin(self):
        while True:
            try:
                id = int(input("Please enter Customer ID: "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.")
        try:
            self.customer = Customer.fetch(id=id, db=self.db)
        except Exception as e:
            print(e)
            print("Invalid ID. Please ensure the ID is accurate")
            self.customerLogin()
        
        clearTerminal()
        
        print(f"Logged in as {self.staff.first_name} {self.staff.last_name} \n")
        self.takeOrder()
        
    def customerEntry(self):
        a = input(
            "Log in with Customer ID    [1]\n"
            "Create Customer ID         [2]\n"
        )
        
        while a not in ['1', '2']:
            a = input("Please select 1 or 2: ")
            
        clearTerminal()
        
        if a == '1':
            self.customerLogin()
        else:
            self.createCustomer()
        
    def reviewSalesData(self):
        print(
            "View customers with more than 3 transactions       [1]\n"
            "Back                                               [2]\n"
        )
        
        a = ''
        
        while a not in ['1','2']:
            a = input("\nPlease select 1-2: ")
        
        clearTerminal()
        
        if (a == '2'):
            self.productQuantity = []
            self.takeOrderOrSeeSalesData()
        else:
            q = "SELECT c.first_name, c.last_name, count(*) as ct FROM coffee_pos.customer as c JOIN coffee_pos.sale as s ON c.id = s.customer_id JOIN coffee_pos.sale_product as sp ON s.id = sp.id GROUP BY c.id HAVING ct > 3"
            self.db.connect()
            
            self.db.cursor.execute(q)
            
            rows = self.db.cursor.fetchall()
            
            self.db.close()
            
            clearTerminal()
            
            print("Customers with more than 3 transactions")
            
            for row in rows:
                print(f"{row[0]}\t{row[1]}\tTransactions: {row[2]}")
            
            if (len(rows) == 0):
                print("No customers with more than 3 transactions")
            
            print("\n")
            
            a = input(
              "Take Order    [1]\n"
              "Exit          [2]\n"
            )

            while not (a == '1' or a=='2'):
                a = input("Please select 1 or 2: ")
        
            clearTerminal()
        
            if (a == '1'):
                self.customerEntry()
            else:
                print("Exiting...")
                exit()

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
            
    def createCustomer(self):
        first_name: str =  input("First Name: ")
        last_name: str = input("Last Name: ")
        
        self.customer = Customer.create(first_name=first_name, last_name=last_name, db=self.db)
        
        print(
            f"{self.customer.first_name} {self.customer.last_name} associated with customer id {self.staff.id}\n"
        )
        
        a = input("Create another customer?\n"
              "Yes  [1]\n"
              "No   [2]\n")
        
        while not (a == '1' or a=='2'):
            a = input("Please select 1 or 2: ")
        
        clearTerminal()
        
        if (a == '1'):
            self.createCustomer()
        else:
            self.start()
        
        with open('./sql/data.sql', 'r') as f:
            data = f.read()
            
        cmds = [cmd.strip() for cmd in data.split(';')]
        
        if (not self.dbIsPopulated()):
            self.execute(cmds, execute_seperate=True)
            
        
    def start(self):

        clearTerminal()
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

