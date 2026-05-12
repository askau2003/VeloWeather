from fastapi import FastAPI

app = FastAPI()

@app.get("/api/data")
def read_root():
    return {"Hello": "World"}