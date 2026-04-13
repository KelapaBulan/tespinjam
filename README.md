# tespinjam — Item Borrowing Tracker

A Django-based item borrowing management system that uses **Google Sheets** as the primary data source and **Firebase** as a sync target. Admins can view borrowing records, confirm return dates, delete entries, and export data to CSV — all from a simple web interface.

---

## Features

- View all borrowing records pulled live from Google Sheets
- Sync Google Sheets data to Firebase with one click
- Confirm return date (Date IN) per entry
- Auto-detect status: **Borrowed** / **Returned** based on Date IN
- Delete entries directly from the sheet
- Export all records as a CSV file
- Firebase Realtime Database integration

---

## Requirements

- Python 3.10+
- Node.js (for any JS tooling in `node_modules`)
- A Google Cloud project with Sheets API enabled
- A Firebase project with Realtime Database enabled

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/KelapaBulan/tespinjam.git
cd tespinjam
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

> If there is no `requirements.txt`, install manually:
> ```bash
> pip install django pyrebase4 gspread google-auth
> ```

### 4. Configure Google Sheets

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the **Google Sheets API** and **Google Drive API**
3. Create a **Service Account** and download the credentials JSON file
4. Share your Google Sheet with the service account email
5. Place the credentials file in the project and reference it in `sheets_client.py`

### 5. Configure Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a project and enable **Realtime Database**
3. Go to Project Settings → Service Accounts → generate a new private key
4. Update `firebase_config.py` with your Firebase project credentials:

```python
config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_PROJECT.firebaseapp.com",
    "databaseURL": "https://YOUR_PROJECT-default-rtdb.firebaseio.com",
    "storageBucket": "YOUR_PROJECT.appspot.com",
}
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Run the development server

```bash
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`.

---

## Project Structure

```
tespinjam/
├── tespinjam/              # Main Django app
│   ├── views.py            # All views (index, sync, CSV, delete, update)
│   ├── urls.py             # URL routing
│   ├── firebase_config.py  # Firebase connection setup
│   ├── firebase_auth.py    # Firebase token helper
│   ├── sheet_firebase_sync.py  # Sync logic from Sheets → Firebase
│   ├── sheets_client.py    # Google Sheets read/write helpers
│   └── templates/
│       └── index.html      # Main borrowing table UI
├── tespinjam1/             # Secondary Django app (config or additional module)
├── node_modules/           # JS dependencies
├── manage.py
└── .gitignore
```

---

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Main borrowing table |
| `/sync/` | Sync Google Sheets → Firebase |
| `/update-datein/` | Save return date for an entry |
| `/delete/` | Delete an entry from the sheet |
| `/download-csv/` | Download all records as CSV |

---

## How It Works

1. Borrowing requests are submitted via a **Google Form** linked to a Google Sheet
2. The Django app reads rows directly from the sheet via the Sheets API
3. Status is automatically determined: if `Date IN` is filled → **Returned**, otherwise → **Borrowed**
4. Admins can confirm return dates and delete entries through the web UI, which writes back to the sheet
5. The **Sync** button pushes the latest sheet data to Firebase Realtime Database

---

## Notes

- The `node_modules` folder should not be committed — add it to `.gitignore` if not already
- Make sure your service account credentials file is also in `.gitignore` to avoid leaking secrets
- Date fields are normalized automatically to handle different date formats from the Google Form
