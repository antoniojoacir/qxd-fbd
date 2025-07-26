from typing import List
from fastapi import APIRouter, HTTPException
from models.evento import Evento
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Evento])
async def list_eventos():
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("SELECT id_evento, titulo, data_inicio, data_fim, horario_inicio, horario_fim, id_contato, id_endereco FROM eventos")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return [
        Evento(
            id_evento=i[0], titulo=i[1], data_inicio=i[2], data_fim=i[3], horario_inicio=i[4], horario_fim=i[5,] id_contato=i[6], id_endereco=i[7]
        )
        for i in data
    ]


@router.post("/create")
async def create_evento(evento: Evento):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO eventos (id_evento, titulo, data_inicio, data_fim, horario_inicio, horario_fim, id_contato, id_endereco) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                evento.id_evento,
                evento.titulo,
                evento.data_inicio,
                evento.data_fim,
                evento.horario_inicio,
                evento.horario_fim,
                evento.id_contato,
                evento.id_endereco,
            ),
        )
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return "OK"
