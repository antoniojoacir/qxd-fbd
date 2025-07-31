from typing import List
from fastapi import APIRouter, HTTPException
from models.evento import Evento, EventoNoDetails
from models.ticket import Ticket, TicketCreate, TicketUpdate
from models.cliente import Cliente, ClienteNoDetails
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Ticket])
async def list_tickets():
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                t.id_ticket, t.numero, t.lote,
                c.id_cliente, c.cpf, c.pnome, c.unome, c.data_nasc, c.genero, c.id_contato, c.id_endereco,
                e.id_evento, e.titulo, e.data_inicio, e.data_fim, e.horario_inicio, e.horario_fim, e.id_contato, e.id_endereco
            FROM tickets AS t
            LEFT JOIN clientes AS c ON t.id_cliente = c.id_cliente
            LEFT JOIN eventos AS e ON t.id_evento = e.id_evento
            """
        )
        data = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail={"NOK": {e}})
    finally:
        cursor.close()
        connection.close()
    return [
        Ticket(
            id_ticket=i[0],
            numero=i[1],
            lote=i[2],
            cliente=(
                (
                    ClienteNoDetails(
                        id_cliente=i[3],
                        cpf=i[4],
                        pnome=i[5],
                        unome=i[6],
                        data_nasc=i[7],
                        genero=i[8],
                        id_contato=i[9],
                        id_endereco=i[10] if i[10] is not None else None,
                    )
                )
                if i[3] is not None
                else None
            ),
            evento=(
                (
                    EventoNoDetails(
                        id_evento=i[11],
                        titulo=i[12],
                        data_inicio=i[13],
                        data_fim=i[14],
                        horario_inicio=i[15],
                        horario_fim=i[16],
                        id_contato=i[17] if i[17] is not None else None,
                        id_endereco=i[18] if i[18] is not None else None,
                    )
                )
                if i[11] is not None
                else None
            ),
        )
        for i in data
    ]


@router.get("/get/{id}", response_model=Ticket)
async def get_ticket_by_id(id: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT 
                t.id_ticket, t.numero, t.lote,
                c.id_cliente, c.cpf, c.pnome, c.unome, c.data_nasc, c.genero, c.id_contato, c.id_endereco,
                e.id_evento, e.titulo, e.data_inicio, e.data_fim, e.horario_inicio, e.horario_fim, e.id_contato, e.id_endereco
            FROM tickets AS t
            LEFT JOIN clientes AS c ON t.id_cliente = c.id_cliente
            LEFT JOIN eventos AS e ON t.id_evento = e.id_evento
            WHERE id_ticket=%s
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
        return Ticket(
            id_ticket=data[0],
            numero=data[1],
            lote=data[2],
            cliente=(
                (
                    ClienteNoDetails(
                        id_cliente=data[3],
                        cpf=data[4],
                        pnome=data[5],
                        unome=data[6],
                        data_nasc=data[7],
                        genero=data[8],
                        id_contato=data[9],
                        id_endereco=data[10] if data[10] is not None else None,
                    )
                )
                if data[3] is not None
                else None
            ),
            evento=(
                (
                    EventoNoDetails(
                        id_evento=data[11],
                        titulo=data[12],
                        data_inicio=data[13],
                        data_fim=data[14],
                        horario_inicio=data[15],
                        horario_fim=data[16],
                        id_contato=data[17] if data[17] is not None else None,
                        id_endereco=data[18] if data[18] is not None else None,
                    )
                )
                if data[11] is not None
                else None
            ),
        )
    raise HTTPException(status_code=404, detail=f"NOK: Ticket {id} não encontrado.")


@router.post("/create")
async def create_ticket(ticket: TicketCreate):
    data = {key: value for key, value in ticket if value is not None}
    connection = db_connect()
    cursor = connection.cursor()
    try:
        if "id_evento" in data:
            cursor.execute(
                """
                SELECT id_evento 
                FROM eventos
                WHERE id_evento = %s
                """,
                (data["id_evento"],),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail=f"Evento com ID {data['id_evento']} não encontrado.",
                )

        if "id_cliente" in data:
            cursor.execute(
                """
                SELECT id_cliente 
                FROM clientes
                WHERE id_cliente = %s
                """,
                (data["id_cliente"],),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail=f"Cliente com ID {data['id_cliente']} não encontrado.",
                )

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        cursor.execute(
            f"""
            INSERT INTO tickets ({columns}) 
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
    return {"OK": "Ticket criado com sucesso."}


@router.patch("/update/{id}")
async def update_ticket(id: int, evento: TicketUpdate):
    data = {key: value for key, value in evento if value is not None}
    if not data:
        raise HTTPException(
            status_code=400,
            detail={"NOK": "Nenhum campo para atualizar foi fornecido."},
        )
    connection = db_connect()
    cursor = connection.cursor()
    try:
        if "id_evento" in data:
            cursor.execute(
                """
                SELECT id_evento 
                FROM eventos
                WHERE id_evento = %s
                """,
                (data["id_evento"],),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail=f"Evento com ID {data['id_evento']} não encontrado.",
                )

        if "id_cliente" in data:
            cursor.execute(
                """
                SELECT id_cliente 
                FROM clientes
                WHERE id_cliente = %s
                """,
                (data["id_cliente"],),
            )
            if not cursor.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail=f"Cliente com ID {data['id_cliente']} não encontrado.",
                )
        set_ = ", ".join([f"{key}=%s" for key in data.keys()])
        values = list(data.values())
        values.append(id)
        cursor.execute(
            f"""
            UPDATE tickets
            SET {set_}
            WHERE id_ticket=%s
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
    return {"OK": f"Ticket {id} atualizado com sucesso."}


@router.delete("/delete/{id}")
async def delete_ticket(id: int):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT id_ticket
            FROM tickets 
            WHERE id_ticket=%s
            """,
            (id,),
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail=f"Ticket {id} inexistente.",
            )
        cursor.execute(
            """
            DELETE FROM tickets
            WHERE id_ticket=%s
            """,
            (id,)
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK {e}")
    finally:
        cursor.close()
        connection.close()
    return {"OK": f"Ticket {id} removido"}
