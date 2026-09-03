from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analises import calcular_metricas_dashboard
from app.schemas.dashboard import DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=DashboardResponse)
def obter_dashboard(db: Session = Depends(get_db)):
    return calcular_metricas_dashboard(db)