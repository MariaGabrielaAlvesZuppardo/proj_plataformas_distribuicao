import asyncio

class TTLChecker: 
    """
    Worker responsável por limpar mensagens expiradas no EventsRepository
    """

    def __init__(self,broker_service,interval:float = 1.0):
        self.broker_service = broker_service
        self.interval = interval
        self.running = True

    
    async def run (self):
        print("[TTLChecker] Worker inciado")

        while self.running:
            removed = self.broker_service.remove_expired()

            #Atualizar métricas internas 
            if removed > 0:
                self.broker_service.metrics.ttl_removed += removed 

            await asyncio.sleep(self.interval)