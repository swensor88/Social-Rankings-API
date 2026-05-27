from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import account as repo
from app.schemas.account import AccountCreate, AccountRead, AccountUpdate
from app.security import require_api_key

router = APIRouter(prefix="/accounts", tags=["accounts"], dependencies=[Depends(require_api_key)])


@router.post("", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)) -> AccountRead:
    return repo.create_account(db, payload.model_dump())


@router.get("", response_model=list[AccountRead])
def list_accounts(db: Session = Depends(get_db)) -> list[AccountRead]:
    return repo.list_accounts(db)


@router.get("/{account_id}", response_model=AccountRead)
def get_account(account_id: int, db: Session = Depends(get_db)) -> AccountRead:
    account = repo.get_account(db, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/{account_id}", response_model=AccountRead)
def update_account(account_id: int, payload: AccountUpdate, db: Session = Depends(get_db)) -> AccountRead:
    account = repo.get_account(db, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return repo.update_account(db, account, payload.model_dump(exclude_unset=True))


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)) -> None:
    account = repo.get_account(db, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    repo.delete_account(db, account)
