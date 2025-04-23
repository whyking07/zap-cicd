from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
 
app = FastAPI()
security = HTTPBasic()
 
# In-memory "database"
fake_users = {"admin": "pass123"}
 
@app.get("/")
def read_root():
    return {"msg": "Welcome to the API"}
 
@app.get("/private")
def private_area(credentials: HTTPBasicCredentials = Depends(security)):
    user = credentials.username
    password = credentials.password
    if fake_users.get(user) != password:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"msg": f"Hello, {user}"}