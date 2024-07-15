from fastapi import FastAPI

from api.data_fetchers.sheets_data_fetcher import SheetsDataFetcher
from api.writers.github_writer import GithubWriter
from services.build_exercises_service import build_exercises

app = FastAPI()


@app.get("/")
async def get_build_exercises():
    sheets_fetcher = SheetsDataFetcher()
    github_writer = GithubWriter()
    return build_exercises(sheets_fetcher, github_writer)
