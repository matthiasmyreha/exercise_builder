from fastapi import FastAPI

from services.build_exercises_service import build_exercises

app = FastAPI()


@app.get("/")
async def get_build_exercises():
    return build_exercises()
