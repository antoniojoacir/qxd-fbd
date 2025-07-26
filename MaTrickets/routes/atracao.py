from typing import List
from fastapi import APIRouter, HTTPException
from models.atracao import Atracao
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Atracao])
async def list_atracoes():
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("SELECT id_atracao, cnpj, nome_atracao, tipo_atracao, id_contato FROM atracoes")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return [
        Atracao(
            id_atracao=i[0], cnpj=i[1], nome_atracao=i[2], tipo_atracao=i[3], id_contato=i[4]
        )
        for i in data
    ]


@router.post("/create")
async def create_atracao(atracao: Atracao):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO atracoes (id_atracao, cnpj, nome_atracao, tipo_atracao, id_contato) VALUES (%s, %s, %s, %s, %s)",
            (
                atracao.id_atracao,
                atracao.cnpj,
                atracao.nome_atracao,
                atracao.tipo_atracao,
                atracao.id_contato,
            ),
        )
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return "OK"
