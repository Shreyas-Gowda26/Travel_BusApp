from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime,date

class BookingBase(BaseModel):
    bus_id:str
    seat_number: int
    booking_date: datetime

class BookingCreate(BookingBase):
    pass 

class BookingResponse(BookingBase):
    id : str = Field(...)
    

    class Config:
        orm_mode = True