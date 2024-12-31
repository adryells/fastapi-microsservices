from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Product(BaseModel):
    id: int
    name: str
    price: float

products = [
    {"id": 1, "name": "Manto do tricolor paulista", "price": 459.0},
    {"id": 2, "name": "Moto G34", "price": 999.0},
]

@app.get("/products")
def get_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return {"error": "Product not found"}
    return product

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
