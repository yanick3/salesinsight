from pydantic import BaseModel


class ClienteBase(BaseModel):
    nome: str
    email: str


from pydantic import ConfigDict


class ClienteResponse(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)