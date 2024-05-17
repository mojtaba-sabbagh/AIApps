import os
from pymongo import MongoClient

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

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
