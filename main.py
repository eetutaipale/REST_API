from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/another")
async def root():
    return {"message": "Another one!"}

@app.post("/")
async def root():
    return {"message": "Post message!"}