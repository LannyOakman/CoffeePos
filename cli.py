from coffee_pos import initPos
import os
from dotenv import load_dotenv
import mysql.connector

def main():
    
    try:
        conn = mysql.connector.connect(
            os.getenv("DB_HOST"),
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD")
        )
    except:
        print("Credentials Invalid. Create .env file with correct credentials")
        exit()
    
    initPos(conn)
    
if __name__ == '__main__':
    main()