from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,EmailStr
from typing import List
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
class User(BaseModel):
    first_name:str
    last_name:str
    age:int
    email:EmailStr
    height:float

user_data: List[User] = []
@app.middleware("http")
async def log_middleware(request:Request, call_next):
    start_time = time.time()

    response = await call_next(request)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Request: {request.method} {request.url} | Duration: {duration:.4f} seconds")
    return response

app.middleware("http")(log_middleware)


@app.post("/Users", status_code=201)
def create_user(user: User):
    user_data.append(user)
    return{
        "message": "user created successfully!"
    }
