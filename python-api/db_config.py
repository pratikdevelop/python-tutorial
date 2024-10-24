from pymongo import MongoClient

def get_db():
    client = MongoClient('mongodb://localhost:27017/password-manager')  # Change to your MongoDB URI
    db = client['password-manager']  # Replace with your database name
    return db
