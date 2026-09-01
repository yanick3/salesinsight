import shutil
import tempfile
import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.importacao import processar_csv

router = APIRouter(prefix="/upload", tags=["Importação"])


@router.post("/")
def upload_csv(arquivo: UploadFile = File(...), db: Session = Depends(get_db)):
    if not arquivo.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="O arquivo precisa ser um .csv")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        shutil.copyfileobj(arquivo.file, tmp)
        caminho_temporario = tmp.name

    try:
        resultado = processar_csv(db, caminho_temporario)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    finally:
        os.remove(caminho_temporario)

    return resultado