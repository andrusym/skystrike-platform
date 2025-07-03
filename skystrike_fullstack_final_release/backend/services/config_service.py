from sqlalchemy import select
from backend.db.session import get_session
from backend.db.models import BotConfig
from fastapi import HTTPException

async def get_all_configs() -> list[BotConfig]:
    """
    Returns a list of all BotConfig records, including ML and override fields.
    """
    async with get_session() as session:
        result = await session.execute(select(BotConfig))
        return result.scalars().all()

async def update_bot_override(
    bot_name: str,
    contracts: int | None,
    dte: int | None,
    active: bool | None
) -> BotConfig:
    """
    Applies manual override settings to a single bot configuration.
    """
    async with get_session() as session:
        bot = await session.get(BotConfig, bot_name)
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        bot.manual_override = True
        if contracts is not None:
            bot.override_contracts = contracts
        if dte is not None:
            bot.override_dte = dte
        if active is not None:
            bot.active = active
        await session.commit()
        return bot
