from fastapi import FastAPI

import uvicorn

from items_views import router as items_router
from users.views import router as users_router
from api_v1 import router as router_v1

from contextlib import asynccontextmanager

from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(items_router)
app.include_router(users_router)
app.include_router(
    router_v1,
    prefix=settings.api_v1_prefix,
)


@app.get("/")
def hello_index():
    return {
        "message": "hello index!",
    }


@app.get("/hello/")
def hello(name: str = "World"):
    name = name.capitalize()
    return {"message": f"Hello {name}"}


@app.post("/calc/add/")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
