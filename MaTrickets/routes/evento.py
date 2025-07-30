from typing import List
from fastapi import APIRouter, HTTPException
from models.endereco import Endereco
from models.evento import Evento, EventoCreate, EventoUpdate
from models.contato import Contato
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Evento])
async def list_eventos():
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
        SELECT 
            e.id_evento, e.titulo, e.data_inicio, e.data_fim, e.horario_inicio, e.horario_fim, 
            c.id_contato, c.tipo_contato, c.info_contato,
            ed.id_endereco, ed.cep, ed.cidade, ed.rua, ed.uf, ed.numero 
        FROM eventos AS e
        LEFT JOIN contatos AS c ON e.id_contato = c.id_contato
        LEFT JOIN enderecos AS ed ON e.id_endereco = ed.id_endereco
        """
        )
        data = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail={"NOK": {e}})
    finally:
        cursor.close()
        connection.close()
    return [
        Evento(
            id_evento=i[0],
            titulo=i[1],
            data_inicio=i[2],
            data_fim=i[3],
            horario_inicio=i[4],
            horario_fim=i[5],
            contato=(
                Contato(id_contato=i[6], tipo_contato=i[7], info_contato=i[8])
                if i[6] is not None
                else None
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


@router.get("/get/{id}", response_model=Evento)
async def get_evento_by_id(id: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                e.id_evento, e.titulo, e.data_inicio, e.data_fim, e.horario_inicio, e.horario_fim, 
                c.id_contato, c.tipo_contato, c.info_contato,
                ed.id_endereco, ed.cep, ed.cidade, ed.rua, ed.uf, ed.numero 
            FROM eventos AS e
            LEFT JOIN contatos AS c ON e.id_contato = c.id_contato
            LEFT JOIN enderecos AS ed ON e.id_endereco = ed.id_endereco
            WHERE id_evento=%s
            """,
            (id,),
        )
        data = cursor.fetchone()
    except Exception as e:
        raise HTTPException(status_code=400, detail={"NOK": {e}})
    finally:
        cursor.close()
        connection.close()
    if data:
        return Evento(
            id_evento=data[0],
            titulo=data[1],
            data_inicio=data[2],
            data_fim=data[3],
            horario_inicio=data[4],
            horario_fim=data[5],
            contato=(
                Contato(id_contato=data[6], tipo_contato=data[7], info_contato=data[8])
                if data[6] is not None
                else None
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
    raise HTTPException(status_code=404, detail=f"NOK: Evento {id} não encontrado.")


@router.post("/create")
async def create_evento(evento: EventoCreate):
    data = {key: value for key, value in evento if value is not None}
    connection = db_connect()
    cursor = connection.cursor()
    try:
        if "id_contato" in data:
            cursor.execute(
                """
                SELECT id_contato 
                FROM contatos 
                WHERE id_contato = %s
                """,
                (data["id_contato"],),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail=f"Contato com ID {data['id_contato']} não encontrado.",
                )

        if "id_endereco" in data:
            cursor.execute(
                """
                SELECT id_endereco 
                FROM enderecos 
                WHERE id_endereco = %s
                """,
                (data["id_endereco"],),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail=f"Endereço com ID {data['id_endereco']} não encontrado.",
                )

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        cursor.execute(
            f"""
            INSERT INTO eventos ({columns}) 
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
    return {"OK": "Evento criado com sucesso."}


@router.patch("/update")
async def update_evento(id: int, evento: EventoUpdate):
    data = {key: value for key, value in evento if value is not None}
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
                WHERE id_contato = %s
                """,
                (data["id_contato"],),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail=f"Contato com ID {data['id_contato']} não encontrado.",
                )

        if "id_endereco" in data:
            cursor.execute(
                """
                SELECT id_endereco 
                FROM enderecos 
                WHERE id_endereco = %s
                """,
                (data["id_endereco"],),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail=f"Endereço com ID {data['id_endereco']} não encontrado.",
                )
        set_ = ", ".join([f"{key}=%s" for key in data.keys()])
        values = list(data.values())
        values.append(id)
        cursor.execute(
            f"""
            UPDATE eventos
            SET {set_}
            WHERE id_evento=%s
            """,
            tuple(values),
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": f"Evento {id} atualizado com sucesso."}


@router.delete("/delete/{id}")
async def delete_evento(id: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_evento
            FROM eventos 
            WHERE id_evento=%s
            """,
            (id,),
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail=f"Evento {id} inexistente.",
            )
        cursor.execute(
            """
            UPDATE tickets
            SET id_evento = NULL
            WHERE id_evento=%s
            """,
            (id,),
        )
        cursor.execute(
            """
            UPDATE se_apresenta 
            SET id_evento = NULL
            WHERE id_evento=%s
            """,
            (id,),
        )
        cursor.execute(
            """
            DELETE FROM eventos 
            WHERE id_evento = %s
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
    return {"OK": f"Evento {id} removido"}
