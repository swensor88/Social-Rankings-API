from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import political_body as repo
from app.schemas.political_body import PoliticalBodyCreate, PoliticalBodyRead, PoliticalBodyUpdate
from app.security import require_api_key

router = APIRouter(prefix="/political-bodies", tags=["political-bodies"], dependencies=[Depends(require_api_key)])


@router.post("", response_model=PoliticalBodyRead, status_code=status.HTTP_201_CREATED)
def create_political_body(payload: PoliticalBodyCreate, db: Session = Depends(get_db)) -> PoliticalBodyRead:
    return repo.create_political_body(db, payload.model_dump())


@router.get("", response_model=list[PoliticalBodyRead])
def list_political_bodies(db: Session = Depends(get_db)) -> list[PoliticalBodyRead]:
    return repo.list_political_bodies(db)


@router.get("/{body_id}", response_model=PoliticalBodyRead)
def get_political_body(body_id: int, db: Session = Depends(get_db)) -> PoliticalBodyRead:
    body = repo.get_political_body(db, body_id)
    if body is None:
        raise HTTPException(status_code=404, detail="Political body not found")
    return body


@router.put("/{body_id}", response_model=PoliticalBodyRead)
def update_political_body(
    body_id: int, payload: PoliticalBodyUpdate, db: Session = Depends(get_db)
) -> PoliticalBodyRead:
    body = repo.get_political_body(db, body_id)
    if body is None:
        raise HTTPException(status_code=404, detail="Political body not found")
    return repo.update_political_body(db, body, payload.model_dump(exclude_unset=True))


@router.delete("/{body_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_political_body(body_id: int, db: Session = Depends(get_db)) -> None:
    body = repo.get_political_body(db, body_id)
    if body is None:
        raise HTTPException(status_code=404, detail="Political body not found")
    repo.delete_political_body(db, body)
