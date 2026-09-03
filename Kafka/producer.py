import csv
import json
import logging
import time
from confluent_kafka import Producer
from pathlib import Path
from confluent_kafka.admin import AdminClient, NewTopic
import Logging

bootstrap_servers = 'localhost:9092'
conf = {
    'bootstrap.servers': bootstrap_servers
}
producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        logging.warning(f'Message delivery failed: {err}')
        print(f'Message delivery failed: {err}')
    else:
        logging.info(f'Message delivered to {msg.topic()}')
        print(f'Message delivered to {msg.topic()}')

def produce_csv_to_kafka(csv_file_path, topic_name):
    count = 0
    logging.info("open file")
    with open(csv_file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for line in reader:
            value = json.dumps(line)

            producer.produce(
                topic_name,
                value=value.encode("utf-8"),
                callback=delivery_report
            )
            producer.poll(0)
            count += 1
            logging.info("Sent to Topic")
        producer.flush()
        logging.info("Sending completed")
    print(f"{count}")

def main():
    topic_name = "raw-topic"
    parent_dir = Path.cwd().parent
    file_name = "developer_ai_learning_raw.csv"
    csv_file_path = parent_dir / "Data" / file_name
    produce_csv_to_kafka(csv_file_path, topic_name)

if __name__ == "__main__":
    main()
