from fastapi import FastAPI
from app.routes import produtos, clientes

app = FastAPI(title="SalesInsight API")

app.include_router(produtos.router)
app.include_router(clientes.router)


@app.get("/")
def read_root():
    return {"mensagem": "SalesInsight API está no ar!"}