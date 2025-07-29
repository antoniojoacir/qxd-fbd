from typing import List
from fastapi import APIRouter, HTTPException
from models.contato import Contato
from models.endereco import Endereco
from models.cliente import Cliente
from models.cliente import ClienteCreate
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Cliente])
async def list_clientes():
    connection = db_connect()
    cursor = connection.cursor()
    data = []
    try:
        cursor.execute(
            """
            SELECT 
                c.id_cliente, c.cpf, c.pnome, c.unome, c.data_nasc, c.genero,
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
            id_cliente=i[0],
            cpf=i[1],
            pnome=i[2],
            unome=i[3],
            data_nasc=i[4],
            genero=i[5],
            contato=Contato(
                id_contato=i[6],
                tipo_contato=i[7],
                info_contato=i[8],
            ),
            endereco=Endereco(
                id_endereco=i[9],
                cep=i[10],
                cidade=i[11],
                rua=i[12],
                uf=i[13],
                numero=i[14],
            ),
        )
        for i in data
    ]


@router.get("/list/{id}")
async def get_cliente_by_id(index: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                c.id_cliente, c.cpf, c.pnome, c.unome, c.data_nasc, c.genero,
                ct.id_contato, ct.tipo_contato, ct.info_contato,
                e.id_endereco, e.cep, e.cidade, e.rua, e.uf, e.numero
            FROM clientes AS c
            JOIN contatos AS ct ON c.id_contato = ct.id_contato
            JOIN enderecos AS e ON c.id_endereco = e.id_endereco
            WHERE c.id_cliente=%s
            """,
            (index,),
        )
        data = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"NOK {e}")
    finally:
        cursor.close()
        connection.close()
    if data:
        return (
            Cliente(
                id_cliente=data[0],
                cpf=data[1],
                pnome=data[2],
                unome=data[3],
                data_nasc=data[4],
                genero=data[5],
                contato=Contato(
                    id_contato=data[6],
                    tipo_contato=data[7],
                    info_contato=data[8],
                ),
                endereco=Endereco(
                    id_endereco=data[9],
                    cep=data[10],
                    cidade=data[11],
                    rua=data[12],
                    uf=data[13],
                    numero=data[14],
                ),
            ),
        )
    raise HTTPException(status_code=404, detail=f"NOK: Atração {id} não encontrada")


@router.post("/create")
async def create_cliente(cliente: ClienteCreate):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_contato 
            FROM contatos 
            WHERE id_contato=%s
            """,
            (cliente.id_contato,),
        )
        contato = cursor.fetchone()
        if not contato:
            raise HTTPException(
                status_code=404,
                detail={f"Contato {cliente.id_contato} não encontrado"},
            )
        cursor.execute(
            """
            SELECT id_endereco 
            FROM enderecos 
            WHERE id_endereco=%s
            """,
            (cliente.id_endereco,),
        )
        endereco = cursor.fetchone()
        if not endereco:
            raise HTTPException(
                status_code=404,
                detail={f"Endereco {cliente.id_endereco} não encontrado"},
            )

        cursor.execute(
            """
            INSERT INTO clientes (id_cliente, cpf, pnome, unome, data_nasc, id_contato, id_endereco) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                cliente.id_cliente,
                cliente.cpf,
                cliente.pnome,
                cliente.unome,
                cliente.data_nasc,
                cliente.id_contato,
                cliente.id_endereco,
            ),
        )
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK {e}")
    finally:
        cursor.close()
        connection.close()
    return "OK"
