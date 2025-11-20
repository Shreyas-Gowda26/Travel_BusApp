from fastapi import APIRouter, HTTPException, status, Depends
from passlib.context import CryptContext
from .token import create_access_token
from travelBus.schemas.users_schema import UserLogin,UserCreate,UserResponse   # adjust import path
from travelBus.database import users_collection

router = APIRouter(tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    user_dict = user.dict()
    user_dict["password"] = pwd_context.hash(user.password)

    result = users_collection.insert_one(user_dict)

    return {
        "id": str(result.inserted_id),
        "name": user.name,
        "email": user.email
    }

@router.post("/login")
async def login(request: UserLogin):   
    user = users_collection.find_one({"email": request.email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not pwd_context.verify(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    access_token = create_access_token(
        data={"user_id": str(user["_id"])}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
