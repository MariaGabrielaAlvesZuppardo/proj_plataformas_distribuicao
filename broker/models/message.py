

import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Message:
    """
    Representa uma mensagem interna do broker, usada somente no core do broker (EventsRepository,etc). 
    """
    msg_id: str
    topic: str
    payload: Dict[str, Any]
    sensor_id: str
    ttl_ms: int
    priority: int
    timestamp: float  # epoch seconds
    expire_at: float  # epoch seconds

    def is_expired(self, now: float = None) -> bool:
        """Verifica se a mensagem está expirada."""
        if now is None:
            now = time.time()
        return now > self.expire_at


def create_message(
    topic: str,
    payload: Dict[str, Any],
    ttl_ms: int,
    priority: int,
    sensor_id: str
) -> Message:
    """
    Factory para criação de mensagens do broker.

    - Garante ID único
    - Converte ttl_ms para timestamp de expiração
    - Define timestamp atual
    """
    if ttl_ms <= 0:
        raise ValueError("ttl_ms maior que zero") 

    if priority < 0:
        raise ValueError("prioridade >=0")

    now = time.time()
    expire_at = now + (ttl_ms / 1000)

    return Message(
        msg_id=str(uuid.uuid4()),
        topic=topic,
        payload=payload,
        sensor_id=sensor_id,
        ttl_ms=ttl_ms,
        priority=priority,
        timestamp=now,
        expire_at=expire_at,
    )
