import logging
import os
import json
from confluent_kafka import Consumer, Producer
from Cleaning_and_conversions import process_record
import Logging


bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
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
    logging.info("Starting the processing")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                logging.warning("The message is None")
                continue
            if msg.error():
                logging.error(f"Consumer error: {msg.error()}")
                print(f"Consumer error: {msg.error()}")
                continue

            raw_value = msg.value().decode('utf-8')
            raw_record = json.loads(raw_value)

            processed_record = process_record(raw_record)

            logging.info("Defines a topic")
            producer.produce(
                output_topic,
                value=json.dumps(processed_record).encode("utf-8")
            )
            producer.poll(0)
            message_count += 1
            logging.info(f"Processed and sent message number: {message_count}")
            print(f"Processed and sent message number: {message_count}")

    except KeyboardInterrupt:
        logging.error("Stopping processor")
        print("Stopping processor")
    finally:
        logging.info("Consumer closure")
        consumer.close()
        producer.flush()

if __name__ == "__main__":
    start_processing()