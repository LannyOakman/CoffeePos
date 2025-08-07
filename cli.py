from coffee_pos import CoffeePos
import os
from dotenv import load_dotenv
import mysql.connector


def main():

    load_dotenv()

    pos = CoffeePos(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    pos.start()


if __name__ == "__main__":
    main()
