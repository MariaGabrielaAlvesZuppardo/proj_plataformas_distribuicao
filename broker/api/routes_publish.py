from fastapi import APIRouter, Depends
from broker.api.dto import PublishDTO
from broker.patterns.server_request_handler import ServerRequestHandler 

router = APIRouter(prefix="/publish")

def get_srh()-> ServerRequestHandler:
    from broker.api.main import srh 
    return srh

@router.post("/")

def publish(dto: PublishDTO, srh: ServerRequestHandler = Depends(get_srh)):
    return srh.handle_publish(dto) 