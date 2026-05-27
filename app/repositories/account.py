from sqlalchemy.orm import Session

from app.models.account import Account
from app.repositories.common import create, delete, get_by_id, list_all, update


def create_account(session: Session, payload: dict) -> Account:
    return create(session, Account, payload)


def list_accounts(session: Session) -> list[Account]:
    return list_all(session, Account)


def get_account(session: Session, account_id: int) -> Account | None:
    return get_by_id(session, Account, account_id)


def update_account(session: Session, account: Account, payload: dict) -> Account:
    return update(session, account, payload)


def delete_account(session: Session, account: Account) -> None:
    delete(session, account)
