from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URL)
db = client["travelBusDB"]

users_collection = db["users"]
buses_collection = db["buses"]
bookings_collection = db["bookings"]
seats_collection = db["seats"]