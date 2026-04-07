import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")

if not SERVICE_ACCOUNT_FILE:
    raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_FILE is not set")


def get_sheet_rows():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )

    client = gspread.authorize(creds)

    spreadsheet = client.open("tespinjam")
    worksheet = spreadsheet.worksheet("Form Responses 2")

    values = worksheet.get_all_records()

    rows = []
    for i, record in enumerate(values, start=2):
        record["row"] = i
        rows.append(record)

    return rows


def update_datein(sheet_row, value):
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open("tespinjam")
    worksheet = spreadsheet.worksheet("Form Responses 2")

    headers = worksheet.row_values(1)
    col = headers.index("date_in") + 1
    
    if "date_in" not in headers:
        raise ValueError("Date IN column not found")

    worksheet.update_cell(sheet_row, col, value or "")
    
def delete_sheet_row(sheet_row):
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open("tespinjam")
    worksheet = spreadsheet.worksheet("Form Responses 2")

    worksheet.delete_rows(sheet_row)
def normalize_date(value):
    if not value:
        return ""
    try:
        return datetime.strptime(value, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return value
