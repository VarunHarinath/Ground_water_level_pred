from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
import os
import json

class MongoDB:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "groundwater_db"):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            print(f"Connected to MongoDB at {uri}, Database: {db_name}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def get_collection(self, collection_name: str):
        return self.db[collection_name]
    
    def close(self):
        """Close MongoDB client connection."""
        self.client.close()

class GroundWaterModel:
    def __init__(self, db: MongoDB):
        self.db = db
        self.collection = self.db.get_collection("ground_water_data")  
        self.create_indexes()

    def create_indexes(self):
        """Create necessary indexes to optimize queries."""
        self.collection.create_index([("Temperature_C", ASCENDING)])
        self.collection.create_index([("Rainfall_mm", ASCENDING)])
       

    def insert_data(self, data: dict):
        """Insert data into the MongoDB collection"""
        try:
            result = self.collection.insert_one(data)
            return str(result.inserted_id)  
        except Exception as e:
            print(f"Error inserting data: {e}")
            raise

    def get_data(self, query: dict = None, skip: int = 0, limit: int = 100):
        """Retrieve data from MongoDB collection based on query, with pagination"""
        query = query or {}
        try:
            return list(self.collection.find(query).skip(skip).limit(limit))  
        except Exception as e:
            print(f"Error retrieving data: {e}")
            raise

    def get_data_by_id(self, data_id: str):
        """Retrieve a single document by its ObjectId"""
        try:
            return self.collection.find_one({"_id": ObjectId(data_id)})
        except Exception as e:
            print(f"Error fetching data by ID: {e}")
            raise

    def update_data(self, data_id: str, updated_data: dict):
        """Update data in MongoDB by ID"""
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(data_id)},
                {"$set": updated_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating data: {e}")
            raise

    def delete_data(self, data_id: str):
        """Delete a document by its ObjectId"""
        try:
            result = self.collection.delete_one({"_id": ObjectId(data_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting data: {e}")
            raise
