from pydantic import BaseModel, Field

class SeatBase(BaseModel):
    bus_id: str
    seat_number: int
    seat_status: str = "available"

class SeatCreate(SeatBase):
    pass

class SeatResponse(SeatBase):
    id: str = Field(..., alias="_id")  

    class Config:
        orm_mode = True
        populate_by_name = True         
