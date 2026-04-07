import os
import time
from .firebase_config import auth
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv("FIREBASE_EMAIL")
PASSWORD = os.getenv("FIREBASE_PASSWORD")

def firebase_login(request):
    user = auth.sign_in_with_email_and_password(EMAIL, PASSWORD)

    user["expiresAt"] = time.time() + int(user.get("expiresIn", 3600))
    request.session["firebase_user"] = user

    return user


def get_token(request):
    user = request.session.get("firebase_user")

    if not user:
        user = firebase_login(request)

    if time.time() > user["expiresAt"]:
        refreshed = auth.refresh(user["refreshToken"])

        user["idToken"] = refreshed["idToken"]
        user["refreshToken"] = refreshed["refreshToken"]
        user["expiresAt"] = time.time() + 3600  # 🔑 FIX

        request.session["firebase_user"] = user

    return user["idToken"]