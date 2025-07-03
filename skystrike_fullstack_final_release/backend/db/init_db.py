import asyncio
from .session import engine
from .base_class import Base
from .models import BotConfig

async def init_db():
    """
    Initializes the database, creating the bot_configs table.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
