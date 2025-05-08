#!/bin/bash
#source ~/.bashrc
#cat ~/.bashrc | grep KAFKA_HOME
#echo $KAFKA_HOME
KAFKA_CLUSTER_ID="kLHeUqTfQMmlWEtzttOV7Q"
kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c "$KAFKA_HOME/config/server.properties"
kafka-server-start.sh "$KAFKA_HOME/config/server.properties" > kafka.log 2>&1 &
sleep 5
kafka-topics.sh --create --topic tracking --bootstrap-server localhost:9092
bash scripts/stop_kafka.sh
