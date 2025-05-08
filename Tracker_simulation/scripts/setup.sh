#!/bin/bash
cd ~
wget https://dlcdn.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz
tar -xzf kafka_2.13-4.0.0.tgz
mv kafka_2.13-4.0.0 kafka

cd kafka/bin
echo "export PATH=\$PATH:$(pwd)" >> ~/.bashrc
echo "export KAFKA_HOME=$(dirname $(pwd))" >> ~/.bashrc
source ~/.bashrc

