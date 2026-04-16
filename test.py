# Simplified connection using MONGODB_URI
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()
try:
    # mongodb_uri = os.getenv('MONGODB_URI')
    # mongodb_= os.getenv('MONGODB_URI')
    # db_name = os.getenv('MONGO_DB_NAME', 'TestDB')
    # collection_name = os.getenv('MONGO_COLLECTION_NAME', 'tutedude')
    password = os.getenv('MONGO_PASSWORD')
    print(password)

    mongodb_uri = f"mongodb+srv://ambardarviresh18:{os.getenv('MONGO_PASSWORD')}@tutedude.dw5lcw2.mongodb.net/"
    
    client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = "TestDB"
    collection = "Sample"
    print("Connected to MongoDB Atlas successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    collection = None