from broker.core.broker_service import BrokerService
from broker.models.message import Message
from broker.models.events import Event 

class Invoker : 

    """
    Camada do Remoting Pattern responsável por: 

    - Receber uma operação do SRH 
    - Montar objetos de domínio (Message,Event) 
    - Invocar métodos reais no BrokerService 
    """

    def __init__(self,broker_service:BrokerService):
        self.broker_service = broker_service

    
    def invoke(self,operation:str,params:dict):
        """
        Recebe operação + parametros vindo do SRH decidindo qual método do BrokerService chamar 
        """

        if operation == "publish":
            return self._invoke_publish(params)
        
        elif operation == "subscribe":
            return self._invoke_subscribe(params) 
        
        elif operation =="metrics":
            return self.broker_service.get_metrics()
        
        else:
            raise ValueError(f"Operação desconhecida:{operation}")
        
    def _invoke_publish(self,params):
            """
            Converte o DTO em Message -> Event e envia ao broker. 
            """

            #Criar a Message com dados crus do sensor 

            msg = Message(
                 humidity = params["payload"]["humidity"],
                 temperature = params["payload"]["temperature"],
                 valve=params["payload"]["valve"],
            )

            # Cria o evento interno 

            event = Event(
                 message=msg,
                 topic=params["topic"],
                 priority=params["priority"],
                 ttl=params["ttl"],
            )

            #Publicar no broker 

            self.broker_service.publish(event)

            return {"status":"ok","event_id":event.event_id} 
    
    def _invoke_subscribe(self, params):
        """
        Faz o subscriber entrar no tópico.
        params: {subscriber_id, topic}
        """
        self.broker_service.subscribe(
            subscriber_id=params["subscriber_id"],
            topic=params["topic"]
        )

        return {"status": "subscribed", "topic": params["topic"]}