from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import politician as repo
from app.schemas.politician import PoliticianCreate, PoliticianRead, PoliticianUpdate
from app.security import require_api_key

router = APIRouter(prefix="/politicians", tags=["politicians"], dependencies=[Depends(require_api_key)])


@router.post("", response_model=PoliticianRead, status_code=status.HTTP_201_CREATED)
def create_politician(payload: PoliticianCreate, db: Session = Depends(get_db)) -> PoliticianRead:
    return repo.create_politician(db, payload.model_dump())


@router.get("", response_model=list[PoliticianRead])
def list_politicians(db: Session = Depends(get_db)) -> list[PoliticianRead]:
    return repo.list_politicians(db)


@router.get("/{politician_id}", response_model=PoliticianRead)
def get_politician(politician_id: int, db: Session = Depends(get_db)) -> PoliticianRead:
    politician = repo.get_politician(db, politician_id)
    if politician is None:
        raise HTTPException(status_code=404, detail="Politician not found")
    return politician


@router.put("/{politician_id}", response_model=PoliticianRead)
def update_politician(
    politician_id: int, payload: PoliticianUpdate, db: Session = Depends(get_db)
) -> PoliticianRead:
    politician = repo.get_politician(db, politician_id)
    if politician is None:
        raise HTTPException(status_code=404, detail="Politician not found")
    return repo.update_politician(db, politician, payload.model_dump(exclude_unset=True))


@router.delete("/{politician_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_politician(politician_id: int, db: Session = Depends(get_db)) -> None:
    politician = repo.get_politician(db, politician_id)
    if politician is None:
        raise HTTPException(status_code=404, detail="Politician not found")
    repo.delete_politician(db, politician)
