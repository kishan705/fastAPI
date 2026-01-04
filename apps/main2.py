#main2.py
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user,auth,votes
from . import config
from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "https://www.google.com",
    "http://localhost:3000",  
    # "*"                        # ⚠️ DANGER: This allows EVERYONE in the world
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_credentials=True,
    allow_methods=["*"],        # Allow all types (GET, POST, DELETE, etc.)
    allow_headers=["*"],        # Allow all headers
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)