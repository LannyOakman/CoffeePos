from coffee_pos import CoffeePos
import os
from dotenv import load_dotenv
import mysql.connector
from models.coffee_db import CoffeeDb


def main():

    load_dotenv()

    coffeeDb = CoffeeDb(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    pos = CoffeePos(coffeeDb)
    pos.start()


if __name__ == "__main__":
    main()
