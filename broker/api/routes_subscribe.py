from fastapi import APIRouter,Depends
from broker.api.dto import SubscribeDTO
from broker.patterns.server_request_handler import ServerRequestHandler 

router = APIRouter(prefix="/subscribe") 

def get_srh () -> ServerRequestHandler:
    from broker.api.main import srh 
    return srh 

@router.post("/")

def subscribe(dto:SubscribeDTO, srh: ServerRequestHandler= Depends(get_srh)): 
    return srh.handle_subscribe(dto)
