import firebase_admin
import os
from dotenv import load_dotenv


from firebase_admin import credentials, db

load_dotenv()

cred = credentials.Certificate(
    os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    )

firebase_admin.initialize_app(cred, {
    "databaseURL" : os.getenv("DATABASE_URL")
})

def firebase_ref(path):
    return db.reference(path)
