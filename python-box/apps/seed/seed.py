import csv, json
from kafka import KafkaProducer

def create_dict(headers, row):
    obj = {}
    for i in range(len(headers)):
        obj[headers[i]] = row[i]
    return obj

def stream_csv_to_kafka(file_name: str) -> None:
    producer = KafkaProducer(bootstrap_servers='kafka-box:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    with open(file_name, 'r', 1) as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            obj = create_dict(headers, row)
            producer.send('transactions', value=obj)

if __name__ == '__main__':
    stream_csv_to_kafka('bs140513_032310_with_id.csv')