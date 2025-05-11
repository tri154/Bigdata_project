from kafka import KafkaConsumer
import json
import numpy as np
import cv2
from draw import draw_image
from elasticsearch import Elasticsearch, helpers
import time

index_name = "tracking_data"

def main():
    # Create Kafka consumer
    consumer = KafkaConsumer(
        'tracking',
        bootstrap_servers='localhost:9094',
        group_id='visualization',  # Set a group ID
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',  # Read from the beginning if no offset is committed
        enable_auto_commit=True
    )

    client = Elasticsearch(
        "https://my-elasticsearch-project-dabe03.es.ap-southeast-1.aws.elastic.cloud:443",
        api_key="VFZpdnM1WUJ3Y3A0cmZvQUJPeEU6NXhvZ0ZZa095LWp2QzRmNnM5YmxtZw=="
    )

    print("Listening for messages on topic 'tracking'...")

    for message in consumer:
        data_list = message.value
        if data_list == 'Done':
            break
        data_array = []
        for data in data_list:
            data_array.append([int(float(x)) for x in data[:7]] + [float(x) for x in data[7:9]] + [data[9]])
        data_array = np.array(data_array, dtype=object)
        print(data_array.shape)
        frame = draw_image(data_array)
        cv2.imwrite('last_img.jpg', frame)
        time.sleep(0.1)
        arr = []
        for parts in data_array:
            arr.append({
                "_index": index_name,
                "_source": {
                    "camera_id": parts[0],
                    "obj_id": parts[1],
                    "frame_id": parts[2],
                    "xmin": parts[3],
                    "ymin": parts[4],
                    "width": parts[5],
                    "height": parts[6],
                    "xworld": parts[7],
                    "yworld": parts[8],
                    "timestamp": parts[9] # Proper datetime string
                }
            })
        bulk_response = helpers.bulk(client, arr)
        print("Bulk upload response:", bulk_response)


if __name__ == "__main__":
    main()
    # consumer = KafkaConsumer(
    #     'tracking',
    #     bootstrap_servers='localhost:9094',
    #     group_id='visualization',  # Set a group ID
    #     value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    #     auto_offset_reset='earliest',  # Read from the beginning if no offset is committed
    #     enable_auto_commit=True
    # )
    # for message in consumer:
    #     print(message.value)