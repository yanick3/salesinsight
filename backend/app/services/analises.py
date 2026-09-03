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

def calcular_vendas_por_mes(db: Session) -> list[dict]:
    df = carregar_vendas_dataframe(db)
    if df.empty:
        return []

    df["mes"] = df["data"].dt.to_period("M").astype(str)
    resultado = df.groupby("mes")["valor_total"].sum().reset_index()
    resultado.columns = ["mes", "faturamento"]
    resultado["faturamento"] = resultado["faturamento"].round(2)

    return resultado.to_dict(orient="records")


def calcular_produtos_mais_vendidos(db: Session, limite: int = 5) -> list[dict]:
    df = carregar_vendas_dataframe(db)
    if df.empty:
        return []

    resultado = (
        df.groupby("produto_nome")["quantidade"]
        .sum()
        .sort_values(ascending=False)
        .head(limite)
        .reset_index()
    )
    resultado.columns = ["produto", "quantidade_vendida"]

    return resultado.to_dict(orient="records")


def calcular_faturamento_por_categoria(db: Session) -> list[dict]:
    df = carregar_vendas_dataframe(db)
    if df.empty:
        return []

    resultado = df.groupby("categoria_nome")["valor_total"].sum().reset_index()
    resultado.columns = ["categoria", "faturamento"]
    resultado["faturamento"] = resultado["faturamento"].round(2)

    return resultado.to_dict(orient="records")

def gerar_insights(db: Session) -> list[str]:
    df = carregar_vendas_dataframe(db)

    if df.empty:
        return ["Ainda não há vendas suficientes para gerar insights."]

    insights = []

    produto_mais_vendido = df.groupby("produto_nome")["quantidade"].sum().idxmax()
    insights.append(f"O produto mais vendido foi {produto_mais_vendido}.")

    categoria_top = df.groupby("categoria_nome")["valor_total"].sum().idxmax()
    insights.append(f"A categoria {categoria_top} possui o maior faturamento.")

    cliente_mais_compras = df.groupby("cliente_nome")["id"].count().idxmax()
    insights.append(f"O cliente {cliente_mais_compras} realizou mais compras.")

    df["mes"] = df["data"].dt.to_period("M")
    faturamento_mensal = df.groupby("mes")["valor_total"].sum().sort_index()

    if len(faturamento_mensal) >= 2:
        mes_atual = faturamento_mensal.iloc[-1]
        mes_anterior = faturamento_mensal.iloc[-2]

        if mes_anterior > 0:
            variacao = ((mes_atual - mes_anterior) / mes_anterior) * 100
            if variacao >= 0:
                insights.append(
                    f"O faturamento aumentou {variacao:.1f}% em relação ao período anterior."
                )
            else:
                insights.append(
                    f"O faturamento caiu {abs(variacao):.1f}% em relação ao período anterior."
                )

    return insights