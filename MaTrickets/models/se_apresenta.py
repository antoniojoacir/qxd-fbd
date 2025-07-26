from pydantic import BaseModel
from models.atracao import Atracao
from models.evento import Evento


class Se_Apresenta(BaseModel):
    id_atracao: Atracao
    id_evento: Evento