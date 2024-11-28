# 이 Python 코드는 Kafka consumer 역할을 합니다. 즉, topic1에서 메시지를 소비하는 역할을 합니다.

from kafka import KafkaConsumer
from json import loads
import sys
# KafkaConsumer 인스턴스 생성
consumer = KafkaConsumer(
    'topic1',  # 메시지를 소비할 토픽명
    bootstrap_servers=['localhost:9092'],  # Kafka 브로커 주소
    auto_offset_reset='earliest',  # 가장 처음 메시지부터 소비
    enable_auto_commit=True,  # 오프셋을 자동으로 커밋
    group_id='test-group',  # 컨슈머 그룹 식별자
    value_deserializer=lambda x: loads(x.decode('utf-8')),  # 메시지 값 역직렬화 (JSON 파싱)
    consumer_timeout_ms=5000  # 5초간 메시지를 기다린 후 메시지없으면 종료
)

print('[Start] get consumer')

# 메시지를 계속 소비하며 출력
for message in consumer:
    print(f'Topic : {message.topic}, Partition : {message.partition}, Offset : {message.offset}, Key : {message.key}, value : {message.value}')

print('[End] get consumer')
sys.stdout.flush()  # 출력이 즉시 표준 출력에 반영되도록


# KafkaConsumer는 Kafka 브로커에서 메시지를 읽어오는 역할을 합니다.
# 'topic1'에서 메시지를 소비하며, 메시지의 오프셋을 earliest로 설정하여 처음부터 읽기 시작합니다.
# 메시지를 읽을 때마다, value_deserializer를 사용하여 JSON 형식의 메시지를 파싱합니다.
# consumer_timeout_ms=1000 설정은 1초 동안 메시지가 없으면 소비를 종료하도록 합니다.