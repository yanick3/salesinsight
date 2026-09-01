from fastapi import FastAPI

app = FastAPI(title="SalesInsight API")


@app.get("/")
def read_root():
    return {"mensagem": "SalesInsight API está no ar!"}