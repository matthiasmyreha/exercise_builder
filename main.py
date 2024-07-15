from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def build_exercises():
    return "Building exercises"
