from typing import Optional

from broker.models.message import Message
from broker.core.events_repository import EventsRepository
from broker.core.subscription_manager import SubscriptionManager
from broker.core.metrics import BrokerMetrics

class BrokerService:
    """
    Fachada principal do Broker 
    Usada pelo Invoker via remotting pattern
    """

    def __init__(
            self,
            events_repo: EventsRepository,
            subs_manager: SubscriptionManager,
            metrics: BrokerMetrics
    ):
        self._repo = events_repo
        self._subs = subs_manager
        self._metrics = metrics
    
    #-----------------------------------------------------

    def publish(self,message:Message) -> bool:
        """Publica mensagem no tópico"""
        self._repo.enqueue(message)
        self._metrics.inc("messages_received")
        self._metrics.set("messages_in_queue",self._repo.count(message.topic))
        return True

    #----------------------------------------------------

    def get_next_message(self,topic:str)->Optional[Message]:
        """Retorna próxima mensagem (para entrega pelo worker)"""  
        msg = self._repo.dequeue(topic)

        if msg:
            self._metrics.inc("messages_delivered")
            self._metrics.set("messages_in_queue",self._repo.count(topic))

        return msg 

    #------------------------------------------------------

    def get_subscribers (self,topic:str):
        return self._subs.get_subscribers(topic)      
    
    # ----------------------------------------------------

    def subscribe(self,topic:str,url:str):
        return self._subs.get_subscribers(topic,url)
     # -------------------------------------------------------

    def remove_expired(self) -> int:
        removed = self._repo.remove_expired()
        if removed > 0:
            self._metrics.inc("messages_expired", removed)
        return removed

    # -------------------------------------------------------

    def dump_state(self):
        """Usado só para depuração."""
        return {
            "messages": self._repo.get_all_for_debug(),
            "subscribers": self._subs.dump(),
            "metrics": self._metrics.dump(),
        }