from typing import List
from fastapi import APIRouter, HTTPException
from models.contato import Contato
from models.atracao import Atracao
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Atracao])
async def list_atracoes():
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT \
                a.id_atracao, a.cnpj, a.nome_atracao, a.tipo_atracao, \
                c.id_contato, c.tipo_contato, c.info_contato \
            FROM atracoes AS a \
            JOIN contatos AS c ON c.id_contato = a.id_contato"
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


@router.get("/list/{id}")
async def get_atracao_by_id(id: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT \
                a.id_atracao, a.cnpj, a.nome_atracao, a.tipo_atracao, \
                c.id_contato, c.tipo_contato, c.info_contato \
            FROM atracoes AS a \
            JOIN contatos AS c ON c.id_contato = a.id_contato \
            WHERE id_atracao = %s",
            (id,),
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
    return HTTPException(status_code=404, detail={"NOK": " Atração não encontrada"})


@router.post("/create")
async def create_atracao(atracao: Atracao):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO atracoes (id_atracao, cnpj, nome_atracao, tipo_atracao, id_contato) \
                VALUES (%s, %s, %s, %s, NULL)",
            (
                atracao.id_atracao,
                atracao.cnpj,
                atracao.nome_atracao,
                atracao.tipo_atracao,
            ),
        )
        cursor.execute(
            "SELECT id_contato FROM contatos WHERE id_contato=%s",
            (atracao.contato.id_contato,),
        )
        contato = cursor.fetchone()
        if contato:
            cursor.execute(
                "UPDATE atracoes SET id_contato=%s WHERE id_atracao=%s",
                (contato[0], atracao.id_atracao),
            )
        else:
            cursor.execute(
                "INSERT INTO contatos (id_contato, tipo_contato, info_contato) values (%s, %s, %s)",
                (
                    atracao.contato.id_contato,
                    atracao.contato.tipo_contato,
                    atracao.contato.info_contato,
                ),
            )
            cursor.execute(
                "UPDATE atracoes SET id_contato=%s WHERE id_atracao=%s",
                (atracao.contato.id_contato, atracao.id_atracao),
            )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": "Atração criada com sucesso"}


@router.delete("/delete/{id}")
async def delete_atracao(id: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM atracoes WHERE id_atracao = %s", (id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": f"Atração {id} removida"}
