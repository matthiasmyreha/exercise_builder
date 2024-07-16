from fastapi import FastAPI, HTTPException

from api.data_fetchers.sheets_data_fetcher import SheetsDataFetcher
from api.writers.github_writer import GithubWriter
from services.build_exercises_service import build_exercises

app = FastAPI()


@app.get("/")
async def get_build_exercises():
    sheets_fetcher = SheetsDataFetcher()
    github_writer = GithubWriter()
    result = build_exercises(sheets_fetcher, github_writer)
    if result["status"] == "success":
        return {"status": "success", "message": "Exercises built successfully"}
    elif result["status"] == "error":
        raise HTTPException(status_code=500, detail=result.message)
