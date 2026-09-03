import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Venda, Produto, Cliente, Categoria


def carregar_vendas_dataframe(db: Session) -> pd.DataFrame:
    vendas = db.query(
        Venda.id,
        Venda.quantidade,
        Venda.preco_unitario,
        Venda.valor_total,
        Venda.data,
        Produto.nome.label("produto_nome"),
        Cliente.nome.label("cliente_nome"),
        Categoria.nome.label("categoria_nome"),
    ).join(Produto, Venda.produto_id == Produto.id) \
     .join(Cliente, Venda.cliente_id == Cliente.id) \
     .join(Categoria, Produto.categoria_id == Categoria.id) \
     .all()

    df = pd.DataFrame(vendas, columns=[
        "id", "quantidade", "preco_unitario", "valor_total",
        "data", "produto_nome", "cliente_nome", "categoria_nome"
    ])

    if not df.empty:
        df["data"] = pd.to_datetime(df["data"])

    return df


def calcular_metricas_dashboard(db: Session) -> dict:
    df = carregar_vendas_dataframe(db)

    if df.empty:
        return {
            "faturamento_total": 0,
            "quantidade_vendas": 0,
            "ticket_medio": 0,
            "produto_mais_vendido": None,
            "cliente_que_mais_comprou": None,
        }

    faturamento_total = df["valor_total"].sum()
    quantidade_vendas = len(df)
    ticket_medio = df["valor_total"].mean()

    produto_mais_vendido = (
        df.groupby("produto_nome")["quantidade"].sum().idxmax()
    )

    cliente_que_mais_comprou = (
        df.groupby("cliente_nome")["valor_total"].sum().idxmax()
    )

    return {
        "faturamento_total": round(float(faturamento_total), 2),
        "quantidade_vendas": int(quantidade_vendas),
        "ticket_medio": round(float(ticket_medio), 2),
        "produto_mais_vendido": produto_mais_vendido,
        "cliente_que_mais_comprou": cliente_que_mais_comprou,
    }