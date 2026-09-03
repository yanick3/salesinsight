from fastapi import FastAPI
from app.routes import produtos, clientes, upload, dashboard, insights

app = FastAPI(title="SalesInsight API")

app.include_router(produtos.router)
app.include_router(clientes.router)
app.include_router(upload.router)
app.include_router(dashboard.router)
app.include_router(insights.router)


@app.get("/")
def read_root():
    return {"mensagem": "SalesInsight API está no ar!"}