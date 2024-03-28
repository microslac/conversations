import json
import pika

from micro.events.publishers import Publisher


class P(Publisher):
    def publish(
            self,
            data: dict,
            routing_key: str,
            mandatory: bool = False,
            **kwargs,
    ) -> None:
        if not self.is_enabled():
            return

        while True:
            try:
                data = data or {}
                body = json.dumps(data).encode("utf-8")
                properties = pika.BasicProperties(content_encoding="utf-8", content_type="application/json", **kwargs)
                self.channel.basic_publish(
                    body=body,
                    exchange=self.exchange,
                    routing_key=routing_key,
                    properties=properties,
                    mandatory=mandatory,
                )
                break
            except pika.exceptions.ConnectionClosedByBroker:
                break
            except pika.exceptions.AMQPChannelError:
                break
            except pika.exceptions.AMQPConnectionError:
                self.setup_connection()  # Recover connection
                continue


communication = P("communication")
