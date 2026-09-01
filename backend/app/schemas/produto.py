from pydantic import BaseModel


class ProdutoBase(BaseModel):
    nome: str
    categoria_id: int


class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True