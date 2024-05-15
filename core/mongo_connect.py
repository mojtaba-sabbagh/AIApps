import os
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
DBNAME = os.getenv("DBNAME")

try:
    uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@{HOST}/" #{DBNAME}?connectTimeoutMS=300000&retryWrites=true&w=majority
    client = MongoClient(uri)

    database = client[DBNAME]

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)
