import pandas as pd
from sqlalchemy.orm import Session
from app.models import Categoria, Produto, Cliente, Venda


def get_or_create_categoria(db: Session, nome: str) -> Categoria:
    categoria = db.query(Categoria).filter(Categoria.nome == nome).first()
    if categoria is None:
        categoria = Categoria(nome=nome)
        db.add(categoria)
        db.flush()
    return categoria


def get_or_create_produto(db: Session, nome: str, categoria: Categoria) -> Produto:
    produto = db.query(Produto).filter(Produto.nome == nome).first()
    if produto is None:
        produto = Produto(nome=nome, categoria_id=categoria.id)
        db.add(produto)
        db.flush()
    return produto


def get_or_create_cliente(db: Session, nome: str, email: str) -> Cliente:
    cliente = db.query(Cliente).filter(Cliente.email == email).first()
    if cliente is None:
        cliente = Cliente(nome=nome, email=email)
        db.add(cliente)
        db.flush()
    return cliente


def processar_csv(db: Session, caminho_arquivo: str) -> dict:
    df = pd.read_csv(caminho_arquivo)

    colunas_esperadas = {
        "data", "cliente_nome", "cliente_email",
        "produto_nome", "categoria_nome",
        "quantidade", "preco_unitario"
    }
    if not colunas_esperadas.issubset(df.columns):
        faltando = colunas_esperadas - set(df.columns)
        raise ValueError(f"Colunas faltando no CSV: {faltando}")

    df = df.dropna(subset=list(colunas_esperadas))

    vendas_criadas = 0

    for _, linha in df.iterrows():
        categoria = get_or_create_categoria(db, linha["categoria_nome"])
        produto = get_or_create_produto(db, linha["produto_nome"], categoria)
        cliente = get_or_create_cliente(db, linha["cliente_nome"], linha["cliente_email"])

        quantidade = int(linha["quantidade"])
        preco_unitario = float(linha["preco_unitario"])
        valor_total = quantidade * preco_unitario

        venda = Venda(
            produto_id=produto.id,
            cliente_id=cliente.id,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
            valor_total=valor_total,
            data=pd.to_datetime(linha["data"]),
        )
        db.add(venda)
        vendas_criadas += 1

    db.commit()

    return {"vendas_importadas": vendas_criadas}