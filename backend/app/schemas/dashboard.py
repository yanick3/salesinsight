from pydantic import BaseModel
from typing import Optional


class DashboardResponse(BaseModel):
    faturamento_total: float
    quantidade_vendas: int
    ticket_medio: float
    produto_mais_vendido: Optional[str] = None
    cliente_que_mais_comprou: Optional[str] = None