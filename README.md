# Kafka Producer and Consumer Pratice

이 프로젝트는 Kafka를 사용하여 메시지 생산자(Producer)와 소비자(Consumer) 프로세스를 구현한 예제입니다. 아래에서 각 파일과 출력 내용에 대해 설명하겠습니다.

## 1. Docker Compose 실행

Kafka와 Zookeeper를 실행하기 위해 `docker-compose` 명령어를 사용합니다.

### 실행 명령어

```bash
docker-compose up -d
```

이 명령어는 Docker Compose 파일을 기반으로 Kafka와 Zookeeper를 백그라운드에서 실행합니다.

## 2. Docker 컨테이너 목록 조회

실행 중인 모든 Docker 컨테이너를 조회하려면 아래 명령어를 사용합니다.

```bash
docker ps -a
```

## 3. Producer (producer.py)

이 Python 코드는 Kafka producer 역할을 하며, topic1이라는 Kafka 토픽에 메시지를 전송합니다.

```python

from kafka import KafkaProducer
from json import dumps
import time

# KafkaProducer 인스턴스 생성
producer = KafkaProducer(
    acks=0,  # 메시지 전송 후 Kafka로부터의 응답을 안기다림
    compression_type='gzip',  # 메시지 gzip으로 압축하여 전송
    bootstrap_servers=['localhost:9092'],  # Kafka 브로커 주소
    value_serializer=lambda x: dumps(x).encode('utf-8')
    # 메시지 값 직렬화 (JSON으로 변환 후 UTF-8 인코딩)
)

start = time.time()  # 시작 시간 기록

# 1000개의 메시지를 보내기
for i in range(1000):
    data = {'str': 'result' + str(i)}  # 전송할 메시지 생성
    producer.send('topic1', value=data)  # 'topic1'에 메시지 전송
    producer.flush()  # 메시지가 전송될 때까지 기다림

print('[Done]:', time.time() - start)  # 실행 시간 출력
```

`KafkaProducer는` Kafka 브로커에 메시지를 전송하는 역할을 합니다.<br/>
메시지는 JSON 형식으로 직렬화되어 UTF-8로 인코딩되고, topic1이라는 Kafka 토픽에 1000개의 메시지가 전송됩니다.

`flush() 메서드`는 메시지가 브로커에 전송될 때까지 기다립니다.<br/>

acks=0 설정은 메시지가 브로커에 도달한 후 응답을 기다리지 않도록 설정합니다.
메시지는 gzip 형식으로 압축되어 전송됩니다.

```bash
[Done]: 0.5606689453125
```

- 1000개의 메시지를 보내는 데 약 0.56초가 걸린 것을 나타냅니다.

## 4. Consumer (consumer.py)

이 Python 코드는 Kafka consumer 역할을 하며, topic1에서 메시지를 소비합니다.

```python
from kafka import KafkaConsumer
from json import loads

# KafkaConsumer 인스턴스 생성
consumer = KafkaConsumer(
    'topic1',  # 메시지를 소비할 토픽명
    bootstrap_servers=['localhost:9092'],  # Kafka 브로커 주소
    auto_offset_reset='earliest',  # 가장 처음 메시지부터 소비
    enable_auto_commit=True,  # 오프셋을 자동으로 커밋
    group_id='test-group',  # 컨슈머 그룹 식별자
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    # 메시지 값 역직렬화 (JSON 파싱)
    consumer_timeout_ms=1000  # 1초간 메시지를 기다린 후 종료
)

print('[Start] get consumer')

# 메시지를 계속 소비하며 출력
for message in consumer:
    print(f'Topic : {message.topic}, Partition : {message.partition}, Offset : {message.offset}, Key : {message.key}, value : {message.value}')

print('[End] get consumer')
```

- `KafkaConsumer는` Kafka 브로커에서 메시지를 읽어오는 역할을 합니다.</br>
  </br>

`topic1에서 메시지를 소비`하며, 메시지의 오프셋을 earliest로 설정하여 처음부터 읽기 시작합니다.</br>

value_deserializer를 사용하여 JSON 형식의 메시지를 파싱합니다.</br>

`consumer_timeout_ms=1000 설정은` 1초 동안 메시지가 없으면 소비를 종료하도록 합니다.</br>

```bash
[Start] get consumer
[End] get consumer
```

consumer_timeout_ms=1000에 의해 1초 동안 메시지가 없으면 소비자가 종료됩니다.<br/>

이 설정은 일정 시간 동안 메시지가 없으면 자동으로 종료되도록 하여, 소비자 프로세스가 무한 대기하지 않도록 합니다.

## 5. Docker 및 Kafka 관련 명령어

Kafka 관련 명령어는 Docker Compose를 통해 실행되고 있는 Kafka 인스턴스에서 Kafka 토픽을 관리하는 데 사용됩니다.

## 6. 토픽 리스트 확인

Kafka 브로커에서 현재 존재하는 모든 토픽을 확인하려면 아래 명령어를 사용합니다.

```bash
# docker-compose exec [Service Name] kafka-topics --list --bootstrap-server [Service Name]:[Port]
docker-compose exec broker kafka-topics --list --bootstrap-server broker:9092

```

- \_\_consumer_offsets은 컨슈머 그룹의 오프셋 정보를 저장하는 특별한 내부 토픽으로 각 컨슈머가 읽은 메시지의 오프셋을 추적하고 관리하는 역할을 합니다.

- topic1: 메시지를 보내고 받기 위한 Kafka 토픽
  \_\_consumer_offsets: Kafka가 소비한 메시지의 오프셋을 추적하는 내부 토픽

## 7. 토픽 세부 정보 확인

특정 토픽에 대한 세부 정보를 확인하려면 아래 명령어를 사용합니다.

```bash
# docker-compose exec [Service Name] kafka-topics --describe --topic [Topic Name] --bootstrap-server [Service Name]:[Port]
docker-compose exec broker kafka-topics --describe --topic topic1 --bootstrap-server broker:9092
```

```bash
Topic: topic1   TopicId: 9vr7CyLFRlOmWEGS7x90Aw PartitionCount: 1       ReplicationFactor: 1    Configs:
        Topic: topic1   Partition: 0    Leader: 1       Replicas: 1     Isr: 1
```

topic1은 1개의 파티션을 가지며, 파티션 0의 리더는 브로커 1입니다.
복제 수는 1로 설정되어 있어, 데이터 복제가 최소 1번으로 보장됩니다.

## 8. 결론

- producer.py는 Kafka 브로커에 1000개의 메시지를 전송합니다.
- consumer.py는 topic1에서 메시지를 소비하고 이를 출력합니다.
- Docker Compose를 통해 Kafka 인스턴스를 실행하고, Kafka 명령어를 통해 토픽을 관리할 수 있습니다.<br/>

- consumer.py가 바로 종료된 것은 consumer_timeout_ms 설정에 의한 것으로, 메시지가 없어 1초 후 자동으로 종료된 것으로 보입니다.
