from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/list/")
async def get_contato():
    return {"OK": "Sucesso"}
