from typing import List
from fastapi import APIRouter, HTTPException
from models.atracao import AtracaoNoDetails
from models.evento import EventoNoDetails
from models.se_apresenta import Se_Apresenta, SeApresentaCreate
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Se_Apresenta])
async def list_se_apresenta():
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT
                a.id_atracao, a.cnpj, a.nome_atracao, a.tipo_atracao, a.id_contato,
                e.id_evento, e.titulo, e.data_inicio, e.data_fim, e.horario_inicio, e.horario_fim, e.id_contato, e.id_endereco
            FROM se_apresenta AS sa
            LEFT JOIN atracoes AS a ON sa.id_atracao = a.id_atracao
            LEFT JOIN eventos AS e ON sa.id_evento = e.id_evento
            """
        )
        data = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail={"NOK": {e}})
    finally:
        cursor.close()
        connection.close()
    return [
        Se_Apresenta(
            atracao=AtracaoNoDetails(
                id_atracao=i[0],
                cnpj=i[1],
                nome_atracao=i[2],
                tipo_atracao=i[3],
                id_contato=i[4] if i[4] is not None else None,
            ),
            evento=EventoNoDetails(
                id_evento=i[5],
                titulo=i[6],
                data_inicio=i[7],
                data_fim=i[8],
                horario_inicio=i[9],
                horario_fim=i[10],
                id_contato=i[11] if i[11] is not None else None,
                id_endereco=i[12] if i[12] is not None else None,
            ),
        )
        for i in data
    ]


@router.get("/get/{id_atracao}/{id_evento}", response_model=Se_Apresenta)
async def get_se_apresenta_by_id(id_atracao: int, id_evento: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT
                a.id_atracao, a.cnpj, a.nome_atracao, a.tipo_atracao, a.id_contato,
                e.id_evento, e.titulo, e.data_inicio, e.data_fim, e.horario_inicio, e.horario_fim, e.id_contato, e.id_endereco
            FROM se_apresenta AS sa
            LEFT JOIN atracoes AS a ON sa.id_atracao = a.id_atracao
            LEFT JOIN eventos AS e ON sa.id_evento = e.id_evento
            WHERE sa.id_atracao = %s AND sa.id_evento = %s
            """,
            (id_atracao, id_evento),
        )
        data = cursor.fetchone()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail={"status": "NOK", "message": str(e)}
        )
    finally:
        cursor.close()
        connection.close()

    if not data:
        raise HTTPException(
            status_code=404, detail="Associação entre Atração e Evento não encontrada."
        )

    return Se_Apresenta(
        atracao=AtracaoNoDetails(
            id_atracao=data[0],
            cnpj=data[1],
            nome_atracao=data[2],
            tipo_atracao=data[3],
            id_contato=data[4] if data[4] is not None else None,
        ),
        evento=EventoNoDetails(
            id_evento=data[5],
            titulo=data[6],
            data_inicio=data[7],
            data_fim=data[8],
            horario_inicio=data[9],
            horario_fim=data[10],
            id_contato=data[11] if data[11] is not None else None,
            id_endereco=data[12] if data[12] is not None else None,
        ),
    )


@router.post("/create")
async def create_se_apresenta(se_apresenta_data: SeApresentaCreate):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT 1 FROM atracoes WHERE id_atracao = %s",
            (se_apresenta_data.id_atracao,),
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail=f"Atração com ID {se_apresenta_data.id_atracao} não encontrada.",
            )

        cursor.execute(
            "SELECT 1 FROM eventos WHERE id_evento = %s", (se_apresenta_data.id_evento,)
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail=f"Evento com ID {se_apresenta_data.id_evento} não encontrado.",
            )

        cursor.execute(
            "INSERT INTO se_apresenta (id_atracao, id_evento) VALUES (%s, %s)",
            (se_apresenta_data.id_atracao, se_apresenta_data.id_evento),
        )
        connection.commit()

        return await get_se_apresenta_by_id(
            se_apresenta_data.id_atracao, se_apresenta_data.id_evento
        )

    except HTTPException as http_exc:
        connection.rollback()
        raise http_exc
    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=400, detail={"status": "NOK", "message": str(e)}
        )
    finally:
        cursor.close()
        connection.close()


@router.delete("/delete/{id_atracao}/{id_evento}")
async def delete_se_apresenta(id_atracao: int, id_evento: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM se_apresenta WHERE id_atracao = %s AND id_evento = %s",
            (id_atracao, id_evento),
        )
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Associação a ser deletada não foi encontrada."
            )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(
            status_code=400, detail={"status": "NOK", "message": str(e)}
        )
    finally:
        cursor.close()
        connection.close()

    return {"message": "Associação removida com sucesso"}
