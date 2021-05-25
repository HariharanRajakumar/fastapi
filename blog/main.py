from fastapi import FastAPI
from .database import engine
from . import models
from .routers import blog,user

models.Base.metadata.create_all(engine)

app = FastAPI(title="Demo")

app.include_router(blog.router)
app.include_router(user.router)