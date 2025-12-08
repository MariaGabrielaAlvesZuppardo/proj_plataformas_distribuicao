from threading import Lock 
from typing import Dict,List

class SubscriptionManager:
    """
    Gerencia subscribers por tópico.
    Não envia HTTP, isso é trabalho do NotificationEngine 
    """

    def __init__(self):
        self._lock = Lock ()
        self._subscribers: Dict[str,List[str]] = {}

    def subscribe(self,topic:str,endpoint_url:str):
        with self._lock:
            if topic not in self._subscribers:
                self._subscribers[topic] = []
            if endpoint_url not in self._subscribers[topic]:
                self._subscribers[topic].append(endpoint_url)
    
    def unsubscribe(self,topic:str,endpoint_url:str):
        with self._lock:
            if topic in sel._subscribers:
                self._subscribers[topic]=[
                    x for x in self._subscribers[topic] if x != endpoint_url
                ]
    
    def get_subscribers(self,topic:str) -> List[str]:
        with self._lock:
            return list(self._subscribers.get(topic,[]))
    
    def dump(self):
        with self._lock:
            return dict(self._subscribers)