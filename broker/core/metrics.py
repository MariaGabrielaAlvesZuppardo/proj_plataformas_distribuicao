from threading import Lock 
from typing import Dict 

class BrokerMetrics:
    """
    Coletor de métricas internas do broker. 
    """

    def __init__(self):
        self._lock = Lock()
        self._metrics = {
            "messages_received": 0,
            "messages_delivered": 0,
            "messages_expired": 0,
            "messages_in_queue": 0,
        }
    def inc (self,key: str,value: int =1):
        with self._lock:
            if key not in self._metrics:
                raise KeyError(f"Métrica inexistente:{key}")
            self._metrics[key] += value
    
    def set(self,key:str,value:int):
        with self._lock:
            self._metrics[key] = value
    
    def get(self,key:str) -> int: 
        with self._lock:
            return self._metrics.get(key,0)
    
    def dump(self) -> Dict[str, int]:
        """Retorna snapshot completo das métricas."""
        with self._lock:
            return dict(self._metrics)