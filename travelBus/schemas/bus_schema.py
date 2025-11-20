from pydantic import BaseModel,Field
from typing import Optional


class BusBase(BaseModel):
    bus_number: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    total_seats: int
    is_cancelled: bool = False
class BusCreate(BusBase):
    pass 

class BusResponse(BusBase):
    id :str = Field(... )

    class Config:
        orm_mode = True