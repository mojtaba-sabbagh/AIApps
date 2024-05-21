import os
from pymongo import MongoClient

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

MONGOUSERNAME = os.getenv("MONGOUSERNAME")
MONGOPASSWORD = os.getenv("MONGOPASSWORD")
MONGOHOST = os.getenv("MONGOHOST")
MONGODBNAME = os.getenv("MONGODBNAME")

try:
    uri = f"mongodb+srv://{MONGOUSERNAME}:{MONGOPASSWORD}@{MONGOHOST}/" #{DBNAME}?connectTimeoutMS=300000&retryWrites=true&w=majority
    client = MongoClient(uri)

    database = client[MONGODBNAME]

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)
