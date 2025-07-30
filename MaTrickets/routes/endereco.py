from typing import List
from fastapi import APIRouter, HTTPException
from models.endereco import Endereco
from models.endereco import EnderecoUpdate
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Endereco])
async def list_enderecos():
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_endereco, cep, cidade, rua, uf, numero 
            FROM enderecos
            """
        )
        data = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
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
    try:
        cursor.execute(
            """
            SELECT id_endereco, cep, cidade, rua, uf, numero 
            FROM enderecos 
            WHERE id_endereco=%s
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
        return Endereco(
            id_endereco=data[0],
            cep=data[1],
            cidade=data[2],
            rua=data[3],
            uf=data[4],
            numero=data[5],
        )
    raise HTTPException(status_code=404, detail=f"NOK: Endereço {id} não encontrado")


@router.post("/create")
async def create_endereco(endereco: Endereco):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO enderecos (id_endereco, cep, cidade, rua, uf, numero) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                endereco.id_endereco,
                endereco.cep,
                endereco.cidade,
                endereco.rua,
                endereco.uf,
                endereco.numero,
            ),
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": "Endereço criado com sucesso"}


@router.patch("/update/{id}")
async def update_endereco(id: int, endereco: EnderecoUpdate):
    data = {key: value for key, value in endereco if value is not None}
    if not data:
        raise HTTPException(
            status_code=404,
            detail={"NOK": "Nenhum campo para atualizar foi fornecido."},
        )
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_endereco 
            FROM enderecos 
            WHERE id_endereco=%s
            """,
            (id,),
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Endereço {id} não existe")

        set_ = ", ".join([f"{key}=%s" for key in data.keys()])
        values = list(data.values())
        values.append(id)
        cursor.execute(
            f"""
            UPDATE enderecos
            SET {set_}
            WHERE id_endereco=%s
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
    return {"OK": f"Endereço {id} atualizado com sucesso"}


@router.delete("/delete/{id}")
async def delete_endereco(id_endereco: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            UPDATE clientes 
            SET id_endereco = NULL 
            WHERE id_endereco = %s
            """,
            (id_endereco,),
        )

        cursor.execute(
            """
            UPDATE eventos 
            SET id_endereco = NULL 
            WHERE id_endereco = %s
            """,
            (id_endereco,),
        )
        cursor.execute(
            """
            DELETE FROM enderecos 
            WHERE id_endereco=%s
            """,
            (id_endereco,),
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": "Endereço removido com sucesso"}
