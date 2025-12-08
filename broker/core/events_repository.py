import heapq
import time
from threading import Lock
from typing import Dict, List, Tuple, Optional

from broker.models.message import Message


class EventsRepository:
    """
    Repositório de mensagens por tópico.
    Responsável por:
      - Heap de prioridade
      - TTL
      - Ordenação determinística (priority, timestamp, sequence)
    """

    def __init__(self):
        self._lock = Lock()
        self._topics: Dict[str, List[Tuple]] = {}
        self._sequence = 0  # resolve empates no heap

    # -------------------------------------------------------

    def enqueue(self, message: Message):
        """Insere uma mensagem no heap do tópico."""
        with self._lock:
            topic = message.topic
            if topic not in self._topics:
                self._topics[topic] = []

            entry = (
                message.priority,
                message.timestamp,
                self._sequence,
                message
            )

            heapq.heappush(self._topics[topic], entry)
            self._sequence += 1

    # -------------------------------------------------------

    def dequeue(self, topic: str) -> Optional[Message]:
        """
        Remove e retorna a mensagem mais prioritária.
        Remove também mensagens expiradas automaticamente.
        """
        with self._lock:
            if topic not in self._topics or not self._topics[topic]:
                return None

            while self._topics[topic]:
                priority, ts, seq, msg = heapq.heappop(self._topics[topic])

                if self._is_expired(msg):
                    continue  # descarte silencioso

                return msg

            return None

    # -------------------------------------------------------

    def peek(self, topic: str) -> Optional[Message]:
        """Retorna a próxima mensagem sem remover, ignorando expiradas."""
        with self._lock:
            if topic not in self._topics or not self._topics[topic]:
                return None

            # Limpa expiradas do topo
            while self._topics[topic]:
                priority, ts, seq, msg = self._topics[topic][0]
                if self._is_expired(msg):
                    heapq.heappop(self._topics[topic])
                    continue
                return msg

            return None

    # -------------------------------------------------------

    def remove_expired(self) -> int:
        """Remove todas mensagens expiradas de todos os tópicos."""
        now = time.time()
        removed = 0

        with self._lock:
            for topic, heap in self._topics.items():
                new_heap = []
                for priority, ts, seq, msg in heap:
                    if msg.timestamp + msg.ttl_ms / 1000 < now:
                        removed += 1
                        continue
                    new_heap.append((priority, ts, seq, msg))

                heapq.heapify(new_heap)
                self._topics[topic] = new_heap

        return removed

    # -------------------------------------------------------

    def count(self, topic: str) -> int:
        if topic not in self._topics:
            return 0
        return len(self._topics[topic])

    # -------------------------------------------------------

    def get_all_for_debug(self) -> Dict[str, List[Message]]:
        with self._lock:
            result = {}
            for topic, heap in self._topics.items():
                result[topic] = [entry[3] for entry in heap]
            return result

    # -------------------------------------------------------

    @staticmethod
    def _is_expired(msg: Message) -> bool:
        now = time.time()
        expires_at = msg.timestamp + msg.ttl_ms / 1000
        return now > expires_at
