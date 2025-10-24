from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/ping")
def ping():
    return JSONResponse({"status": "ok"})
