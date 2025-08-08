from models.coffee_db import CoffeeDb

class Customer:
    def __init__(self, first_name, last_name, id):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        
    def create(first_name, last_name, db: CoffeeDb):
        q = f"INSERT INTO customer (first_name, last_name) VALUES ('{first_name}', '{last_name}')"
        
        db.execute(q, close_conn=False)
        
        id = db.cursor.lastrowid
        
        db.close()

        return Customer(
            first_name=first_name,
            last_name=last_name,
            id=id
        )
    
    def fetch(id: int, db: CoffeeDb):
        q = f"SELECT * FROM customer WHERE id = {id}"
        
        db.connect()
        db.cursor.execute(q)

        top = db.cursor.fetchone()
        
        db.close()
        
        return Customer(
            id=top[0],
            first_name=top[1],
            last_name=top[2]
        )