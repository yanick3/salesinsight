from pydantic import BaseModel


class ProdutoBase(BaseModel):
    nome: str
    categoria_id: int


from pydantic import ConfigDict


class ProdutoResponse(ProdutoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)