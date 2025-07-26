from typing import List
from fastapi import APIRouter, HTTPException
from models.se_apresenta import Se_Apresenta
from env.db import db_connect

router = APIRouter()


@router.get("/list", response_model=List[Se_Apresenta])
async def list_se_apresenta():
    connection = db_connect()
    cursor = connection.cursor()
    cursor.execute("SELECT id_atracao, id_evento FROM se_apresenta")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return [
        Se_Apresenta(
            id_atracao=i[0], id_evento=i[1]
        )
        for i in data
    ]


@router.post("/create")
async def create_se_apresenta(se_apresenta: Se_Apresenta):
    connection = db_connect()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO se_apresenta (id_atracao, id_evento) VALUES (%s, %s)",
            (
                se_apresenta.id_atracao,
                se_apresenta.id_evento,
            ),
        )
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=400, detail=f"NOK: {e}")
    finally:
        cursor.close()
        connection.close()
    return "OK"
