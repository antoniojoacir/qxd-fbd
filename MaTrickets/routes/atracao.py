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
            LEFT JOIN contatos AS c ON c.id_contato = a.id_contato
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
            contato=(
                Contato(id_contato=i[4], tipo_contato=i[5], info_contato=i[6])
                if i[4] is not None
                else None
            ),
        )
        for i in data
    ]


@router.get("/get/{id}", response_model=Atracao)
async def get_atracao_by_id(id: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT
                a.id_atracao, a.cnpj, a.nome_atracao, a.tipo_atracao, 
                c.id_contato, c.tipo_contato, c.info_contato 
            FROM atracoes AS a 
            LEFT JOIN contatos AS c ON c.id_contato = a.id_contato 
            WHERE id_atracao = %s
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
        return Atracao(
            id_atracao=data[0],
            cnpj=data[1],
            nome_atracao=data[2],
            tipo_atracao=data[3],
            contato=(
                Contato(
                    id_contato=data[4],
                    tipo_contato=data[5],
                    info_contato=data[6],
                )
                if data[4] is not None
                else None
            ),
        )
    raise HTTPException(status_code=404, detail=f"NOK: Atração {id} não encontrada")


@router.post("/create")
async def create_atracao(atracao: AtracaoCreate):
    data = {key: value for key, value in atracao if value is not None}
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
                (atracao.id_contato,),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail={"NOK": f"Contato {atracao.id_contato} não encontrado"},
                )
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        cursor.execute(
            f"""
            INSERT INTO atracoes ({columns}) 
            VALUES ({placeholders})
            """,
            values,
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
async def update_atracao(id: int, atracao: AtracaoUpdate):
    data = {key: value for key, value in atracao if value is not None}
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
        cursor.execute(
            """
            SELECT id_atracao
            FROM atracoes
            WHERE id_atracao=%s
            """,
            (id,),
        )
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Atração {id} não encontrada")
        set_ = ", ".join([f"{key}=%s" for key in data.keys()])
        values = list(data.values())
        values.append(id)
        cursor.execute(
            f"""
            UPDATE atracoes
            SET {set_}
            WHERE id_atracao=%s
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
    return {"OK": f"Atração {id} atualizada com sucesso."}


@router.delete("/delete/{id}")
async def delete_atracao(id: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_atracao
            FROM atracoes
            WHERE id_atracao=%s
            """,
            (id,),
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail=f"Atração {id} inexistente.",
            )
        cursor.execute(
            """
            UPDATE se_apresenta
            SET id_atracao = NULL
            WHERE id_atracao=%s
            """,
            (id,),
        )
        cursor.execute(
            """
            DELETE FROM atracoes 
            WHERE id_atracao = %s
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
    return {"OK": f"Atração {id} removida"}
