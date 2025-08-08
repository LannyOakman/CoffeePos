from models.coffee_db import CoffeeDb

class Product:
    def __init__(self, id, p_name, p_type, price):
        self.id = id
        self.p_name = p_name
        self.p_type = p_type
        self.price = price
        
    def fetchProducts(db: CoffeeDb) -> list:
        q = f"SELECT * FROM product"
        
        db.connect()
        db.cursor.execute(q)
        
        rows = db.cursor.fetchall()
        
        db.close()
        
        products = []
        
        for row in rows:
            products.append(
                Product(
                    id=row[0],
                    p_name=row[1],
                    p_type=row[2],
                    price=row[3],
                )
            )
        
        return products

        
        