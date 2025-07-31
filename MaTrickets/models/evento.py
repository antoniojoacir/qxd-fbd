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


class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    horario_inicio: Optional[time] = None
    horario_fim: Optional[time] = None
    id_contato: Optional[int] = None
    id_endereco: Optional[int] = None

class EventoNoDetails(BaseModel):
    id_evento: int
    titulo: str
    data_inicio: date
    data_fim: date
    horario_inicio: time
    horario_fim: time
    id_contato: Optional[int] = None
    id_endereco: Optional[int] = None

