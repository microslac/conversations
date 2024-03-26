from typing import Optional
from pydantic import BaseModel


class TeamUser(BaseModel):
    team: str
    user: str
    auth: Optional[str]
