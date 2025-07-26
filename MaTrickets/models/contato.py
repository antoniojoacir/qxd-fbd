from pydantic import BaseModel

class Contato(BaseModel):
    id_contato: int
    tipo_contato: str
    info_contato: str
