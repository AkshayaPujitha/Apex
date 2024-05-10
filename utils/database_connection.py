from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
load_dotenv()

class DataBaseConnection():
    def __init__(self) -> None:
        pass
    def connect():
        try:
            mongo_db_password = os.environ.get('MONGO_DB_PASSWORD')
            mongo_db_username=os.environ.get('USERNAME')
            uri =f"mongodb+srv://{mongo_db_username}:{mongo_db_password}@cluster0.gqhkq1b.mongodb.net/"
            # Create a new client and connect to the server
            client = MongoClient(uri, server_api=ServerApi('1'))
            db = client.admin
            print(db)

        except Exception as e:
            print(f"Error: {e}")