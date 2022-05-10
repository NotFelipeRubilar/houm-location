import pika
from app.config import settings


class RabbitMQConnection:
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

    def start_consuming(self, callback) -> None:
        try:
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(queue=settings.rabbit_queue, on_message_callback=callback)
            print(" [*] Waiting for messages. To exit press CTRL+C")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("Interrupted")
            self.channel.stop_consuming()
