import producer
import Processor_Service
import tiבme

def main():
    producer.main()
    Processor_Service.start_processing()

if __name__ == "__main__":
    main()