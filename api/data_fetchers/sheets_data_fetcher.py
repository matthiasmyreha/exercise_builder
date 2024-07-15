import json
import os
import os.path
from typing import Dict, List

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from model import Category, DataFetcher, Item, Phoneme
from utils.security import generate_random

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


class SheetsDataFetcher(DataFetcher):
    def fetchExerciseLevelConfiguration(self) -> List[Dict]:
        SPREADSHEET_ID = "1IVPvrwoGAfWusfaktxobMw1W_3Spj9q-PjFPQjzGurs"
        RANGE_NAME = "exercise_level_filters!A1:L10000"
        service = get_sheets_service()
        if not service:
            return []

        try:
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
                .execute()
            )
            values = result.get("values", [])

            if not values:
                return []

            data = sheets_to_dict(values)
            data_for_exercise = {}
            for item in data:
                code = item["exercise"]
                if code not in data_for_exercise:
                    data_for_exercise[code] = []

                nested_item = nest_dict(item)
                data_for_exercise[code].append(nested_item)
            return data_for_exercise
        except HttpError as err:
            print(err)
            return []

    def fetchPhonemes(self) -> List[Phoneme]:
        print("fetch Phonemes from Sheets")
        return []

    def fetchCategories(self) -> List[Category]:
        print("fetch Categories from Sheets")
        return []

    def fetchItems(self) -> List[Item]:
        SPREADSHEET_ID = "1IVPvrwoGAfWusfaktxobMw1W_3Spj9q-PjFPQjzGurs"
        RANGE_NAME = "items_new!A1:M10000"
        service = get_sheets_service()
        if not service:
            return []

        try:
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
                .execute()
            )
            values = result.get("values", [])

            if not values:
                return []

            data = sheets_to_dict(values)
            items = [
                Item(
                    id=item["content"] + "_" + generate_random(),
                    name=item["content"],
                    category=None,
                    image=value_if_exists(item, "image"),
                    has_image=len(item["image"] or "") > 0,
                    gender=value_if_exists(item, "gender"),
                    type=value_if_exists(item, "type"),
                    locale="de",
                    syllables=string_to_int(value_if_exists(item, "syllables")),
                    phonemes=[],
                    word_type=value_if_exists(item, "word_type"),
                    letter_distractors=(
                        letter_distractors := string_to_array(
                            value_if_exists(item, "letter_distractors")
                        )
                    ),
                    has_letter_distractors=len(letter_distractors) > 0,
                )
                for item in data
            ]

            return items
        except HttpError as err:
            print(err)
            return []


def string_to_array(value: str | None) -> List[str]:
    return value.split(",") if value else []


def string_to_int(value: str | None) -> int | None:
    return int(value) if value else None


def value_if_exists(item, key):
    return item[key] if key in item and len(item[key] or "") > 0 else None


def nest_dict(flat_dict):
    result = {}
    for key, value in flat_dict.items():
        parts = key.split(".")
        d = result
        for part in parts[:-1]:
            if part not in d:
                d[part] = {}
            d = d[part]
        if value == "":
            d[parts[-1]] = None
        elif value is None:
            d[parts[-1]] = None
        else:
            try:
                d[parts[-1]] = int(value)
            except ValueError:
                d[parts[-1]] = value
    return result


def get_sheets_service():
    try:
        service_account_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT"))
        creds = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=SCOPES
        )

        service = build("sheets", "v4", credentials=creds)
        return service
    except HttpError as err:
        print(err)
        return None


""" def get_sheets_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            config = json.loads(os.getenv("GOOGLE_SHEETS_CREDENTIALS"))
            flow = InstalledAppFlow.from_client_config(config, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        return service
    except HttpError as err:
        print(err)
        return None """


def sheets_to_dict(values: List[List[str]]) -> List[Dict[str, str]]:
    if not values:
        return []

    headers = values[0]
    json_data = []
    for row in values[1:]:
        row_data = {
            headers[i]: row[i] if i < len(row) else None for i in range(len(headers))
        }
        json_data.append(row_data)

    return json_data
