#!/usr/bin/env bash
#Note Please change the kafka topics path before running the script
/opt/homebrew/bin/kafka-topics --zookeeper localhost:2181 --delete --topic data

/opt/homebrew/bin/kafka-topics --zookeeper localhost:2181 --delete --topic status


/opt/homebrew/bin/kafka-topics --create --topic data --bootstrap-server localhost:9092

/opt/homebrew/bin/kafka-topics --create --topic status --bootstrap-server localhost:9092
