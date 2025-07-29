from typing import List
from fastapi import APIRouter, HTTPException
from models.contato import Contato
from models.atracao import Atracao
from models.atracao import AtracaoCreate
from models.atracao import AtracaoUpdate
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Atracao])
async def list_atracoes():
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                a.id_atracao, a.cnpj, a.nome_atracao, a.tipo_atracao, 
                c.id_contato, c.tipo_contato, c.info_contato 
            FROM atracoes AS a 
            JOIN contatos AS c 
            ON c.id_contato = a.id_contato
            """
        )
        data = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return [
        Atracao(
            id_atracao=i[0],
            cnpj=i[1],
            nome_atracao=i[2],
            tipo_atracao=i[3],
            contato=Contato(id_contato=i[4], tipo_contato=i[5], info_contato=i[6]),
        )
        for i in data
    ]


@router.get("/get/{id}", response_model=Atracao)
async def get_atracao_by_id(index: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT
                a.id_atracao, a.cnpj, a.nome_atracao, a.tipo_atracao, 
                c.id_contato, c.tipo_contato, c.info_contato 
            FROM atracoes AS a 
            JOIN contatos AS c 
            ON c.id_contato = a.id_contato 
            WHERE id_atracao = %s
            """,
            (index,),
        )
        data = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    if data:
        return Atracao(
            id_atracao=data[0],
            cnpj=data[1],
            nome_atracao=data[2],
            tipo_atracao=data[3],
            contato=Contato(
                id_contato=data[4],
                tipo_contato=data[5],
                info_contato=data[6],
            ),
        )
    raise HTTPException(status_code=404, detail=f"NOK: Atração {index} não encontrada")


@router.post("/create")
async def create_atracao(atracao: AtracaoCreate):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_contato 
            FROM contatos 
            WHERE id_contato=%s
            """,
            (atracao.id_contato,),
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail={"NOK": f"Contato {atracao.id_contato} não encontrado"},
            )
        cursor.execute(
            """
            INSERT INTO atracoes (id_atracao, cnpj, nome_atracao, tipo_atracao, id_contato) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                atracao.id_atracao,
                atracao.cnpj,
                atracao.nome_atracao,
                atracao.tipo_atracao,
                atracao.id_contato,
            ),
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": "Atração criada com sucesso"}


@router.patch("/update/{id}")
async def update_atracao(index: int, atracao: AtracaoUpdate):
    data = {key: value for key, value in atracao if value is not None}
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_atracao
            FROM atracoes
            WHERE id_atracao=%s
            """,
            (index,),
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404, detail={"NOK": "Atração não encontrada"}
            )
        cursor.execute(
            """
            UPDATE atracoes
            SET cnpj=%s, nome_atracao=%s, tipo_atracao=%s, id_contato=%s
            WHERE id_atracao=%s
            """,
            (
                atracao.cnpj,
                atracao.nome_atracao,
                atracao.tipo_atracao,
                atracao.id_contato,
                index,
            ),
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail={"NOK": f"{e}"})
    finally:
        cursor.close()
        connection.close()
    return {"OK": f"Atração {index} atualizada com sucesso."}


@router.delete("/delete/{id}")
async def delete_atracao(index: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            DELETE FROM atracoes 
            WHERE id_atracao = %s
            """,
            (index,),
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": f"Atração {index} removida"}
