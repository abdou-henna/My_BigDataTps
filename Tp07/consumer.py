from kafka import KafkaConsumer

consumer = KafkaConsumer('test-topic', bootstrap_servers='localhost:9092')
for msg in consumer:
    print(f"Received: {msg.value.decode('utf-8')}")
