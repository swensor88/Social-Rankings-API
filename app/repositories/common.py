from typing import Any, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


def create(session: Session, model_cls: type[ModelType], payload: dict[str, Any]) -> ModelType:
    obj = model_cls(**payload)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def list_all(session: Session, model_cls: type[ModelType]) -> list[ModelType]:
    return list(session.query(model_cls).all())


def get_by_id(session: Session, model_cls: type[ModelType], object_id: int) -> ModelType | None:
    return session.get(model_cls, object_id)


def update(session: Session, obj: ModelType, payload: dict[str, Any]) -> ModelType:
    for key, value in payload.items():
        setattr(obj, key, value)
    session.commit()
    session.refresh(obj)
    return obj


def delete(session: Session, obj: ModelType) -> None:
    session.delete(obj)
    session.commit()
