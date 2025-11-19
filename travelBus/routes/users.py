from fastapi import APIRouter,HTTPException,Depends
from travelBus.database import users_collection
from travelBus.schemas.users_schema import UserCreate,UserResponse
from travelBus.hashing import hash_password


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",response_model=UserResponse)
def create_user(user: UserCreate):
    if users_collection.find_one({"email":user.email}):
        raise HTTPException(status_code=400,detail="Email already registered")
    
    hashed_pwd = hash_password(user.password)
    user_dict = user.model_dump()
    user_dict["password"] = hashed_pwd
    result = users_collection.insert_one(user_dict)
    new_user = users_collection.find_one({"_id":result.inserted_id})
    return UserResponse(
        id=str(new_user["_id"]),
        name= new_user["name"],
        email=new_user["email"]
    )