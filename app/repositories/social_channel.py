from sqlalchemy.orm import Session

from app.models.social_channel import SocialChannel
from app.repositories.common import create, delete, get_by_id, list_all, update


def create_social_channel(session: Session, payload: dict) -> SocialChannel:
    return create(session, SocialChannel, payload)


def list_social_channels(session: Session) -> list[SocialChannel]:
    return list_all(session, SocialChannel)


def get_social_channel(session: Session, channel_id: int) -> SocialChannel | None:
    return get_by_id(session, SocialChannel, channel_id)


def update_social_channel(session: Session, channel: SocialChannel, payload: dict) -> SocialChannel:
    return update(session, channel, payload)


def delete_social_channel(session: Session, channel: SocialChannel) -> None:
    delete(session, channel)
