from typing import List
from fastapi import APIRouter, HTTPException
from models.ticket import Ticket
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Ticket])
async def list_tickets():
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("SELECT id_ticket, numero, lote, id_cliente, id_evento FROM tickets")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return [
        Ticket(
            id_ticket=i[0], numero=i[1], lote=i[2], id_cliente=i[3], id_evento=i[4]
        )
        for i in data
    ]


@router.post("/create")
async def create_ticket(ticket: Ticket):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO tickets (id_ticket, numero, lote, id_cliente, id_evento) VALUES (%s, %s, %s, %s, %s)",
            (
                ticket.id_ticket,
                ticket.numero,
                ticket.lote,
                ticket.id_cliente,
                ticket.id_evento,
            ),
        )
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return "OK"
