from app.database import Base, engine
from app.models import Categoria, Produto, Cliente, Venda

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")