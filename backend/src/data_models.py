from pydantic import BaseModel
from uuid import UUID
from typing import Dict


class DataPoint(BaseModel):
    id: UUID
    text: str
    metadata: Dict
