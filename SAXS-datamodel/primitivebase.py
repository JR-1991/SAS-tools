from typing import Optional
from pydantic import BaseModel

class PrimitiveBase(BaseModel):
    variable: Optional[str]