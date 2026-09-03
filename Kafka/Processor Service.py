import os
import json
from confluent_kafka import Consumer, Producer
from Cleaning_and_conversions import process_record


bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
input_topic = os.getenv('INPUT_TOPIC', 'raw-topic')
output_topic = os.getenv('OUTPUT_TOPIC', 'processed-topic')
group_id = "processor-group-v2"

consumer_conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': group_id,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
}
consumer = Consumer(consumer_conf)
consumer.subscribe([input_topic])

producer_conf = {'bootstrap.servers': bootstrap_servers}
producer = Producer(producer_conf)


def start_processing():
    message_count = 0
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            raw_value = msg.value().decode('utf-8')
            raw_record = json.loads(raw_value)

            processed_record = process_record(raw_record)

            producer.produce(
                output_topic,
                value=json.dumps(processed_record).encode("utf-8")
            )
            producer.poll(0)
            message_count += 1
            print(f"Processed and sent message number: {message_count}")

    except KeyboardInterrupt:
        print("Stopping processor")
    finally:
        consumer.close()
        producer.flush()

if __name__ == "__main__":
    start_processing()