
import requests
from requests.exceptions import RequestException, Timeout

class ClientRequestHandler:
    """
    Responsável por enviar requisições HTTP ao broker.
    É a camada de transporte do Remoting Pattern no cliente.
    """

    def __init__(self, timeout: float = 3.0):
        self.timeout = timeout

    def _send(self, method: str, url: str, json_body: dict | None = None):
        """
        Função interna que envia requisições HTTP com tratamento de falhas.
        """

        try:
            if method == "POST":
                response = requests.post(url, json=json_body, timeout=self.timeout)
            elif method == "GET":
                response = requests.get(url, timeout=self.timeout)
            else:
                raise ValueError(f"Método HTTP inválido: {method}")

        except Timeout:
            return {
                "status": "error",
                "error": "timeout",
                "message": f"Broker não respondeu em {self.timeout}s"
            }

        except RequestException as e:
            return {
                "status": "error",
                "error": "network_failure",
                "message": str(e)
            }

        # Processamento do retorno
        if response.status_code >= 400:
            return {
                "status": "error",
                "error": "http_error",
                "code": response.status_code,
                "message": response.text
            }

        try:
            return response.json()
        except ValueError:
            return {
                "status": "error",
                "error": "invalid_json_response",
                "message": "Resposta do broker não pôde ser decodificada"
            }


    def send_http_post(self, url: str, json_body: dict):
        """
        Envia requisição POST ao broker.
        """
        return self._send("POST", url, json_body)

    def send_http_get(self, url: str):
        """
        Envia requisição GET ao broker.
        """
        return self._send("GET", url)
