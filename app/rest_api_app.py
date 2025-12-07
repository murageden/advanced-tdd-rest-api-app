from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def status_page():
    response = {
        "msg": "Welcome! This shows that the API is up and running fine",
        "status_code": 200
    }
    return response