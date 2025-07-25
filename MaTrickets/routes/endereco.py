from typing import List
from fastapi import APIRouter, HTTPException
from models.endereco import Endereco
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Endereco])
async def list_enderecos():
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("SELECT id_endereco, cep, cidade, rua, uf, numero FROM enderecos")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return [
        Endereco(
            id_endereco=i[0], cep=i[1], cidade=i[2], rua=i[3], uf=i[4], numero=i[5]
        )
        for i in data
    ]


@router.post("/create")
async def create_endereco(endereco: Endereco):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO enderecos (id_endereco, cep, cidade, rua, uf, numero) VALUES (%s, %s, %s, %s,)",
            (
                endereco.id_endereco,
                endereco.cep,
                endereco.cidade,
                endereco.rua,
                endereco.uf,
                endereco.numero,
            ),
        )
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return "OK"
