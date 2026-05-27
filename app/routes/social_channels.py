from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories import social_channel as repo
from app.schemas.social_channel import SocialChannelCreate, SocialChannelRead, SocialChannelUpdate
from app.security import require_api_key

router = APIRouter(prefix="/social-channels", tags=["social-channels"], dependencies=[Depends(require_api_key)])


@router.post("", response_model=SocialChannelRead, status_code=status.HTTP_201_CREATED)
def create_social_channel(payload: SocialChannelCreate, db: Session = Depends(get_db)) -> SocialChannelRead:
    return repo.create_social_channel(db, payload.model_dump())


@router.get("", response_model=list[SocialChannelRead])
def list_social_channels(db: Session = Depends(get_db)) -> list[SocialChannelRead]:
    return repo.list_social_channels(db)


@router.get("/{channel_id}", response_model=SocialChannelRead)
def get_social_channel(channel_id: int, db: Session = Depends(get_db)) -> SocialChannelRead:
    channel = repo.get_social_channel(db, channel_id)
    if channel is None:
        raise HTTPException(status_code=404, detail="Social channel not found")
    return channel


@router.put("/{channel_id}", response_model=SocialChannelRead)
def update_social_channel(
    channel_id: int, payload: SocialChannelUpdate, db: Session = Depends(get_db)
) -> SocialChannelRead:
    channel = repo.get_social_channel(db, channel_id)
    if channel is None:
        raise HTTPException(status_code=404, detail="Social channel not found")
    return repo.update_social_channel(db, channel, payload.model_dump(exclude_unset=True))


@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_social_channel(channel_id: int, db: Session = Depends(get_db)) -> None:
    channel = repo.get_social_channel(db, channel_id)
    if channel is None:
        raise HTTPException(status_code=404, detail="Social channel not found")
    repo.delete_social_channel(db, channel)
