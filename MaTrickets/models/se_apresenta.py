from typing import Optional
from pydantic import BaseModel
from models.atracao import AtracaoNoDetails
from models.evento import EventoNoDetails


class Se_Apresenta(BaseModel):
    atracao: Optional[AtracaoNoDetails] = None
    evento: Optional[EventoNoDetails] = None
