
import asyncio

class NotificationEngine:
    """
    Worker responsável por retirar mensagens da fila 
    e entregar para todos os subscribers do tópico.
    """

    def __init__(self, broker_service, interval: float = 0.5):
        self.broker_service = broker_service
        self.interval = interval
        self.running = True

    async def run(self):
        print("[NotificationEngine] Worker iniciado.")

        while self.running:
            # Pega o próximo evento da fila
            event = self.broker_service.dequeue_event()

            if event:
                topic = event.topic
                subscribers = self.broker_service.get_subscribers(topic)

                for sub in subscribers:
                    # Entrega a mensagem ao subscriber
                    sub.receive(event.payload)

                    # Atualiza métricas
                    self.broker_service.metrics.messages_delivered += 1

            await asyncio.sleep(self.interval)
