from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analises import gerar_insights

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("/")
def obter_insights(db: Session = Depends(get_db)):
    return {"insights": gerar_insights(db)}