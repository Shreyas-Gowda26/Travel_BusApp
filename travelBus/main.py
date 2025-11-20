from fastapi import FastAPI
from travelBus.auth import auth
from travelBus.routes import bus,booking,seats
app = FastAPI()

@app.get("/")
def read_root():
    return {"message":"Welcome to Travel Bus App"}


app.include_router(auth.router)
app.include_router(bus.router)
app.include_router(booking.router)
app.include_router(seats.router)