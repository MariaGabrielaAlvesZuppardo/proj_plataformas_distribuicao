# client/client_proxy.py

class ClientProxy:
    """
    Interface usada pelo sensor ESP32 ou simulador.
    """

    def __init__(self, requestor):
        self.requestor = requestor

    def publish(self, humidity: float, temperature: float, valve: bool,
                topic: str = "solo.mandioca",
                priority: int = 5,
                ttl: float = 30.0):
        """
        Envia uma leitura de umidade/temperatura para o broker.
        """

        payload = {
            "humidity": humidity,
            "temperature": temperature,
            "valve": valve
        }

        return self.requestor.send_publish_request(
            topic=topic,
            payload=payload,
            priority=priority,
            ttl=ttl
        )

    def subscribe(self, subscriber_id: str, topic: str):
        return self.requestor.send_subscribe_request(subscriber_id, topic)

    def get_metrics(self):
        return self.requestor.send_metrics_request()
