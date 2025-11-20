from fastapi import APIRouter,HTTPException,status,Depends
from travelBus.database import seats_collection
from travelBus.schemas.seat_schema import SeatCreate,SeatResponse
from travelBus.schemas.bus_schema import BusResponse
from typing import List
router = APIRouter(
    prefix="/seats",
    tags=["Seats"]
)


def create_seats_for_bus(bus_id: str, total_seats: int):
    for n in range(1, total_seats + 1):
        seats_collection.insert_one({
            "bus_id": bus_id,
            "seat_number": n,
            "seat_status": "available"
        })

@router.get("/bus/{bus_id}", response_model=List[SeatResponse])
def get_seats_for_bus(bus_id: str):
    seats = list(seats_collection.find({"bus_id": bus_id}))
    response = []

    for seat in seats:
        seat["_id"] = str(seat["_id"])   # <-- FIX
        response.append(seat)

    return response

@router.get("/bus/{bus_id}/available")
def get_available_seats(bus_id: str):
    seats = list(seats_collection.find({
        "bus_id": bus_id,
        "seat_status": "available"
    }))
    if not seats:
        return {"message": "Seats are full. No available seats."}
    response = []
    for seat in seats:
        seat["_id"] = str(seat["_id"])
        response.append(seat)

    return response


@router.get("/bus/{bus_id}/booked", response_model=List[SeatResponse])
def get_booked_seats(bus_id: str):
    seats = seats_collection.find({
        "bus_id": bus_id,
        "seat_status": "booked"
    })
    response = []
    for seat in seats:
        seat["_id"] = str(seat["_id"])
        response.append(seat)

    return response

