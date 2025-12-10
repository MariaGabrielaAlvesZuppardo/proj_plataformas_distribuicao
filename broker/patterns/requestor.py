# client/requestor.py

class Requestor:
    """
    Responsável por montar requisições remotas que serão enviadas
    pelo ClientRequestHandler.
    Converte chamadas de alto nível (ClientProxy) em objetos prontos
    para envio via HTTP/JSON.
    """

    def __init__(self, client_request_handler, base_url: str):
        self.client_request_handler = client_request_handler
        self.base_url = base_url.rstrip("/")

    def send_publish_request(self, topic: str, payload: dict, priority: int, ttl: float):
        """
        Monta o corpo JSON que será enviado para o broker via publish.
        """

        request_body = {
            "topic": topic,
            "payload": payload,
            "priority": priority,
            "ttl": ttl,
        }

        url = f"{self.base_url}/publish"
        return self.client_request_handler.send_http_post(url, request_body)

    def send_subscribe_request(self, subscriber_id: str, topic: str):
        """
        Solicita inscrição do cliente em um tópico.
        """

        request_body = {
            "subscriber_id": subscriber_id,
            "topic": topic
        }

        url = f"{self.base_url}/subscribe"
        return self.client_request_handler.send_http_post(url, request_body)

    def send_metrics_request(self):
        """
        Recupera métricas internas do broker.
        """

        url = f"{self.base_url}/metrics"
        return self.client_request_handler.send_http_get(url)
