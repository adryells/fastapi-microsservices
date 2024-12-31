from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import requests

app = FastAPI()

AUTH_SERVICE_URL = "http://127.0.0.1:8000/verify"
PRODUCT_SERVICE_URL = "http://127.0.0.1:8001/products"


class Order(BaseModel):
    product_id: int
    quantity: int
    token: str


orders = []


def verify_token(token: str):
    response = requests.get(AUTH_SERVICE_URL, params={"token": token})
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return response.json()


@app.post("/orders")
def create_order(order: Order, user=Depends(verify_token)):
    product_response = requests.get(f"{PRODUCT_SERVICE_URL}/{order.product_id}")
    if product_response.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")

    product = product_response.json()
    total_price = product["price"] * order.quantity
    new_order = {
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_price": total_price,
        "username": user["username"]
    }
    orders.append(new_order)
    return {"message": "Order created", "order": new_order}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8002)
