from fastapi import FastAPI
from routes.endereco import router as enderecoRouter
from routes.contato import router as contatoRouter
from routes.cliente import router as clienteRouter
from routes.atracao import router as atracaoRouter

app = FastAPI(title="MaTrickets")

app.include_router(enderecoRouter, prefix="/enderecos", tags=["Endereços"])
app.include_router(contatoRouter, prefix="/contatos", tags=["Contatos"])
app.include_router(clienteRouter, prefix="/clientes", tags=["Clientes"])
app.include_router(atracaoRouter, prefix="/atracoes", tags=["Atrações"])
