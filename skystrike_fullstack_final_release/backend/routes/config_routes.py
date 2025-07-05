# backend/routes/config_routes.py

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from ..db.session import SessionLocal
from ..db.models import BotConfig
from ..auth import get_current_user, User
from .schemas import BotConfigSchema

router = APIRouter(prefix="/api/config", tags=["config"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "",
    response_model=List[BotConfigSchema],
    dependencies=[Depends(get_current_user)],
    summary="List all bot configs",
)
def read_configs(db: Session = Depends(get_db)):
    """
    Retrieve all bot configurations, including ML defaults and manual overrides.
    """
    return db.query(BotConfig).all()


@router.patch(
    "/{bot_name}/override",
    response_model=BotConfigSchema,
    dependencies=[Depends(get_current_user)],
    summary="Apply manual override for a bot",
)
def set_override(
    bot_name: str,
    contracts: Optional[int] = Body(None, description="Override number of contracts"),
    dte:       Optional[int] = Body(None, description="Override DTE"),
    active:    Optional[bool] = Body(None, description="Override active flag"),
    db:        Session       = Depends(get_db),
):
    """
    Apply a manual override for a bot's configuration.
    """
    bot = db.get(BotConfig, bot_name)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    bot.manual_override = True
    if contracts is not None:
        bot.override_contracts = contracts
    if dte is not None:
        bot.override_dte = dte
    if active is not None:
        bot.active = active
    db.commit()
    db.refresh(bot)
    return bot
