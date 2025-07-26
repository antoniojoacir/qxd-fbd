from typing import List
from fastapi import APIRouter, HTTPException
from models.contato import Contato
from models.endereco import Endereco
from models.cliente import Cliente
from env.db import db_connect
import psycopg2.extras

router = APIRouter()


@router.get("/list", response_model=List[Cliente])
async def list_clientes():
    connection = db_connect()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    data = []
    try:
        cursor.execute(
            """
            SELECT 
                c.id_cliente, c.cpf, c.pnome, c.unome, c.data_nasc,
                ct.id_contato, ct.tipo_contato, ct.info_contato,
                e.id_endereco, e.cep, e.cidade, e.rua, e.uf, e.numero
            FROM clientes AS c
            JOIN contatos AS ct ON c.id_contato = ct.id_contato
            JOIN enderecos AS e ON c.id_endereco = e.id_endereco
            """
        )
        data = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
        return [
            Cliente(
                id_cliente=row["id_cliente"],
                cpf=row["cpf"],
                pnome=row["pnome"],
                unome=row["unome"],
                data_nasc=row["data_nasc"],
                contato=Contato(
                    id_contato=row["id_contato"],
                    tipo_contato=row["tipo_contato"],
                    info_contato=row["info_contato"],
                ),
                endereco=Endereco(
                    id_endereco=row["id_endereco"],
                    cep=row["cep"],
                    cidade=row["cidade"],
                    rua=row["rua"],
                    uf=row["uf"],
                    numero=row["numero"],
                ),
            )
            for row in data
        ]


@router.post("/create")
async def create_cliente(cliente: Cliente):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO clientes (id_cliente, cpf, pnome, unome, data_nasc, id_contato, id_endereco) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                cliente.id_cliente,
                cliente.cpf,
                cliente.pnome,
                cliente.unome,
                cliente.data_nasc,
                cliente.contato,
                cliente.endereco,
            ),
        )
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return "OK"
