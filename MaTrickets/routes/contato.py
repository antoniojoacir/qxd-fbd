from typing import List
from fastapi import APIRouter, HTTPException
from models.contato import Contato, ContatoUpdate
from env.db import db_connect

router = APIRouter()


@router.get("/list/", response_model=List[Contato])
async def get_contato():
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_contato, tipo_contato, info_contato 
            FROM contatos
            """,
        )
        data = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return [
        Contato(id_contato=i[0], tipo_contato=i[1], info_contato=i[2]) for i in data
    ]


@router.get("/get/{id}", response_model=Contato)
async def get_contato_by_id(id: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_contato, tipo_contato, info_contato
            FROM contatos
            WHERE id_contato=%s
            """,
            (id,),
        )
        data = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    if data:
        return Contato(
            id_contato=data[0],
            tipo_contato=data[1],
            info_contato=data[2],
        )
    raise HTTPException(status_code=404, detail=f"NOK: Contato {id} não encontrada")


@router.post("/create")
async def create_contato(contato: Contato):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_contato
            FROM contatos
            WHERE id_contato=%s
            """,
            (contato.id_contato,),
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail=f"Contato {contato.id_contato} já existe.",
            )
        cursor.execute(
            """
            INSERT INTO contatos (id_contato, tipo_contato, info_contato)
            VALUES (%s, %s, %s)
            """,
            (contato.id_contato, contato.tipo_contato, contato.info_contato),
        )
        connection.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": "Contato criado com sucesso."}


@router.patch("/update/{id}")
async def update_contato(id: int, contato: ContatoUpdate):
    data = {key: value for key, value in contato if value is not None}
    if not data:
        raise HTTPException(
            status_code=400,
            detail="Nenhum campo para atualizar foi fornecido.",
        )
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
                SELECT id_contato
                FROM contatos
                WHERE id_contato=%s
                """,
            (id,),
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail=f"Contato {id} não encontrado",
            )
        set_ = ", ".join([f"{key}=%s" for key in data.keys()])
        values = list(data.values())
        values.append(id)
        cursor.execute(
            f"""
            UPDATE contatos
            SET {set_}
            WHERE id_contato=%s
            """,
            tuple(values),
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": f"Contato {id} atualizado com sucesso."}
