from fastapi import FastAPI
from travelBus.routes import users
app = FastAPI()

@app.get("/")
def read_root():
    return {"message":"Welcome to Travel Bus App"}

app.include_router(users.router)