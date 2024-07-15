from api.data_fetchers.sheets_data_fetcher import SheetsDataFetcher
from api.writers.github_writer import GithubWriter
from api.writers.local_disc_writer import LocalDiskWriter
from services.build_exercises_service import build_exercises


def main():
    sheets_fetcher = SheetsDataFetcher()
    github_writer = LocalDiskWriter()
    return build_exercises(sheets_fetcher, github_writer)


if __name__ == "__main__":
    main()
