from dataclasses import dataclass,field
import time
import uuid

@dataclass(order=True)
class Event:
    #order = True permite o heapq ordenar por prioridade e timestamp 

    sort_index: tuple = field(init=False,repr=False)

    priority: int 
    ttl:float 
    message:object
    topic:str 
    created_at:float = field(default_factory=time.time)
    event_id: str = field(default_factory=lambda:str(uuid.uuid4()))

    def __post_init__(self):
        self.expires_at = self.created_at + self.ttl
        self.sort_index = (self.priority,self.created_at) 
        
        #prioridade menor = mais urgente 
    
    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    
