from fastapi import FastAPI
from src.api import main_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(main_router)
<<<<<<< HEAD
=======


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],     
    allow_headers=["*"],   
)
>>>>>>> df3111053c3a26cda76bee187fddb5c789d5c9c7
