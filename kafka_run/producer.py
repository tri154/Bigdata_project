import numpy as np
from kafka import KafkaProducer
import json
import time
# Initialize Kafka producer (adjust the bootstrap_servers and topic as needed)
producer = KafkaProducer(
    bootstrap_servers='localhost:9094',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

results = []
import datetime

with open('track_2.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line == '':
            # Send to Kafka when a blank line is encountered
            if results:
                data_array = np.array(results)
                # Convert array to list before sending to Kafka
                producer.send('tracking', data_array.tolist())
                results = []  # Reset for the next block
                time.sleep(0.5)
                print("Sent")
        else:
            results.append(line)

# Optionally send remaining results if file doesn't end with a blank line
if results:
    data_array = np.array(results)
    producer.send('tracking', data_array.tolist())
producer.send('tracking', "Done")
producer.flush()
producer.close()
