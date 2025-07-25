from fastapi import FastAPI
from routes.endereco import router as enderecoRouter


app = FastAPI(title="MaTrickets")

app.include_router(enderecoRouter, prefix="/enderecos", tags=["Endereços"])
