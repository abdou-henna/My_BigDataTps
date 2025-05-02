from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')
for i in range(10):
    message = f"Message {i}"
    if i == 7:
         message = f"hello world {i}" 
   
    producer.send('test-topic', message.encode('utf-8'))
    print(f"Sent: {message}")
    time.sleep(1)

producer.flush()
