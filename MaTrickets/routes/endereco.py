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


@router.get("/get/{id}", response_model=Endereco)
async def get_endereco_by_id(id: int):
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id_endereco, cep, cidade, rua, uf, numero FROM enderecos WHERE id_endereco = %s",
        (id,),
    )
    endereco = cursor.fetchone()
    cursor.close()
    connection.close()
    if endereco:
        return Endereco(
            id_endereco=endereco[0],
            cep=endereco[1],
            cidade=endereco[2],
            rua=endereco[3],
            uf=endereco[4],
            numero=endereco[5],
        )


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


@router.delete("/delete/{id}")
async def delete_endereco(id_endereco: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM enderecos WHERE id_endereco=%s", (id_endereco,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"Err: {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": "Endereço removido com sucesso"}
