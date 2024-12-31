import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
import uvicorn

app = FastAPI()

SECRET_KEY = "MIAUUUU"

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    if request.username == "admin" and request.password == "password":
        token = jwt.encode(
            {"username": request.username, "exp": datetime.datetime.now() + datetime.timedelta(hours=1)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/verify")
def verify(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"valid": True, "username": decoded["username"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
