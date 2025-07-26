from pydantic import BaseModel
from models.cliente import Cliente
from models.evento import Evento


class Ticket(BaseModel):
    id_ticket: int
    numero: int
    lote: str
    
    id_cliente: Cliente
    id_evento: Evento