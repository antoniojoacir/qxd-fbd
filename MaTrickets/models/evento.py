from pydantic import BaseModel
from typing import Optional
from datetime import date, time
from models.endereco import Endereco
from models.contato import Contato


class Evento(BaseModel):
    id_evento: int
    titulo: str
    data_inicio: date
    data_fim: date
    horario_inicio: time
    horario_fim: time
    contato: Optional[Contato] = None
    endereco: Optional[Endereco] = None


class EventoCreate(BaseModel):
    id_evento: int
    titulo: str
    data_inicio: date
    data_fim: date
    horario_inicio: time
    horario_fim: time
    id_contato: Optional[int] = None
    id_endereco: Optional[int] = None

