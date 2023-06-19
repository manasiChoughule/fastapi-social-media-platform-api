from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# only create tables if it does not exist, no need of this when we use alembic 
#models.Base.metadata.create_all(bind = engine)

app = FastAPI()
 
# allowed domains
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers =["*"]
)



# this should be first instance of app
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():    
    return {"message": "Welcome to my api!!"}





