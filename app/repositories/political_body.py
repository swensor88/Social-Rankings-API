from sqlalchemy.orm import Session

from app.models.political_body import PoliticalBody
from app.repositories.common import create, delete, get_by_id, list_all, update


def create_political_body(session: Session, payload: dict) -> PoliticalBody:
    return create(session, PoliticalBody, payload)


def list_political_bodies(session: Session) -> list[PoliticalBody]:
    return list_all(session, PoliticalBody)


def get_political_body(session: Session, body_id: int) -> PoliticalBody | None:
    return get_by_id(session, PoliticalBody, body_id)


def update_political_body(session: Session, body: PoliticalBody, payload: dict) -> PoliticalBody:
    return update(session, body, payload)


def delete_political_body(session: Session, body: PoliticalBody) -> None:
    delete(session, body)
