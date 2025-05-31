from kafka import KafkaConsumer
import json
import numpy as np
import cv2
from draw import draw_image
from elasticsearch import Elasticsearch, helpers
import time
import argparse

index_name = "tracking_data"

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("--topic", type=str, help="Kafka topic", default='tracking')
    parse.add_argument("--not_use_elastic", action="store_true", default=False)
    parse.add_argument("--elastic_host", type=str, default="")
    parse.add_argument("--elastic_api_key", type=str, default="")


    args = parse.parse_args()
    is_elastic = not args.not_use_elastic
    # Create Kafka consumer
    consumer = KafkaConsumer(
        'tracking',
        bootstrap_servers='localhost:9094',
        group_id='visualization',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    if is_elastic:
        client = Elasticsearch(args.elastic_host,api_key=args.elastic_api_key)

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
        if is_elastic:
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
