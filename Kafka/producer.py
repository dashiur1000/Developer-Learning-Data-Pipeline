import csv
import json
import time
from confluent_kafka import Producer
from pathlib import Path
from confluent_kafka.admin import AdminClient, NewTopic



def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()}')

def produce_csv_to_kafka(csv_file_path, topic_name):
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
        producer.flush()

def ensure_topic_exists(bootstrap_servers, topic_name):
    admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})
    metadata = admin_client.list_topics(timeout=5)

    if topic_name not in metadata.topics:
        new_topic = NewTopic(topic=topic_name, num_partitions=1, replication_factor=1)
        fs = admin_client.create_topics([new_topic])
        for topic, future in fs.items():
            try:
                future.result()
                print(f"Topic '{topic}' created successfully.")
            except Exception as e:
                print(f"Failed to create topic '{topic}': {e}")
    else:
        print(f"Topic '{topic_name}' already exists.")



if __name__ == "__main__":
    bootstrap_servers = 'localhost:9092'
    conf = {
        'bootstrap.servers': bootstrap_servers
    }

    producer = Producer(conf)
    topic_name = "raw-topic"
    # ensure_topic_exists(bootstrap_servers, topic_name)
    parent_dir = Path.cwd().parent
    file_name = "developer_ai_learning_raw.csv"
    csv_file_path = parent_dir / "Data" / file_name
    produce_csv_to_kafka(csv_file_path, topic_name)