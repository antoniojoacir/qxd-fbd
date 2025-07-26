from typing import List
from fastapi import APIRouter, HTTPException
from models.cliente import Cliente
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Cliente])
async def list_clientes():
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id_cliente, cpf, pnome, unome, data_nasc, id_contato, id_endereco FROM clientes"
    )
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return [
        Cliente(
            id_cliente=i[0],
            cpf=i[1],
            pnome=i[2],
            unome=i[3],
            data_nasc=i[4],
            id_contato=i[5],
            id_endereco=i[6],
        )
        for i in data
    ]


@router.post("/create")
async def create_cliente(cliente: Cliente):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO clientes (id_cliente, cpf, pnome, unome, data_nascimento, id_contato, id_endereco) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                cliente.id_cliente,
                cliente.cpf,
                cliente.pnome,
                cliente.unome,
                cliente.data_nascimento,
                cliente.id_contato,
                cliente.id_endereco,
            ),
        )
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return "OK"
