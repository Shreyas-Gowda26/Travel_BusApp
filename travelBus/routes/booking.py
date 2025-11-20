from fastapi import APIRouter, HTTPException,status
from travelBus.database import bookings_collection
from travelBus.schemas.booking_schema import BookingCreate, BookingResponse
from bson import ObjectId
from datetime import datetime
from travelBus.database import seats_collection
router = APIRouter(
    prefix="/bookings",
    tags=["Booking"]
)

@router.post("/", response_model=BookingResponse, status_code=201)
async def create_booking(booking: BookingCreate):
    if not booking.bus_id:
        raise HTTPException(400, "Invalid bus ID")

    if booking.seat_number <= 0:
        raise HTTPException(400, "Invalid seat number")
    seat = seats_collection.find_one({
        "bus_id": booking.bus_id,
        "seat_number": booking.seat_number
    })
    if not seat:
        raise HTTPException(404, "Seats are full")
    if seat["seat_status"] == "booked":
        raise HTTPException(400, "Seat already booked") 
    seats_collection.update_one(
        {"_id": seat["_id"]},
        {"$set": {"seat_status": "booked"}}
    )

    booking_data = booking.model_dump()

    if isinstance(booking_data["booking_date"], datetime) is False:
        booking_data["booking_date"] = datetime.combine(
            booking_data["booking_date"], datetime.min.time()
        )
    result = bookings_collection.insert_one(booking_data)
    new_booking = bookings_collection.find_one({"_id": result.inserted_id})


    return BookingResponse(
        id=str(new_booking["_id"]),
        bus_id=new_booking["bus_id"],
        seat_number=new_booking["seat_number"],
        booking_date=new_booking["booking_date"]
    )

@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: str):
    booking = bookings_collection.find_one({"_id": ObjectId(booking_id)})
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return BookingResponse(
        id=str(booking["_id"]),
        bus_id=booking["bus_id"],
        seat_number=booking["seat_number"],
        booking_date=booking["booking_date"],
    )

@router.delete("/delete/{id}")
def delete_booking(id: str):
    result = bookings_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    return {"detail": "Booking deleted successfully"}

@router.get("/", response_model=list[BookingResponse])
def get_all_bookings():
    bookings = []
    for booking in bookings_collection.find():
        bookings.append(BookingResponse(
            id=str(booking["_id"]),
            bus_id=booking["bus_id"],
            seat_number=booking["seat_number"],
            booking_date=booking["booking_date"],
        ))
    return bookings