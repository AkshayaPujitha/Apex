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
            url=os.environ('URL')
            # Create a new client and connect to the server
            client = MongoClient(url, server_api=ServerApi('1'))
            db = client.admin
            print(db)

        except Exception as e:
            print(f"Error: {e}")