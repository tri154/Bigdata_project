from kafka import KafkaConsumer
import json
import numpy as np

# Create Kafka consumer
consumer = KafkaConsumer(
    'tracking',
    bootstrap_servers='localhost:9092',
    group_id='visualization',  # Set a group ID
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',  # Read from the beginning if no offset is committed
    enable_auto_commit=True
)

print("Listening for messages on topic 'tracking'...")

# Poll and print incoming messages
for message in consumer:
    data_list = message.value
    data_array = np.array(data_list)  # Convert to NumPy array
