import datetime
import json

from app.db.crud import add_location
from app.db.engine import Session
from app.queue import RabbitMQConnection
from app.schemas import LocationMessage
from pika.channel import Channel
from pika.spec import Basic, BasicProperties


def main():
    connection = RabbitMQConnection()

    def callback(ch: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
        print(" [x] Received %r" % body)
        try:
            msg = LocationMessage.parse_obj(json.loads(body))
        except Exception:
            print(" Message contains invalid data. Rejecting...")
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

        try:
            session = Session()
            add_location(
                session,
                user_id=msg.user_id,
                latitude=msg.latitude,
                longitude=msg.longitude,
                date_time=datetime.datetime.fromtimestamp(msg.timestamp),
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(" [x] Done")
        except Exception:
            print(" Error while inserting location data. Message will be requeued")
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)

    connection.start_consuming(callback)


if __name__ == "__main__":
    main()
