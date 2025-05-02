from kafka import KafkaProducer
import time, random, json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for i in range(20):
    data = {
        "sensor_id": f"S-{random.randint(1000,9999)}",
        "temp": round(random.uniform(25.0, 90.0), 2),
        "status": random.choice(["OK", "FAIL"]),
        "timestamp": time.time()
    }
    producer.send("iot-data", value=data)
    print("Sent:", data)
    time.sleep(1)

producer.flush()
    