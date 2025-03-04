from pydantic import BaseModel
from pydantic import ConfigDict

class ProductBase(BaseModel):
    name: str
    price: int
    description: str

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductCreate):
    pass

class ProductUpdatePartial(ProductCreate):
    name: str | None = None
    price: int | None = None
    description: str | None = None

