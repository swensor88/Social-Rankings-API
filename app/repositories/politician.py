from sqlalchemy.orm import Session

from app.models.politician import Politician
from app.repositories.common import create, delete, get_by_id, list_all, update


def create_politician(session: Session, payload: dict) -> Politician:
    return create(session, Politician, payload)


def list_politicians(session: Session) -> list[Politician]:
    return list_all(session, Politician)


def get_politician(session: Session, politician_id: int) -> Politician | None:
    return get_by_id(session, Politician, politician_id)


def update_politician(session: Session, politician: Politician, payload: dict) -> Politician:
    return update(session, politician, payload)


def delete_politician(session: Session, politician: Politician) -> None:
    delete(session, politician)
