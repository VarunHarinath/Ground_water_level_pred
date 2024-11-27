from kafka import KafkaConsumer
import json
from pymongo import MongoClient
from mongo_model import MongoDB, GroundWaterModel


mongo_client = MongoDB(uri="mongodb://localhost:27017", db_name="groundwater_db")
groundwater_model = GroundWaterModel(db=mongo_client)

# Kafka Consumer setup
consumer = KafkaConsumer(
    'groundwater-data',  
    bootstrap_servers=['localhost:9092'],
    group_id='groundwater-consumer-group',  
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  
)


def process_and_store_data(data):
    try:
        # Insert data into MongoDB
        inserted_id = groundwater_model.insert_data(data)
        print(f"Data inserted with ID: {inserted_id}")
    except Exception as e:
        print(f"Error processing data: {e}")


print("Listening for new data on 'groundwater-data' topic...")
for message in consumer:
    data = message.value 
    print(f"Received data: {data}")
    process_and_store_data(data)
