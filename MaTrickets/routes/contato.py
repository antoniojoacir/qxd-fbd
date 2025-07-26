from fastapi import APIRouter, HTTPException
from models.contato import Contato
from env.db import db_connect

router = APIRouter()


@router.get("/list/")
async def get_contato():
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT id_contato, tipo_contato, info_contato FROM contatos",
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
