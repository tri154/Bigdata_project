#!/bin/bash
kafka-server-start.sh "$KAFKA_HOME/config/server.properties" > kafka.log 2>&1