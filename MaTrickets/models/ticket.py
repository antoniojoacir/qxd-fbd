from pydantic import BaseModel
from typing import Optional
from models.cliente import Cliente
from models.evento import Evento


class Ticket(BaseModel):
    id_ticket: int
    numero: int
    lote: str
    
    id_cliente: Cliente
    id_evento: Evento


class TicketCreate(BaseModel):
    id_ticket: int
    numero: int
    lote: str
    
    id_cliente: Cliente
    id_evento: Evento

class TicketUpdate(BaseModel):
    id_ticket: Optional[int] = None
    numero: Optional[int] = None
    lote: Optional[str] = None
    
    id_cliente: Optional[int] = None
    id_evento: Optional[int] = None
   

