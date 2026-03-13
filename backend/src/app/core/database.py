import motor.motor_asyncio
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "deal_viewer")

client: motor.motor_asyncio.AsyncIOMotorClient = None
db: motor.motor_asyncio.AsyncIOMotorDatabase = None

async def connect_db():
    global client, db
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    try:
        await client.admin.command("ping")
        print(f"Connected to MongoDB : {MONGO_URI} / {DB_NAME}")
    except ConnectionFailure:
        print("Failure to connect to MongoDB")
        raise

async def disconnect_db():
    global client
    if client:
        client.close()
        print("Disconnnected from MongoDB")

def get_db():
    return db