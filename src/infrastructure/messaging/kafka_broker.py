import json
import typing

from aiokafka import AIOKafkaProducer

from src.application.ports.message_broker import MessageBroker


class KafkaMessageBroker(MessageBroker):
    def __init__(self, producer: AIOKafkaProducer, topic: str) -> None:
        self._producer = producer
        self._topic = topic

    async def send(self, payload: dict[str, typing.Any]) -> None:
        headers = []
        inner_payload = payload.get("payload")
        if isinstance(inner_payload, dict):
            trace_id = inner_payload.get("trace_id")
            if trace_id:
                headers.append(("x-trace-id", trace_id.encode("utf-8")))
        await self._producer.send_and_wait(self._topic, payload, headers=headers)


def serialize(value: dict[str, typing.Any]) -> bytes:
    return json.dumps(value, ensure_ascii=False).encode("utf-8")
