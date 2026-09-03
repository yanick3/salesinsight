from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analises import (
    calcular_metricas_dashboard,
    calcular_vendas_por_mes,
    calcular_produtos_mais_vendidos,
    calcular_faturamento_por_categoria,
)
from app.schemas.dashboard import DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
def obter_dashboard(db: Session = Depends(get_db)):
    return calcular_metricas_dashboard(db)


@router.get("/vendas-por-mes")
def obter_vendas_por_mes(db: Session = Depends(get_db)):
    return calcular_vendas_por_mes(db)


@router.get("/produtos-mais-vendidos")
def obter_produtos_mais_vendidos(db: Session = Depends(get_db)):
    return calcular_produtos_mais_vendidos(db)


@router.get("/faturamento-por-categoria")
def obter_faturamento_por_categoria(db: Session = Depends(get_db)):
    return calcular_faturamento_por_categoria(db)