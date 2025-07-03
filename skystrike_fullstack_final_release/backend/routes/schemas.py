from pydantic import BaseModel
from typing    import Optional

class BotConfigSchema(BaseModel):
    bot_name:          str
    ticker:            str
    contracts:         int
    dte:               int
    active:            bool
    manual_override:   bool
    override_contracts: Optional[int]
    override_dte:       Optional[int]

    class Config:
        orm_mode = True
