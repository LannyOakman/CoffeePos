from models.coffee_db import CoffeeDb

class Staff:
    def __init__(self, first_name: str, last_name: str, id = None):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        
    def create(first_name, last_name, db: CoffeeDb):
        q = f"INSERT INTO staff (first_name, last_name) VALUES ('{first_name}', '{last_name}')"
        
        db.execute(q, close_conn=False)
        
        id = db.cursor.lastrowid
        
        db.close()
                
        return Staff(
            first_name=first_name,
            last_name=last_name,
            id=id
        )
        
    def fetch(id: int, db: CoffeeDb):
        q = f"SELECT * FROM staff WHERE id = {id}"
        
        db.connect()
        db.cursor.execute(q)

        top = db.cursor.fetchone()
        
        db.close()
        
        return Staff(
            id=top[0],
            first_name=top[1],
            last_name=top[2]
        )