from kafka import KafkaProducer
import json
import random
import time
import datetime


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],  
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  
)


def generate_groundwater_data():
    return {
        "Temperature_C": round(random.uniform(-5, 35), 2),
        "Rainfall_mm": round(random.uniform(0, 200), 2),
        "Dissolved_Oxygen_mg_L": round(random.uniform(5, 12), 2),
        "timestamp": datetime.datetime.now().isoformat()  
    }


topic_name = 'groundwater-data'


while True:
    data = generate_groundwater_data()
    print(f"Sending data: {data}")
    producer.send(topic_name, value=data)  
    time.sleep(5)  
