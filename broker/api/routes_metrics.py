from fastapi import APIRouter, Depends
from broker.patterns.server_request_handler import ServerRequestHandler 

router = APIRouter(prefix="/metrics") 

def get_srh() -> ServerRequestHandler: 
    from broker.api.main import srh 
    return srh 

@router.get("/")
def get_metrics(srh: ServerRequestHandler = Depends(get_srh)):
    return srh.handle_metrics()