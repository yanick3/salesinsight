from pydantic import BaseModel


class ClienteBase(BaseModel):
    nome: str
    email: str


class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True