from pydantic import BaseModel
from typing import Optional
from models.cliente import ClienteNoDetails
from models.evento import EventoNoDetails


class Ticket(BaseModel):
    id_ticket: int
    numero: int
    lote: str

    cliente: Optional[ClienteNoDetails] = None
    evento: Optional[EventoNoDetails] = None


class TicketCreate(BaseModel):
    id_ticket: int
    numero: int
    lote: str

    id_cliente: Optional[int] = None
    id_evento: Optional[int] = None


class TicketUpdate(BaseModel):
    id_ticket: Optional[int] = None
    numero: Optional[int] = None
    lote: Optional[str] = None

    id_cliente: Optional[int] = None
    id_evento: Optional[int] = None
