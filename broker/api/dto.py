from pydantic import BaseModel , Field
from typing import Dict , Any 


class SensorPayload(BaseModel):
    temperatura: float = Field(...,description="Temperatura (C°) do solo")
    umidade: float = Field(...,description="Umidade (%) do solo")
    valvula: bool = Field(...,description="Estado da válvula de irrigação")

class PublishRequest(BaseModel):
    topic: str = Field(...,min_length=3)
    sensor_id: str = Field(...,min_length=1)
    payload:SensorPayload
    ttl_ms: int = Field(...,gt=0)
    priority: int=Field(1,ge=0,le=5)


class PublishDTO(BaseModel):
    topic: str
    payload: dict
    priority: int = 5
    ttl: float = 30.0


class SubscribeDTO(BaseModel):
    subscriber_id: str
    topic: str