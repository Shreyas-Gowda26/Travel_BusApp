from fastapi import APIRouter,HTTPException,status
from travelBus.database import buses_collection
from travelBus.schemas.bus_schema import BusCreate,BusResponse
from typing import List
from travelBus.routes.seats import create_seats_for_bus
router = APIRouter(
    prefix="/buses",
    tags=["Buses"]
)

@router.post("/",response_model=BusResponse)
def create_bus(bus:BusCreate):
    bus_dict = bus.model_dump()
    result = buses_collection.insert_one(bus_dict)
    bus_id = str(result.inserted_id)
    create_seats_for_bus(bus_id, bus.total_seats)
    return BusResponse(
        id=str(result.inserted_id),
        arrival_time=bus.arrival_time,
        departure_time=bus.departure_time,
        origin=bus.origin,
        destination=bus.destination,
        total_seats=bus.total_seats,
        bus_number=bus.bus_number,
        is_cancelled=bus.is_cancelled
    )

@router.get("/",response_model=List[BusResponse])
def get_buses():
    buses = []
    for bus in buses_collection.find():
        result = {k: v for k,v in bus.items() if k!="_id"}
        result["id"]=str(bus["_id"])
        buses.append(BusResponse(**result))
    return buses

@router.get("/{bus_id}",response_model=BusResponse)
def get_bus_by_id(bus_id:str):
    bus = buses_collection.find_one({"_id":bus_id})
    if not bus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus not found")
    return BusResponse(
        id=str(bus["_id"]),
        arrival_time=bus["arrival_time"],
        departure_time=bus["departure_time"],
        origin=bus["origin"],
        destination=bus["destination"],
        total_seats=bus["bus_seats"]
    )

