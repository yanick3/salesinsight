from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rota_raiz():
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "SalesInsight API está no ar!"}