from .sheets_client import get_sheet_rows
from .firebase_admin import firebase_ref


def sync_sheet_to_firebase():
    rows = get_sheet_rows()

    if not rows or len(rows) < 2:
        return

    headers = rows[0]
    data_rows = rows[1:]

    for index, row in enumerate(data_rows):
        record = dict(zip(headers, row))

        payload = {
            "name": record.get("Name"),
            "item": record.get("Item"),
            "keperluan": record.get("keperluan"),
            "dateout": record.get("date out"),
            "datein": record.get("date in") or None,
        }

        firebase_ref("products").child(f"row_{index}").set(payload)