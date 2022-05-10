import json
from abc import ABC, abstractmethod
from typing import Dict

import pika
from app.config import settings
from pika.spec import PERSISTENT_DELIVERY_MODE


class QueueService(ABC):
    @abstractmethod
    def send_message(content: Dict) -> None:
        """Send a message to the queue

        Args:
            content (Dict): Body of the message
        """
        raise NotImplementedError()


class RabbitQueueService(QueueService):
    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.rabbit_host,
                port=settings.rabbit_port,
                credentials=pika.PlainCredentials(
                    username=settings.rabbit_username, password=settings.rabbit_password
                ),
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=settings.rabbit_queue, durable=True)

    def send_message(self, content: Dict) -> None:
        """Send a message to the queue

        Args:
            content (Dict): Body of the message
        """
        self.channel.basic_publish(
            exchange="",
            routing_key=settings.rabbit_queue,
            body=json.dumps(content),
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=PERSISTENT_DELIVERY_MODE,
            ),
        )
