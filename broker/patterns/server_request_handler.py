class ServerRequestHandler:
    """
    Conecta as rotas FastAPI ao Invoker.
    """

    def __init__(self,invoker):
        self.invoker = invoker

    
    #========= PUBLIC METHODS USADOS PELA API 

    def handle_publish(self,dto):
        """
       Contém topic, payload, priority,ttl 
        """

        operation = "publish"
        params = {
            "topic":dto.topic, 
            "payload":dto.payload,
            "priority":dto.priority,
            "ttl":dto.ttl
        }
        return self.invoker.invoke(operation,params)
    
    def handle_subscribe(self,dto):
        """
        Contendo subscriber_id e topic
        """
        operation = "subscribe"
        params = {
            "subscriber_id":dto.subscriber_id,
            "topic": dto.topic
        }

        return self.invoker.invoke(operation,params) 
    
    def handle_metrics(self):
        """
        Retorna métricas internas do broker
        """

        operation = "metrics",
        params = {}
        return self.invoker.invole(operation,params)
