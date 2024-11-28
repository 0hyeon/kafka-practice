#Kafka 토픽에 메시지를 보내는 역할

from kafka import KafkaProducer
from json import dumps
import time

# KafkaProducer 인스턴스 생성
producer = KafkaProducer(
    acks=0,  # 메시지 전송 후 Kafka로부터의 응답을 기다리지 않음
    compression_type='gzip',  # 메시지를 gzip으로 압축하여 전송
    bootstrap_servers=['localhost:9092'],  # Kafka 브로커 주소
    value_serializer=lambda x: dumps(x).encode('utf-8')  # 메시지 값을 직렬화 (JSON으로 변환 후 UTF-8 인코딩)
)

start = time.time()  # 시작 시간 기록

# 1000개의 메시지를 보내기
for i in range(10000):
    data = {'str': 'result' + str(i)}  # 전송할 메시지 생성
    producer.send('topic1', value=data)  # 'topic1'에 메시지 전송
    producer.flush()  # 메시지가 전송될 때까지 기다림 # 전송을 완료하기 위해 호출

print('[Done]:', time.time() - start)  # 실행 시간 출력

# 주요 기능:
# KafkaProducer는 Kafka 브로커에 메시지를 보내는 역할을 합니다.
# 메시지는 JSON 형식으로 직렬화되어 UTF-8로 인코딩되고, topic1이라는 Kafka 토픽에 1000개의 메시지가 보내집니다.
# flush() 메서드는 메시지가 브로커에 전송될 때까지 기다립니다.
# acks=0 설정은 메시지가 브로커에 도달한 후 응답을 기다리지 않도록 설정합니다.
# 메시지는 gzip 형식으로 압축되어 전송됩니다.

# 이 결과는 메시지를 보내는 데 걸린 시간입니다. 1000개의 메시지를 보내는 데 약 0.56초가 걸렸다는 것을 나타냅니다.