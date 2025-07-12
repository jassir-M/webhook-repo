from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB using MONGO_URI from .env or fallback to localhost
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/webhookDB")
client = MongoClient(MONGO_URI)
db = client.webhookDB
events_collection = db.events

def save_event(event_type, author, from_branch, to_branch, timestamp):
    events_collection.insert_one({
        "event_type": event_type,
        "author": author,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": timestamp
    })

def get_latest_events(limit=10):
    events = list(events_collection.find().sort("timestamp", -1).limit(limit))
    # Convert _id ObjectId to string for JSON serialization
    for event in events:
        event["_id"] = str(event["_id"])
    return events
