from elasticsearch import Elasticsearch, helpers
import datetime
import time
import numpy as np

EPOCH_START = datetime.datetime.now(datetime.UTC)

def frame_id_to_timestamp(frame_id, fps=10):
    return (EPOCH_START + datetime.timedelta(seconds=frame_id / fps)).isoformat()
# Initialize the Elasticsearch client
client = Elasticsearch(
    "https://my-elasticsearch-project-dabe03.es.ap-southeast-1.aws.elastic.cloud:443",
    api_key="VFZpdnM1WUJ3Y3A0cmZvQUJPeEU6NXhvZ0ZZa095LWp2QzRmNnM5YmxtZw=="
)


index_name = "tracking_data"

# Parse the file into Elasticsearch-friendly dicts
def parse_tracking_file(file_path):
    arr = []
    with open(file_path, "r") as file:
        for line in file:
            parts = np.fromstring(line.strip(), sep=' ')
            if len(parts) != 9:
                bulk_response = helpers.bulk(client, arr)
                print("Bulk upload response:", bulk_response)
                arr = []
                continue
                # Skip malformed lines
            timestampe = frame_id_to_timestamp(int(parts[2]))
            print(timestampe)
            arr.append({
                "_index": index_name,
                "_source": {
                    "camera_id": int(parts[0]),
                    "obj_id": int(parts[1]),
                    "frame_id": int(parts[2]),
                    "xmin": int(parts[3]),
                    "ymin": int(parts[4]),
                    "width": int(parts[5]),
                    "height": int(parts[6]),
                    "xworld": float(parts[7]),
                    "yworld": float(parts[8]),
                    "timestamp": timestampe # Proper datetime string
                }
            })


parse_tracking_file("track__.txt")


