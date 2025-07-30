from os import uname
from typing import List
from fastapi import APIRouter, HTTPException
from models.contato import Contato
from models.endereco import Endereco
from models.cliente import Cliente
from models.cliente import ClienteCreate
from models.cliente import ClienteUpdate
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
            LEFT JOIN enderecos AS e ON c.id_endereco = e.id_endereco
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
            endereco=(
                Endereco(
                    id_endereco=i[9],
                    cep=i[10],
                    cidade=i[11],
                    rua=i[12],
                    uf=i[13],
                    numero=i[14],
                )
                if i[9] is not None
                else None
            ),
        )
        for i in data
    ]


@router.get("/get/{id}", response_model=Cliente)
async def get_cliente_by_id(id: int):
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
            LEFT JOIN enderecos AS e ON c.id_endereco = e.id_endereco
            WHERE c.id_cliente=%s
            """,
            (id,),
        )
        data = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"NOK {e}")
    finally:
        cursor.close()
        connection.close()
    if data:
        return Cliente(
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
            endereco=(
                Endereco(
                    id_endereco=data[9],
                    cep=data[10],
                    cidade=data[11],
                    rua=data[12],
                    uf=data[13],
                    numero=data[14],
                )
                if data[9] is not None
                else None
            ),
        )
    raise HTTPException(status_code=404, detail=f"NOK: Cliente {id} não encontrado")


@router.post("/create")
async def create_cliente(cliente: ClienteCreate):
    data = {key: value for key, value in cliente if value is not None}
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_contato 
            FROM contatos 
            WHERE id_contato=%s
            """,
            (data["id_contato"],),
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail={f"Contato {cliente.id_contato} não encontrado"},
            )
        if "id_endereco" in data:
            cursor.execute(
                """
                SELECT id_endereco 
                FROM enderecos 
                WHERE id_endereco=%s
                """,
                (data["id_endereco"],),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail={f"Endereco {cliente.id_endereco} não encontrado"},
                )
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        cursor.execute(
            f"""
            INSERT INTO clientes ({columns}) 
            VALUES ({placeholders})
            """,
            values,
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": f"Cliente {data["id_cliente"]}:{data["pnome"]} criado com sucesso."}


@router.patch("/update/{id}")
async def update_cliente(id: int, cliente: ClienteUpdate):
    data = {key: value for key, value in cliente if value is not None}
    if not data:
        raise HTTPException(
            status_code=400,
            detail={"NOK": "Nenhum campo para atualizar foi fornecido."},
        )
    connection = db_connect()
    cursor = connection.cursor()
    try:
        if "id_contato" in data:
            cursor.execute(
                """
                SELECT id_contato 
                FROM contatos 
                WHERE id_contato=%s
                """,
                (data["id_contato"],),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail=f"Contato {data["id_contato"]} não encontrado",
                )
        if "id_endereco" in data:
            cursor.execute(
                """
                SELECT id_endereco 
                FROM enderecos 
                WHERE id_endereco=%s
                """,
                (data["id_endereco"],),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail=f"Endereco {data["id_endereco"]}, não encontrado",
                )
        set_ = ", ".join([f"{key}=%s" for key in data.keys()])
        values = list(data.values())
        values.append(id)
        cursor.execute(
            f"""
            UPDATE clientes
            SET {set_}
            WHERE id_cliente=%s
            """,
            tuple(values),
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail={"NOK": f"{e}"})
    finally:
        cursor.close()
        connection.close()
    return {"OK": f"Cliente {id} atualizado com sucesso."}


@router.delete("/delete/{id}")
async def delete_cliente(id: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_cliente
            FROM clientes
            WHERE id_cliente=%s
            """,
            (id,),
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Cliente {id} não existe")
        cursor.execute(
            """
            UPDATE tickets
            SET id_cliente = NULL
            WHERE id_cliente=%s
            """,
            (id,),
        )
        cursor.execute(
            """
            DELETE FROM clientes
            WHERE id_cliente=%s
            """,
            (id,),
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": f"Cliente {id} removido com sucesso."}
