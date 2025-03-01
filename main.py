from fastapi import FastAPI, Body
import uvicorn
from pydantic import EmailStr, BaseModel

class CreateUser(BaseModel):
    email: EmailStr


app = FastAPI()

@app.get("/")
def hello_index():
    return {
        "message": "hello index!",
    }

@app.get("/hello/")
def hello(name: str = "World"):
    name = name.capitalize()
    return {
        "message": f"Hello {name}"
    }

@app.post("/users/")
def create_user(user: CreateUser):
    return {
        "message": "success",
        "email": user.email
    }

@app.post("/calc/add/")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b,
    }

@app.get("/items/")
def list_items():
    return ["item1", "item2"]


@app.get("/items/latest/")
def get_latest_item():
    return {
        "item": {
            "id": "0",
            "name": "latest",
        }
    }

@app.get("/items/{item_id}/")
def get_item_by_id(item_id: int):
    return {
        "item": f"item{item_id}"
    }



if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)