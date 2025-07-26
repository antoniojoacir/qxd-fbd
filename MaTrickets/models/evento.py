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
    horario_fim: Optional[time] = None
    id_endereco: Endereco
    id_contato: Contato