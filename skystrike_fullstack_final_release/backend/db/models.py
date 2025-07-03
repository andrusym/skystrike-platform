from .base_class import Base
from sqlalchemy import Column, String, Integer, Boolean

class BotConfig(Base):
    __tablename__ = "bot_configs"

    # Primary key: unique bot identifier (e.g. "ironcondor")
    bot_name = Column(String, primary_key=True)

    # Underlying symbol for the bot
    ticker = Column(String, nullable=False)

    # ML-generated defaults
    contracts = Column(Integer, nullable=False, default=0)
    dte = Column(Integer, nullable=False, default=0)
    active = Column(Boolean, nullable=False, default=False)

    # Manual override fields (frontend-controlled)
    manual_override = Column(Boolean, nullable=False, default=False)
    override_contracts = Column(Integer, nullable=True)
    override_dte = Column(Integer, nullable=True)
