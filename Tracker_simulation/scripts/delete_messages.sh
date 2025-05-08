#!/bin/bash
kafka-server-start.sh "$KAFKA_HOME/config/server.properties" > kafka.log 2>&1 &
sleep 5
kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic tracking
echo "Deleted topic, try recreate."
bash create_topic.sh