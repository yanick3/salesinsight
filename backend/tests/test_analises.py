import pandas as pd
from app.services.analises import gerar_insights


class FalsoDB:
    """Um substituto falso para a sessão do banco, só para os testes que não usam banco de verdade."""
    pass


def test_gerar_insights_com_dataframe_vazio(monkeypatch):
    def carregar_vazio(db):
        return pd.DataFrame()

    monkeypatch.setattr("app.services.analises.carregar_vendas_dataframe", carregar_vazio)

    resultado = gerar_insights(FalsoDB())

    assert resultado == ["Ainda não há vendas suficientes para gerar insights."]


def test_gerar_insights_com_dados():
    dados_falsos = pd.DataFrame({
        "id": [1, 2, 3],
        "quantidade": [5, 1, 2],
        "preco_unitario": [10.0, 100.0, 50.0],
        "valor_total": [50.0, 100.0, 100.0],
        "data": pd.to_datetime(["2026-01-10", "2026-01-15", "2026-02-05"]),
        "produto_nome": ["Caneta", "Notebook", "Caneta"],
        "cliente_nome": ["Ana", "Bruno", "Ana"],
        "categoria_nome": ["Papelaria", "Eletrônicos", "Papelaria"],
    })

    def carregar_falso(db):
        return dados_falsos

    import app.services.analises as analises_module
    analises_module.carregar_vendas_dataframe = carregar_falso

    resultado = gerar_insights(FalsoDB())

    assert "Caneta" in resultado[0]
    assert "Papelaria" in resultado[1]
    assert "Ana" in resultado[2]