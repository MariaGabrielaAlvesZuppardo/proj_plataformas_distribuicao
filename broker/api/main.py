# broker/api/main.py

from fastapi import FastAPI
import asyncio

from broker.core.broker_service import BrokerService
from broker.patterns.invoker import Invoker
from broker.patterns.server_request_handler import ServerRequestHandler

from broker.api.routes_publish import router as publish_router
from broker.api.routes_subscribe import router as subscribe_router
from broker.api.routes_metrics import router as metrics_router

from broker.workers.ttl_checker import TTLChecker
from broker.workers.notification_engine import NotificationEngine



# Core do broker
broker_service = BrokerService()

# Invoker (padrão de remoting)
invoker = Invoker(broker_service)

# Server Request Handler (padrão de remoting)
srh = ServerRequestHandler(invoker)

# FastAPI instance
app = FastAPI(
    title="Sensor Broker",
    version="1.0.0",
)

# Registrar rotas
app.include_router(publish_router)
app.include_router(subscribe_router)
app.include_router(metrics_router)


@app.on_event("startup")
async def startup_event():
    """
    Inicializa workers em paralelo:
    - TTL Checker
    - Notification Engine
    """

    loop = asyncio.get_event_loop()

    ttl_checker = TTLChecker(broker_service)
    notification_engine = NotificationEngine(broker_service)

    # Iniciar ambos como tarefas assíncronas
    loop.create_task(ttl_checker.run())
    loop.create_task(notification_engine.run())

    print("[BROKER] Workers iniciados com sucesso.")
